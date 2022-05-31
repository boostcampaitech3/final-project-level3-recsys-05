import json
from pathlib import Path

class ConfigParser:
    def __init__(self, args):
        self.config = self.from_args(args)

    def from_args(self, args):
        cfg_fname = Path(args.config)
        return self.read_json(cfg_fname)

    def read_json(self, fname):
        fname = Path(fname)
        with fname.open('rt') as handle:
            return json.load(handle)
