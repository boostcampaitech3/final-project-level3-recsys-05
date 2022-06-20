# LightGCN

## Model Architecture
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173226266-b6ed5ff8-4199-487d-930e-de3ad37e0652.png" /></p>

## Usage
train
`python -W ignore main.py -c config.json`

### Config file format
Config files are in `.json` format:
```javascript
{
    "model_update" : false,
    "model_update_url" : "http://101.101.218.250:30002/update/",
    "model_update_key" : 123456,
    "model_type" : "lightGCN",

    "model_name": "LightGCN",
    "embedding_name": "LightGCN-Embedding",
    "save_dir" : "./save",
    "remote_server_uri" : "http://34.64.110.227:5000",
    "experiment_name" : "/LightGCN",
    "user" : "SeongBeom",

    "data_dir" : "./data",
    "data_name" : "user",

    "seed" : 22,
    "epochs" : 30,
    "batch_size" : 5000,
    "num_workers" : 8,
    "hidden_units" : 128,
    "n_layers" : 2,
    "reg" : 1e-5,
    "node_dropout_rate" : 0.2,
    "lr" : 0.001
}
```
