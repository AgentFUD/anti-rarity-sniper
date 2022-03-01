import json
import os
from flask import Flask, jsonify, send_file
from os.path import exists
from brownie import Contract, network
from dotenv import load_dotenv
from filelock import FileLock


metadata_dir = "./data/metadata"
image_dir = "./data/images"
database_file = "./database/db.txt"

APP_ROOT = os.path.join(os.path.dirname(__file__), "..")  # noqa
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)

CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
CONTRACT_ABI = os.getenv("CONTRACT_ABI")
WEB3_INFURA_PROJECT_ID = os.getenv("WEB3_INFURA_PROJECT_ID")
BROWNIE_NETWORK = os.getenv('BROWNIE_NETWORK')

app = Flask(__name__)
network.connect(BROWNIE_NETWORK)


@app.route("/<id>.json", methods=["GET"])
def get_metadata(id: int):
    fname = f"{metadata_dir}/{id}.json"
    if exists(fname) and check_if_minted(id):
        with open(fname) as jsonfile:
            return json.load(jsonfile)
    else:
        return jsonify({"error": "Ooops, not found..."})


@app.route("/<id>.png", methods=["GET"])
def get_image(id: int):
    fname = f"{image_dir}/{id}.png"
    if exists(fname) and check_if_minted(id):
        return send_file(
            fname,
            mimetype="image/png",
            attachment_filename=f"{id}.png",
            cache_timeout=0,
        )
    else:
        return jsonify({"error": "Ooops, not found..."})


def check_if_minted(id: int) -> bool:
    with open(database_file, "r") as db:
        last_total_supply = int(db.readline().strip())
    if last_total_supply > int(id):
        return True

    contract = Contract.from_abi(
        "EvolvensNFT", CONTRACT_ADDRESS, json.loads(CONTRACT_ABI)
    )
    totalSupply = int(contract.totalSupply())
    if totalSupply > last_total_supply:
        lock = FileLock(database_file + ".lock")
        with lock:
            with open(database_file, "w") as dbFile:
                dbFile.write(str(totalSupply))
    return int(id) < totalSupply and int(id) >= 0


if __name__ == "__main__":
    app.run(debug=True)
