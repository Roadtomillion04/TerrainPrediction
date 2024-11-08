import pandas as pd
import numpy as np
from model.train_functions.functions import get_pred_label, download_image, load_model, process_image, create_data_batches


# Get custom image filepaths
import os
import random

# if user_input == 1:
custom_image_link = input("Enter image url path: ")
download_image(custom_image_link)
custom_image_path = ["image.jpg"]

# elif user_input == 2:
# custom_image_path = [
#     rf"C:\Users\trc\Desktop\4. WebCam Capture for TerrainPrediction\model\images\{random.randrange(start= 0, stop= 356)}.jpg",
#     rf"C:\Users\trc\Desktop\4. WebCam Capture for TerrainPrediction\model\images\{random.randrange(start= 357, stop= 724)}.jpg",
#     rf"C:\Users\trc\Desktop\4. WebCam Capture for TerrainPrediction\model\images\{random.randrange(start= 725, stop= 824)}.jpg"
# ] #tensors requires list for conversion
#
# # else:
#     print("unhandled_input")

# Turn custom_images to data batches
custom_data = create_data_batches(X= custom_image_path, test_data= True)

# Loading full model
loaded_full_model = load_model(model_path= r"C:\Users\trc\Desktop\4. WebCam Capture for TerrainPrediction\model\Trained models\20220422-10041650621891-Terrain-Road-prediction-model-mobilenetv2-Adam.h5")

# Make predictions on the custom data
custom_preds = loaded_full_model.predict(custom_data)

# Get custom image prediction labels
custom_pred_label = [get_pred_label(prediction_probabilities= custom_preds[i]) for i in range(len(custom_preds))]

custom_images = []

# Loop through unbatched data
for image in custom_data.unbatch().as_numpy_iterator():
    custom_images.append(image) # for displaying using plt.imshow()

