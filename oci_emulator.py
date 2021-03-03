import logging

from flask import Flask

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from app.routes.sample import sample

app = Flask(__name__)
app.register_blueprint(sample)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=12000, debug=True)
