import logging

from flask import Blueprint

logger = logging.getLogger(__name__)
sample = Blueprint("sample", __name__)


@sample.route("/", methods=["GET"])
def index():
    return ""
