from google.cloud import firestore
import tensorflow as tf
import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder
import os
import requests
import json

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 

# FOLDER_DOWNLOAD_IMG = './download/'
# DOC_ID = 'ErpdNb64hA7S0UgX1kYi'

# Function to connect db in firestore
def connect_db(doc_id):
    try:
        # Initialize Firestore client
        db = firestore.Client()

        # Reference the specific document
        doc_ref = db.collection(u'images').document(doc_id)

        # Retrieve the document data
        doc = doc_ref.get()

        # Check if the document exists
        if doc.exists:
            # Retrieve the value of the "images" field
            images_data = doc.get("images")

            if images_data:
                # Create a list to store the extracted information
                extracted_info = []

                # Iterate over the keys (image filenames) and values (image data)
                for filename, image_data in images_data.items():
                    color = image_data.get('color')
                    img_link = image_data.get('publicUrl')
                    extracted_info.append({'filename': filename, 'color': color, 'img_link': img_link})

                return extracted_info

            else:
                return None  # The document does not have an "images" field.

        else:
            return None  # No such document with the specified ID.

    except Exception as e:
        print(f"Error: {e}")
        return None  # Handle the error and return None

# Function to download images
def download_image(image_info, download_path='download'):
    try:
        # Ensure the download directory exists
        os.makedirs(download_path, exist_ok=True)

        filename = image_info.get('filename')
        img_link = image_info.get('img_link')

        if filename and img_link:
            response = requests.get(img_link)
            if response.status_code == 200:
                # Save the image to the specified directory
                image_path = os.path.join(download_path, filename)
                with open(image_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded: {filename}")
                return image_path
            else:
                print(f"Failed to download: {filename}, Status Code: {response.status_code}")
        else:
            print("Invalid image information")

    except Exception as e:
        print(f"Error: {e}")

# Function to predict type fashion
def predict(folder_path, model, classes, class_list):
    results = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".JPG"):
            image_path = os.path.join(folder_path, filename)

            # Load and preprocess the image
            img = Image.open(image_path).convert("RGB")
            img = img.resize((224, 224))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = np.array([img_array])
            img_array = img_array.astype('float32') / 255.

            # Predictions
            predictions = model.predict(img_array, verbose=0)

            predicted_class = np.argmax(predictions)
            predicted_probability = float(predictions[0, predicted_class])

            # Map Predicted class
            predicted_class_label = classes[predicted_class]
            encode_class_label = class_list[predicted_class]

            # Store the results in a dictionary
            result_dict = {
                "filename": filename,
                "image_path": image_path,
                # "label": predicted_class_label,
                # "predicted_probability": predicted_probability,
                "type": encode_class_label
            }

            results.append(result_dict) 
    return results           

# Function to Combine predict data, and connect db data
def combine(folder_path, model, classes, class_list, doc_id):

    # Predict
    prediction_results = predict(folder_path, model, classes, class_list)

    # Connect to the database
    db_data = connect_db(doc_id=doc_id)

    # Combine results
    raw_image_data = {}
    for prediction_result in prediction_results:
        filename = os.path.basename(prediction_result["image_path"])

        # Find the corresponding db_data for the current filename
        matching_db_item = next((db_item for db_item in db_data if db_item["filename"] == filename), None)

        if matching_db_item:
            full_image_path = os.path.join(folder_path, filename)

            combined_result = {
                "image_path": full_image_path,
                "type": prediction_result["type"],
                "color": matching_db_item["color"],
                "img_link": matching_db_item["img_link"]
            }

            raw_image_data[filename] = combined_result

    return raw_image_data

def process_and_return_json_data(folder_path, doc_id):
    # Connect to the database
    result = connect_db(doc_id=doc_id)

    if result:
        for info in result:
            print(f'{info["img_link"]}')
            download_image(info)

    else:
        print('Error or no data returned.')

    # Define your class list
    class_list = [
        "Dresses", "Hoodie", "Pants", "Jackets", "Jeans", 
        "Longsleeve", "Shirts", "Shorts", "Skirts", "Tops", "Tshirts", 
    ]

    label_encoder = LabelEncoder()
    label_encoder.classes_ = np.load('./train/label_encoder_classes.npy', allow_pickle=True)
    classes = list(label_encoder.classes_)

    # Function to load model
    model = tf.keras.models.load_model('./train/Lambi.h5')

    raw_image_data = combine(folder_path=folder_path, model=model, 
                             classes=classes, class_list=class_list, doc_id=doc_id)

    output_file_path = "raw_image.json"  # Replace with the desired output file path

    # Save the result to a .json file
    with open(output_file_path, 'w') as json_file:
        json.dump(raw_image_data, json_file, indent=2)

    # print(f"JSON data saved to {output_file_path}")

    # Read the content of the saved JSON file
    with open(output_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    return output_file_path


