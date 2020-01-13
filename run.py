#!/usr/bin/env python3
import argparse

from ruamel.yaml import YAML

from app import app

yaml = YAML(typ="safe")


def default_config():
    return {
        "debug_mode": False,
    }


def config_from_file(config_path):
    with open(config_path, "r") as f:
        return yaml.load(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    args = parser.parse_args()
    if args.config is None:
        config = default_config()
    else:
        config = config_from_file(args.config)
    app.run(debug=config["debug_mode"])
