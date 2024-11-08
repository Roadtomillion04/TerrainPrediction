import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np

labels_csv = pd.read_csv(r"C:\Users\trc\Desktop\4. WebCam Capture for TerrainPrediction\model\data\TerrainDataset - Sheet1.csv")

labels = labels_csv.road_type.to_numpy()

unique_roads = np.unique(labels)

IMG_SIZE = 224

# Create a function for preprocessing images
def process_image(img_path: str, img_size: int = IMG_SIZE) -> tf.Tensor:
    """ # DocString
    Takes an image file path and turns into a Tensor.
    """
    # Read in an image file
    image = tf.io.read_file(filename=img_path)

    # Turn the jped image into numerical Tensor with 3 color channel (Red, Green, Blue)
    image = tf.image.decode_jpeg(contents=image, channels=3)  # content = image as we read the image path above

    # convert the color channel values from 0 - 255 to 0 - 1 values / normalization
    image = tf.image.convert_image_dtype(image=image,
                                         dtype=tf.float32)  # Convert image to dtype, scaling its values if needed.
    # dtype= tf.float32 or image = image / 255.0 both are same

    # Resize the image to our desired value (224, 224)
    image = tf.image.resize(images=image, size=(img_size, img_size))

    return image

BATCH_SIZE: int = 32

def create_data_batches(X, y= None, batch_size: int= BATCH_SIZE, valid_data: bool= False, test_data: bool= False):
    """ # DcoString
    Creates batches of data out of image (X) and label (y) pairs.
    Shuffles the data if it's training data but doesn't shuffle if it's validation data.
    Also accepts test data as input (no labels).
    """
    # If the data is test dataset, we probably don't have labels
    if test_data:
        print('Creating test data batches...') # for conifirmation

        # Turn filepaths and labels into Tensors
        # tf.data.Dataset - is how to create dataset in tf, from_tensor_slices - Creates a Dataset whose elements are slices of the given tensors.
        data = tf.data.Dataset.from_tensor_slices(tf.constant(X)) # convert X to tensor by tf.constant, and only filepaths (no labels)
        # Transforming
        # map - Maps map_func across the elements of this dataset.
        data_batch = data.map(map_func= process_image).batch(batch_size= BATCH_SIZE) # batch(n) splits elements into n size set
        return data_batch           # process_image() function we created above

# Create a function to load a trained model
def load_model(model_path):
    """ # DocString
    Loads a saved model from a specified path.
    """
    print(f"Loading a model from: {model_path}")
    load_model = tf.keras.models.load_model(filepath= model_path, # Loads a model saved via model.save()
                                            custom_objects= {"KerasLayer": hub.KerasLayer})
    return load_model

# Turn prediction probabilities into thier respective label (easier to understand)
def get_pred_label(prediction_probabilities):
    """ # DocString
    Turns an array of prediction probabilities into a label
    """
    return unique_roads[np.argmax(prediction_probabilities)]

import requests
def download_image(url):
    res = requests.get(url= url)
    content = res.content

    with open("image.jpg", "wb") as file:
        file.write(content)