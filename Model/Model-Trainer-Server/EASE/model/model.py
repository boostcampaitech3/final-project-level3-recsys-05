import gc
import torch

class EASE():
    def __init__(self, reg):
        self.reg = reg
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    def clear_memory(self):
        gc.collect()
        torch.cuda.empty_cache()

    def fit(self, X):
        X = X.to(self.device)
        G = X.t() @ X
        diagIndices = torch.eye(G.shape[0]) == 1
        G[diagIndices] += self.reg

        P = G.inverse()
        B = P / (-1 * P.diag())
        B[diagIndices] = 0

        self.B = B.cpu()
    
    def predict(self, X):
        output = (X.to(self.device) @ self.B.to(self.device)).cpu()
        return output
