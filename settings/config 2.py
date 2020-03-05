import os

from dotenv import load_dotenv

from settings.paths import BASE_DIR
from utils.mrcnn.config import Config

load_dotenv(
    os.path.join(BASE_DIR, 'settings', 'env')
)
DEVICE = "/cpu:0"


class InferenceConfig(Config):
    # Run detection on one image at a time
    # Give the configuration a recognizable name
    # Give the configuration a recognizable name
    NAME = "fashion"
    BATCH_SIZE = 1

    IMAGES_PER_GPU = 1
    # Number of classes (including background)
    NUM_CLASSES = 1 + 3  # Background + pants +top +boots

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 125

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 1024

    TRAIN_ROIS_PER_IMAGE = 200


model_config = InferenceConfig()
