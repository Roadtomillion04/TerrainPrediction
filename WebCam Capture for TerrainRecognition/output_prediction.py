import random
from pynter.pynter import generate_captioned
from terrain_prediction import *

# result of custom image prediction
def plot_figure(webcam_image: bool= False, random_image: bool = False, webcam_image_url:str= None, prediction_image_name: str = None):
    custom_image_path: list = []
    custom_images = []

    if webcam_image:
        webcam_image_path: str = download_image(url= webcam_image_url)
        custom_image_path.append(webcam_image_path)
    elif random_image:
        custom_image_path.extend([ # absolute path required
            rf"/Users/nirmalkumar/Desktop/4. WebCam Capture for TerrainPrediction/images/{random.randrange(start= 0, stop= 824, step= 100)}.jpg"])

    # Turn custom_images to data batches
    custom_data = create_data_batches(X= custom_image_path, test_data= True)

    # Loading full model
    loaded_full_model = load_model(
        model_path= r"Trained models/20220422-10041650621891-Terrain-Road-prediction-model-mobilenetv2-Adam.h5")

    # Make predictions on the custom data
    custom_preds = loaded_full_model.predict(custom_data)

    custom_pred_label = [get_pred_label(prediction_probabilities=custom_preds[i]) for i in range(len(custom_preds))]

    # Loop through unbatched data
    for image in custom_data.unbatch().as_numpy_iterator():
        custom_images.append(image)  # for displaying using plt.imshow()

    for image in custom_image_path:

        font = r"/Users/nirmalkumar/Desktop/4. WebCam Capture for TerrainPrediction/font/FreeMonoBold.ttf"

        im = generate_captioned(text= custom_pred_label[0],
                                image_path= image,
                                size= (1270, 720),
                                font_path= font,
                                filter_color= (0, 0, 0, 40))

        im = im.convert(mode= "RGB") # jpg doesn't support alpha channel
        im.save(fp= rf"/Users/nirmalkumar/Desktop/4. WebCam Capture for TerrainPrediction/predicted_images/{prediction_image_name}.jpg")
        # we can't overwrite file while running second time