import os
import tomllib

CONFIG_PATH = "./config"
CONFIG_NAME = "dev.toml"


class Config:

    def __init__(self):
        self._config: dict
        self.load_config()

    def load_config(self):
        with open(os.path.join(CONFIG_PATH, CONFIG_NAME), "rb") as f:
            self._config = tomllib.load(f)

    @property
    def config(self):
        return self._config
