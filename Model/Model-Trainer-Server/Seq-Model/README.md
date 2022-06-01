# PyTorch Template

## Usage
train
`python -W ignore main.py -c config.json`

### Config file format
Config files are in `.json` format:
```javascript
{
    "model_name": "Seq-Model",
    "embedding_name": "Seq-Embedding",
    "save_dir" : "./save",
    "remote_server_uri" : "http://34.64.110.227:5000",
    "experiment_name" : "/Seq-Model",
    "user" : "SeongBeom",

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
    "emb_cols" : ["Seq-Embedding"]
}

```
