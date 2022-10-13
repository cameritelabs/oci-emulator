import logging

from flask import Flask
from flask_cors import CORS

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from app.routes.sample import sample
from app.routes.object_storage.bucket_operations import bucket_operations
from app.routes.object_storage.objects import objects
from app.routes.object_storage.namespace import namespace
from app.routes.compute_cli import compute
from app.routes.identity import identity
from app.routes.nosql_database.tables import tables
from app.routes.middleware import middleware


app = Flask(__name__)
CORS(app)
app.register_blueprint(sample)
app.register_blueprint(bucket_operations)
app.register_blueprint(objects)
app.register_blueprint(namespace)
app.register_blueprint(compute, url_prefix="/20160918")
app.register_blueprint(identity, url_prefix="/20160918")
app.register_blueprint(tables)
app.wsgi_app = middleware(app.wsgi_app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12000, debug=True)
