from flask import Blueprint

blueprint = Blueprint(
    "scanner_blueprint",
    __name__,
    url_prefix="/api/scanner",
)
