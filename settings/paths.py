from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


FILES_DIR = Path(BASE_DIR, 'files')
FILES_DIR.mkdir(parents=True, exist_ok=True)

TMP_IMAGES_DIR = Path(BASE_DIR, 'images')
TMP_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

MODEL_DIR = Path(BASE_DIR, 'models')
MODEL_PATH = Path(MODEL_DIR, 'coco.h5').as_posix()
MODEL_DIR.parent.mkdir(parents=True, exist_ok=True)

PRELOAD_IMAGE_PATH = Path(FILES_DIR, 'preload_hello.jpg').as_posix()
