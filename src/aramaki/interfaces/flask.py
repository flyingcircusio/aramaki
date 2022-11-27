import logging

import click
import waitress
from flask import Flask

import aramaki
import aramaki.system

app = Flask(__name__)


@app.route(aramaki.System.actor_id)
def system_actor_info():
    with app.aramaki:
        system = ...
        return {
            "@context": ["https://www.w3.org/ns/activitystreams"],
            "type": "System",
            "id": system.actor_id,
            # "following": "https://kenzoishii.example.com/following.json",
            # "followers": "https://kenzoishii.example.com/followers.json",
            "inbox": system.inbox_url,
            # "outbox": request.route_url("outbox"),
            # "preferredUsername": "aramaki",
            "name": system.name,
            # "icon": [""],
        }


@click.group()
@click.option("--database", default="sqlite:///aramaki.sqlite")
@click.option("--application-url", default="http://localhost:6543")
@click.option("--host", default="localhost")
@click.option("--port", default=6543)
@click.pass_context
def main(database, application_url, host, port):
    print(f"Ready. Listening on {host}:{port} ...")

    logging.basicConfig()
    logging.getLogger().setLevel(
        logging.INFO
    )  # Basically silence all logs from the root logger

    logger = logging.getLogger("waitress")
    logger.setLevel(logging.INFO)

    app.aramaki = aramaki.app(db_uri=database, application_url=application_url)

    waitress.serve(app, host=host, port=port)
