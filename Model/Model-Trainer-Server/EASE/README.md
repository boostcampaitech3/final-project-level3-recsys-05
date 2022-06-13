# EASE

## Model Architecture
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173226134-e99b1754-0639-4b8e-8b0e-c87f43088746.png" /></p>

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
    "model_type" : "ease",

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
