import databaseManagement
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from nltk.corpus import stopwords
from io import BytesIO


def rotateImageClockwise(img, degrees):
    rotatedImage = img.rotate(-degrees, expand=True)
    return rotatedImage

def cropImage(img, cropBox):
    croppedImage = img.crop(cropBox)
    return croppedImage

def generateWordcloud():
    # Fetch words from the database
    maskText = databaseManagement.getWordsFromCloud()
    if maskText:
        # Define a custom colormap with blue and gold colors
        colors = ["#0000FF", "#D3D3D3"]  # Blue and Light Grey
        cmapName = "blue_grey"
        n_bins = 100  # Number of bins in the colormap
        cmap = LinearSegmentedColormap.from_list(cmapName, colors, N=n_bins)
        # Assuming you already have the image mask and other configurations
        imageMask = np.array(Image.open('./usaa_logo.png'))

        wc = WordCloud(
            background_color='black',
            mask=imageMask,
            contour_width=2,
            contour_color='black',
            colormap=cmap,
            width=800,
            height=500
        ).generate(maskText)

        # Convert the word cloud to an image
        wordcloudImage = wc.to_image()
        
        # Rotate the word cloud image
        rotatedImage = rotateImageClockwise(wordcloudImage, 30)

        # Define the crop box (left, upper, right, lower)
        cropBox = (100, 250, 1500, 1300)

        # Crop the rotated word cloud image
        croppedImage = cropImage(rotatedImage, cropBox)

        # Display the rotated word cloud image (optional)
        plt.axis("off")
        plt.imshow(croppedImage, interpolation='bilinear')
        plt.show()

        # Convert the rotated image to bytes
        img = BytesIO()
        croppedImage.save(img, format='PNG')
        img.seek(0)
        return img
    else:
        print("No words fetched from the database.")
        return None

