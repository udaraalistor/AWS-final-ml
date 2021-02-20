import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import numpy as np


class IdentityObject:
    def __init__(self):
        self.detector = hub.load("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1").signatures['default']

    def identify(self, image_path):
        im = Image.open(image_path)
        image_arr = np.array(im)
        converted_img = tf.image.convert_image_dtype(image_arr, tf.float32)[tf.newaxis, ...]
        result = self.detector(converted_img)
        result = {key: value.numpy() for key, value in result.items()}
        return result
