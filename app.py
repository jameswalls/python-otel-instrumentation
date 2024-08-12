import logging
from random import randint

from flask import Flask, request
from opentelemetry import trace, metrics

# aquire a tracer
tracer = trace.get_tracer("diceroller.tracer")

# aquire a meter
meter = metrics.get_meter("diceroller.meter")

# counter instrument to make measurements with
roll_counter = meter.create_counter(
    "dice.rolls",
    description="number of rolls by roll value",
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def roll():
    return randint(1, 6)


@app.route("/rolldice")
def roll_dice():
    # create a span that's the child of the current one
    with tracer.start_as_current_span("roll") as roll_span:
        player = request.args.get("player", default=None, type=str)
        result = str(roll())
        roll_span.set_attribute("roll.value", result)
        roll_counter.add(1, {"roll.value": result})
        if player:
            logger.warn(f"{player} is rolling dice: {result}")
        else:
            logger.warn(f"anonymous player is rolling the dice: {result}")

        return result
