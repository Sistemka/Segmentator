import os
import uuid
from pathlib import Path

import tensorflow as tf
import matplotlib.image as mpimg
import imageio

from utils.mrcnn.model import MaskRCNN
from utils.api import image_2_vector
from settings.config import model_config, DEVICE
from settings.paths import (
    MODEL_DIR, MODEL_PATH, TMP_IMAGES_DIR, PRELOAD_IMAGE_PATH
)


def make_segmentation_mask(image, mask, rois, i):
    img = image.copy()
    img[:, :, 0] *= mask
    img[:, :, 1] *= mask
    img[:, :, 2] *= mask

    img[img[:, :, :] == 0] = 255
    cropped_image = img[rois[0]:rois[2], rois[1]:rois[3]]
    return cropped_image


def save_cropped_images(res, image):
    cropped_images = []

    for i in range(res['masks'].shape[-1]):
        mask = res['masks'][:, :, i]
        cropped_image = make_segmentation_mask(image, mask, res['rois'][i], i)

        cropped_image_path = Path(TMP_IMAGES_DIR, f"{uuid.uuid4()}.jpg")
        imageio.imwrite(cropped_image_path, cropped_image)
        cropped_images.append(cropped_image_path)

    return cropped_images


def load_segmentator():
    with tf.device(DEVICE):
        model = MaskRCNN(
            mode="inference",
            model_dir=MODEL_DIR,
            config=model_config
        )
    weights_path = MODEL_PATH
    model.load_weights(weights_path, by_name=True)

    # run predict right after load to make it work, i don't know why?! ¯\_(ツ)_/¯
    image = mpimg.imread(PRELOAD_IMAGE_PATH)
    r = model.detect([image], verbose=0)[0]

    def segmentate(image_path):
        image = mpimg.imread(image_path)
        results = model.detect([image], verbose=0)[0]
        cropped_images = save_cropped_images(res=results, image=image)

        vectors = []
        for image in cropped_images:
            vector = image_2_vector.vectorize(image_path=image)
            vectors.append(vector)
            image.unlink()

        return vectors

    return segmentate

segmentator = load_segmentator()
