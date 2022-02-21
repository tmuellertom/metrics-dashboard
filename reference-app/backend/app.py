from flask import Flask, render_template, request, jsonify

import pymongo
from flask_pymongo import PyMongo

from jaeger_client import Config
import logging

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': "simplest-agent.observability.svc.cluster.local",
                'reporting_port': 5775,
            },
            'logging': True,
        },
        service_name=service,
    )

    return config.initialize_tracer()

tracer = init_tracer('backend')

@app.route("/")
def homepage():
    with tracer.start_span('hello-world'):
        return "Hello World"


@app.route("/api")
def my_api():
    answer = "something"
    with tracer.start_span('api'):
        return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
def add_star():
    star = mongo.db.stars
    name = request.json["name"]
    distance = request.json["distance"]
    star_id = star.insert({"name": name, "distance": distance})
    new_star = star.find_one({"_id": star_id})
    output = {"name": new_star["name"], "distance": new_star["distance"]}
    return jsonify({"result": output})


if __name__ == "__main__":
    app.run()
