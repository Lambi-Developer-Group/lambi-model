from flask import Flask, render_template, jsonify
from reccommender.utils.get_raw_img import process_and_return_json_data
from reccommender.utils.recommendation_library import get_combinations
import json
from google.cloud import firestore
from dotenv import dotenv_values


app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

FOLDER_DOWNLOAD_IMG = './download/'
config = dotenv_values(".env")
DOC_ID = config['DOC_ID']


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/recommend', methods=["POST"])
def recommend():
    # sessionID = ''
    # docRef = firestore.collection('session').doc(sessionID)

    json_data = process_and_return_json_data(folder_path=FOLDER_DOWNLOAD_IMG,
                                            doc_id=DOC_ID)
    
    with open(json_data) as f:
        outfit_data = json.load(f)

    rec = get_combinations(outfit_data)

    # Return a response, for example, a JSON response
    return jsonify(
        {
            "data": rec
        }
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)

