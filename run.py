#!/usr/bin/env python3
import multiprocessing

from gunicorn.app.base import BaseApplication

from app import app


def worker_count():
    return 2 * multiprocessing.cpu_count() + 1


class Application(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    if app.config["ENV"] == "development":
        app.run(port=app.config["PORT"])
    else:
        options = {
            "bind": "0.0.0.0:"+str(app.config["PORT"]),
            "workers": worker_count(),
        }
        Application(app, options).run()
