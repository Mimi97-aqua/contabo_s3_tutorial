"""
Application entrypoint
"""

import os

from flask import Flask

from routes.app import s3_ops


def create_app():
    """
    Application factory
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.register_blueprint(s3_ops)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
