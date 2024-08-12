import logging
from random import randint

from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def roll():
    return randint(1, 6)


@app.route("/rolldice")
def roll_dice():
    player = request.args.get("player", default=None, type=str)
    result = str(roll())
    if player:
        logger.warning(f"{player} is rolling the dice: {result}")
    else:
        logger.warning(f"anonymous player is rolling the dice: {result}")

    return result
