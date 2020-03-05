from pathlib import Path

from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog

from settings.paths import MODEL_DIR

cfg = get_cfg()

cfg.MODEL.DEVICE = 'cpu'
cfg.merge_from_file(model_zoo.get_config_file('COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml'))
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 13


cfg.MODEL.WEIGHTS = Path(MODEL_DIR, 'model_final.pth').as_posix()
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7

fashion_metadata = MetadataCatalog.get('fashion').set(
            thing_classes=[
                'short sleeve top',
                'long sleeve top',
                'short sleeve outwear',
                'long sleeve outwear',
                'vest',
                'sling',
                'shorts',
                'trousers',
                'skirt',
                'short sleeve dress',
                'long sleeve dress',
                'vest dress',
                'sling dress'
            ])

__all__ = [
    'fashion_metadata',
    'cfg'
]
