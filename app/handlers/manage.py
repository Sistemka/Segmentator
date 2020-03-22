import io
import os
from pathlib import Path

from flask import send_file, Response
from flask_restplus import Resource, Namespace
from werkzeug.utils import secure_filename

from src import segmentator
from app.app import basic_args, segmentation_image_args
from settings.paths import FILES_DIR


ns = Namespace(
    '',
    description='Segmentator',
    validate=True
)


@ns.route('/segmentation')
@ns.expect(basic_args, segmentation_image_args)
class Segmentation(Resource):
    def post(self):
        basic_args.parse_args()
        args = segmentation_image_args.parse_args()
        image = args['image']
        mode = args['mode']

        image_name = secure_filename(image.filename)
        image_path = Path(FILES_DIR, image_name).as_posix()
        image.save(image_path)

        result = segmentator(image_path, mode=mode)
        os.remove(image_path)

        if result is None:
            return Response(status=204)

        result_images_archive = Path(FILES_DIR,  f"{result}.zip")
        cropped_files = io.BytesIO()
        with open(result_images_archive, 'rb') as fp:
            cropped_files.write(fp.read())

        cropped_files.seek(0)
        os.remove(result_images_archive)

        return send_file(
            filename_or_fp=cropped_files,
            mimetype='application/zip',
            attachment_filename='cropped.zip'
        )


def register(main_api):
    main_api.add_namespace(ns)
