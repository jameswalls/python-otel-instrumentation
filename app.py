from random import randint

from flask import Flask
from opentelemetry import trace

# aquire a tracer
tracer = trace.get_tracer("diceroller.tracer")

app = Flask(__name__)


@app.route("/rolldice")
def roll_dice():
    return str(roll())


def roll():
    # this creates a new span that's the child of the current one
    with tracer.start_as_current_span("roll") as rollspan:
        result = randint(1, 6)
        rollspan.set_attribute("roll.value", result)
        return result
