# Item2Vec

## Model Architecture
<p align="center"><img src="https://user-images.githubusercontent.com/65529313/173226191-7f357614-c891-40b8-8ba7-4ac1df88d2a1.png" /></p>

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
    "model_type" : "item2vec_v1",
    
    "model_name" : "Item2Vec-Embedding",
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
