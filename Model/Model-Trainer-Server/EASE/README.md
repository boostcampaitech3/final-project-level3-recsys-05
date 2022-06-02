# PyTorch Template

## Usage
train
`python -W ignore main.py -c config.json`

### Config file format
Config files are in `.json` format:
```javascript
{
    "model_name": "ease-item-similarity-matrix",
    "save_dir" : "./save",
    "remote_server_uri" : "http://34.64.110.227:5000",
    "experiment_name" : "/EASE",
    "user" : "SeongBeom",

    "data_dir" : "./data",
    "data_name" : "user",

    "reg" : 1000,
    "seed" : 22
}

```
