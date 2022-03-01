from crypt import methods
import json
from flask import Flask, jsonify, send_file
from os.path import exists
import io

metadata_dir = './data/metadata'
image_dir = './data/images'
nft_contract_address = "0xd...."
infura_key = ''

app = Flask(__name__)

@app.route('/<id>.json', methods=['GET'])
def get_metadata(id: int):
    fname = f"{metadata_dir}/{id}.json"
    if exists(fname):
        with open(fname) as jsonfile:
            return json.load(jsonfile)
    else:
        return jsonify({'error': 'Ooops, not found...'}) 


@app.route('/<id>.png', methods=['GET'])
def get_image(id: int):
    fname = f"{image_dir}/{id}.png"
    if exists(fname):
        return send_file(
            fname,
            mimetype='image/png',
            attachment_filename=f"{id}.png",
            cache_timeout=0
        )
    else:
        return jsonify({'error': 'Ooops, not found...'}) 


if __name__ == "__main__":
    app.run(debug=True)
