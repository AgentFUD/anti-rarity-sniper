import json
import os
from flask import Flask, jsonify, send_file
from os.path import exists
from brownie import Contract, network
from dotenv import load_dotenv


metadata_dir = "./data/metadata"
image_dir = "./data/images"

APP_ROOT = os.path.join(os.path.dirname(__file__), "..")  # noqa
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)

contract_address = os.getenv("CONTRACT_ADDRESS")
contract_abi = os.getenv("CONTRACT_ABI")
web3_infura_project_id = os.getenv("WEB3_INFURA_PROJECT_ID")

app = Flask(__name__)
network.connect("polygon-test")


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
    contract = Contract.from_abi(
        "EvolvensNFT", contract_address, json.loads(contract_abi)
    )
    totalSupply = contract.totalSupply()
    return int(id) < int(totalSupply) and int(id) >= 0


if __name__ == "__main__":
    app.run(debug=True)
