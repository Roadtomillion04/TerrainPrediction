import matplotlib.pyplot as plt
from model.train_functions.helpers import custom_images, custom_pred_label
from PIL import Image


def plot_figure():
    # result of custom image prediction
    plt.figure(figsize= (10, 10))
    for i, image in enumerate(custom_images):
            # nrow, ncol, index
        plt.subplot(1, len(custom_images), i + 1) # index should not be 0 show i + 1

        plt.imshow(X= image)

        plt.title(custom_pred_label[i])
        plt.xticks([])
        plt.yticks([])

        plt.imsave(f"my.jpg", image)

    plt.show()
