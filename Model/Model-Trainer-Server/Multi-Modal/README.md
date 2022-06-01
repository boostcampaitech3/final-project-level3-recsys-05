# PyTorch Template

## Usage
train
`python -W ignore main.py -c config.json`

### Config file format
Config files are in `.json` format:
```javascript
{
    "model_name": "Mutl-Modal",
    "save_dir" : "./save",
    "remote_server_uri" : "http://34.64.110.227:5000",
    "experiment_name" : "/Mutl-Modal",
    "user" : "SeongBeom",
    "embedding_run_ids": {
        "Item2Vec-Embedding" : "ac8bf76b2e8c4e0d97a25f332a8781bf",
        "LightGCN-Embedding" : "485f88f10c024cb88e4e12fbbb8a55b3",
        "Seq-Embedding" : "5b52587695904a768c81604df0ede30f"
    },

    "data_dir" : "./data",
    "data_name" : "score",

    "seed" : 22,
    "epochs" : 30,
    "batch_size" : 512,
    "num_workers" : 8,
    "hidden_units" : 128,
    "num_heads" : 8,
    "num_layers" : 1,
    "dropout_rate" : 0.5,
    "lr" : 0.001,
    "emb_cols" : ["Item2Vec-Embedding", "LightGCN-Embedding", "Seq-Embedding"]
}
```
