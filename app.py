from crypt import methods
import json
from flask import Flask, jsonify
from os.path import exists

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


if __name__ == "__main__":
    app.run(debug=True)
