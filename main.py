from flask import Flask, jsonify, request
from reccommender.utils.get_raw_img import process_and_return_json_data
from reccommender.utils.recommendation_library import get_combinations
import json
from dotenv import dotenv_values, load_dotenv
import os
import shutil

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 

load_dotenv()

app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

FOLDER_DOWNLOAD_IMG = './download/'
config = dotenv_values(".env")
DOC_ID2 = ''

def delete_download_folder(folder_path):
    try:
        # Check if the folder exists
        if os.path.exists(folder_path):
            # Remove the folder and its contents
            shutil.rmtree(folder_path)
    except Exception as e:
        print(f"Error deleting folder: {str(e)}")

@app.route('/api')
def hello_api():
    return 'hello api'

@app.route('/api/recommendation', methods=["POST"])
def recommend():
    try:
        # Get the JSON data from the request body
        request_data = request.json

        doc_id = request_data.get('imageID', DOC_ID2)

        json_data = process_and_return_json_data(folder_path=FOLDER_DOWNLOAD_IMG,
                                                doc_id=doc_id)
        
        with open(json_data) as f:
            outfit_data = json.load(f)

        rec = get_combinations(outfit_data)

        # Delete the download folder after processing
        delete_download_folder(FOLDER_DOWNLOAD_IMG)

        # Return a response, for example, a JSON response
        return jsonify(
            {
                "data": rec
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == '__main__':
    app.run()

