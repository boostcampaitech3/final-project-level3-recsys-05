import torch
import torch.nn as nn
import torch.nn.functional as F
import scipy.sparse as sp
import numpy as np

class LightGCN(nn.Module):
    def __init__(self, num_user, num_item, hidden_units, n_layers, reg, node_dropout_rate, R):
        super().__init__()

        # initialize Class attributes
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.u_final_embeddings = nn.Parameter(torch.rand((num_user, hidden_units)))
        self.i_final_embeddings = nn.Parameter(torch.rand((num_item, hidden_units)))

        self.num_user = num_user
        self.num_item = num_item
        self.hidden_units = hidden_units
        self.graph = self._convert_sp_mat_to_sp_tensor(self.get_adj_mat(R))

        self.reg = reg
        self.n_layers = n_layers
        self.node_dropout_rate = node_dropout_rate

        # Initialize weights
        self.weight_dict = self._init_weights()
        print("Weights initialized.")

    def get_adj_mat(self, R):
        adj_mat = sp.dok_matrix((self.num_user + self.num_item, self.num_user + self.num_item), dtype=np.float32)
        adj_mat = adj_mat.tolil() # to_list
        R = R.tolil()

        adj_mat[:self.num_user, self.num_user:] = R
        adj_mat[self.num_user:, :self.num_user] = R.T
        adj_mat = adj_mat.todok()

        adj_mat = self.normalized_adj_mat(adj_mat)

        return adj_mat

    def normalized_adj_mat(self, adj):
        rowsum = np.array(adj.sum(1))
        d_inv = np.power(rowsum, -.5).flatten()  
        d_inv[np.isinf(d_inv)] = 0.
        d_mat_inv = sp.diags(d_inv)
        norm_adj = d_mat_inv.dot(adj).dot(d_mat_inv)
        return norm_adj.tocoo()

    # initialize weights
    def _init_weights(self):
        print("Initializing weights...")
        weight_dict = nn.ParameterDict()

        initializer = torch.nn.init.xavier_uniform_
        
        weight_dict['user_embedding'] = nn.Parameter(initializer(torch.empty(self.num_user, self.hidden_units).to(self.device)))
        weight_dict['item_embedding'] = nn.Parameter(initializer(torch.empty(self.num_item, self.hidden_units).to(self.device)))
        
        return weight_dict

    # convert sparse matrix into sparse PyTorch tensor
    def _convert_sp_mat_to_sp_tensor(self, X):
        """
        Convert scipy sparse matrix to PyTorch sparse matrix

        Arguments:
        ----------
        X = Adjacency matrix, scipy sparse matrix
        """
        coo = X.tocoo().astype(np.float32)
        i = torch.LongTensor(np.mat([coo.row, coo.col]))
        v = torch.FloatTensor(coo.data)
        res = torch.sparse.FloatTensor(i, v, coo.shape).to(self.device)
        return res

    # apply node_dropout
    def _droupout_sparse(self, X):
        """
        Drop individual locations in X
        
        Arguments:
        ---------
        X = adjacency matrix (PyTorch sparse tensor)
        dropout = fraction of nodes to drop
        noise_shape = number of non non-zero entries of X
        """
        node_dropout_mask = ((self.node_dropout_rate) + torch.rand(X._nnz())).floor().bool().to(self.device)
        i = X.coalesce().indices()
        v = X.coalesce()._values()
        i[:,node_dropout_mask] = 0
        v[node_dropout_mask] = 0
        X_dropout = torch.sparse.FloatTensor(i, v, X.shape).to(self.device)

        return  X_dropout.mul(1/(1-self.node_dropout_rate))

    def forward(self, u, i, j):
        """
        Computes the forward pass
        
        Arguments:
        ---------
        u = user
        i = positive item (user interacted with item)
        j = negative item (user did not interact with item)
        """
        # apply drop-out mask
        graph = self._droupout_sparse(self.graph) if self.node_dropout_rate > 0 else self.graph
        ego_embeddings = torch.cat([self.weight_dict['user_embedding'], self.weight_dict['item_embedding']], 0)
        final_embeddings = [ego_embeddings]

        for k in range(self.n_layers):
            ego_embeddings = torch.sparse.mm(graph, final_embeddings[k])
            final_embeddings.append(ego_embeddings)                                       

        final_embeddings = torch.stack(final_embeddings, dim=1)
        final_embeddings = torch.mean(final_embeddings, dim=1)
        
        u_final_embeddings, i_final_embeddings = final_embeddings.split([self.num_user, self.num_item], 0)

        self.u_final_embeddings = nn.Parameter(u_final_embeddings)
        self.i_final_embeddings = nn.Parameter(i_final_embeddings)
        
        # loss 계산
        u_emb = u_final_embeddings[u] # user embeddings
        p_emb = i_final_embeddings[i] # positive item embeddings
        n_emb = i_final_embeddings[j] # negative item embeddings
        
        y_ui = torch.sum(torch.mul(u_emb, p_emb), dim = 1)                        
        y_uj = torch.sum(torch.mul(u_emb, n_emb), dim = 1)
        
        log_prob = torch.mean(torch.log(torch.sigmoid(y_ui - y_uj))) 
        bpr_loss = -log_prob        
        if self.reg > 0.:
            l2norm = (torch.sum(u_emb**2)/2. + torch.sum(p_emb**2)/2. + torch.sum(n_emb**2)/2.) / u_emb.shape[0]
            l2reg = self.reg * l2norm
            bpr_loss += l2reg

        return bpr_loss