from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


FILES_DIR = Path(BASE_DIR, 'files')
FILES_DIR.mkdir(parents=True, exist_ok=True)

MODEL_DIR = Path(BASE_DIR, 'models')
MODEL_PATH = Path(MODEL_DIR, 'model_final.pth').as_posix()
MODEL_DIR.parent.mkdir(parents=True, exist_ok=True)
