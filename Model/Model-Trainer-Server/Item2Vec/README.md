# PyTorch Template

## Usage
train
`python -W ignore main.py -c config.json`

### Config file format
Config files are in `.json` format:
```javascript
{
    "model_name": "Item2Vec-Embedding",
    "save_dir" : "./save",
    "remote_server_uri" : "http://34.64.110.227:5000",
    "experiment_name" : "/Item2Vec",
    "user" : "SeongBeom",

    "data_dir" : "./data",
    "data_name" : "problem",

    "seed" : 22,
    "epochs" : 30,
    "min_count" : 1,
    "vector_size" : 128,
    "sg" : 0,
    "negative" : 10,
    "window" : 987654321
}

```
