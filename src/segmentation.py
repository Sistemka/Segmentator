import uuid
from pathlib import Path
import shutil

import cv2
import numpy as np
from detectron2.utils.visualizer import Visualizer, GenericMask
from detectron2.engine import DefaultPredictor

from settings.config import fashion_metadata, cfg
from settings.paths import FILES_DIR


def crop_image_mask_and_save(image, outputs, result_images_dir, vis):

    masks = np.asarray(outputs["instances"].pred_masks)
    masks = [GenericMask(x, vis.output.height, vis.output.width) for x in masks]

    areas = np.asarray([x.area() for x in masks])

    sorted_idxs = np.argsort(-areas).tolist()
    masks = [masks[idx] for idx in sorted_idxs]
    boxes = [outputs["instances"].pred_boxes[idx] for idx in sorted_idxs]

    for i, box in zip(range(len(masks)), boxes):
        background = np.ones(image.shape, dtype=np.uint8)
        background.fill(255)

        for j, segment in enumerate(masks[i].polygons):
            item_mask = np.array([segment.reshape(-1, 2)], dtype=np.int32)
            cv2.fillPoly(background, item_mask, 0)

        masked_image = cv2.bitwise_or(image, background)
        x1, y1, x2, y2 = [round(cord) for cord in box.tensor.tolist()[0]]
        crop_img = masked_image[y1:y2, x1:x2]

        cropped_image_path = Path(result_images_dir, f"{uuid.uuid4()}.jpg").as_posix()
        cv2.imwrite(cropped_image_path, crop_img)


def crop_image_and_save(image, outputs, result_images_dir):
    for box in outputs["instances"].pred_boxes:
        x1, y1, x2, y2 = [round(cord) for cord in box.tolist()]
        crop_img = image[y1:y2, x1:x2]
        cropped_image_path = Path(result_images_dir, f"{uuid.uuid4()}.jpg").as_posix()
        cv2.imwrite(cropped_image_path, crop_img)


def load_segmentator():
    predictor = DefaultPredictor(cfg)

    def segmentate(image_path, mode='box'):
        image = cv2.imread(image_path)
        outputs = predictor(image)

        # return None if no fashion objects found on picture
        if not outputs['instances'].pred_boxes:
            return None

        v = Visualizer(image[:, :, ::-1], metadata=fashion_metadata)
        vis_full = v.draw_instance_predictions(outputs['instances'].to('cpu'))

        result_images_dir = Path(FILES_DIR, str(uuid.uuid4()))
        result_images_dir.mkdir(exist_ok=True, parents=True)

        full_image_path = Path(result_images_dir, f"full_{uuid.uuid4()}.jpg").as_posix()

        cv2.imwrite(full_image_path, vis_full.get_image()[:, :, ::-1])
        if mode == 'box':
            crop_image_and_save(image=image, outputs=outputs, result_images_dir=result_images_dir)
        elif mode == 'mask':
            crop_image_mask_and_save(
                image=image,
                outputs=outputs,
                result_images_dir=result_images_dir,
                vis=v
            )

        # make archive to send many pictures
        shutil.make_archive(
            result_images_dir,
            'zip',
            root_dir=Path(FILES_DIR, result_images_dir),
        )
        shutil.rmtree(Path(FILES_DIR, result_images_dir))
        return result_images_dir
    return segmentate


segmentator = load_segmentator()
