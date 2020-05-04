import os

from ruamel.yaml import YAML

yaml = YAML(typ="safe")


class DefaultConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = 5000
    ALLOW_REGISTER = True
    SHOW_TOP_COLLECTORS = True


def dict_to_config(config_dict):
    config = {}
    x = str(config_dict.get("debug_mode", ""))
    if x.lower() == "true":
        config["ENV"] = "development"
        config["DEBUG"] = True
    x = config_dict.get("database_url")
    if x:
        config["SQLALCHEMY_DATABASE_URI"] = x
    x = config_dict.get("port")
    if x:
        config["PORT"] = int(x)
    x = str(config_dict.get("allow_register", ""))
    if x.lower() == "false":
        config["ALLOW_REGISTER"] = False
    x = str(config_dict.get("show_top_collectors", ""))
    if x.lower() == "false":
        config["SHOW_TOP_COLLECTORS"] = False
    return config


def from_env():
    return {
        "debug_mode": os.environ.get("DEBUG_MODE"),
        "database_url": os.environ.get("DATABASE_URL"),
        "port": os.environ.get("PORT"),
        "allow_register": os.environ.get("ALLOW_REGISTER"),
        "show_top_collectors": os.environ.get("SHOW_TOP_COLLECTORS"),
    }


def load_config():
    config = from_env()
    config_path = os.environ.get("RECIPE_BOOK_CONFIG")
    if config_path:
        with open(config_path, "r") as f:
            config = {**config, **yaml.load(f)}
    return dict_to_config(config)
