import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image, ImageOps

# Load model once
model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

def load_image(img, size=(512, 512)):
    img = ImageOps.fit(img, size, Image.Resampling.LANCZOS)
    img = np.array(img).astype(np.float32) / 255.0
    img = tf.expand_dims(img, axis=0)
    return tf.convert_to_tensor(img, dtype=tf.float32)

def tensor_to_image(tensor):
    tensor = tensor[0]
    tensor = tf.clip_by_value(tensor, 0.0, 1.0)
    tensor = tf.image.convert_image_dtype(tensor, dtype=tf.uint8)
    return Image.fromarray(tensor.numpy())

def style_transfer(content_img, style_img, strength=1.0):
    content_tensor = load_image(content_img)
    style_tensor = load_image(style_img)
    stylized_tensor = model(content_tensor, style_tensor)[0]

    if strength < 1.0:
        blended = (1 - strength) * content_tensor + strength * stylized_tensor
        return tensor_to_image(blended)
    else:
        return tensor_to_image(stylized_tensor)
