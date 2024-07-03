import os
from celery import Celery, Task
from flask import Flask
from importlib import import_module
from flask_cors import CORS
import logging
from settings import Config
from typing import Any


def make_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
        include=["app.views.scanner.tasks"]
    )
    celery.conf.update(app.config)

    class ContextTask(Task):
        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def register_blueprints(flask_app: Flask) -> None:
    for module_name in ("scanner",):
        module = import_module("app.views.{}.routes".format(module_name))
        flask_app.register_blueprint(module.blueprint)


def create_app(config: Config) -> Flask:
    flask_app = Flask(__name__)
    flask_app.config.from_object(config)

    register_blueprints(flask_app)

    CORS(flask_app, resources={r"/*": {"origins": "*"}})

    # Default scanner settings directory
    default_scanner_settings = os.path.join(flask_app.root_path, "scanner_settings")
    scanner_settings_directory = flask_app.config.get(
        "SCANNER_SETTINGS", default_scanner_settings
    )

    if not os.path.exists(scanner_settings_directory):
        os.makedirs(scanner_settings_directory)

    flask_app.config["SCANNER_SETTINGS"] = scanner_settings_directory
    logging.info(f"Scanner settings directory set to: {scanner_settings_directory}")

    celery = make_celery(flask_app)

    flask_app.extensions["celery"] = celery

    return flask_app


def make_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler("scanner.log")
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
