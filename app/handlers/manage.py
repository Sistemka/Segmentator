import os
from pathlib import Path

from flask import jsonify
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
@ns.expect(basic_args)
class Segmentation(Resource):
    @ns.expect(segmentation_image_args)
    def post(self):
        basic_args.parse_args()
        args = segmentation_image_args.parse_args()
        image = args['image']
        image_name = secure_filename(image.filename)
        image_path = Path(FILES_DIR, image_name).as_posix()
        image.save(image_path)
        print(image_path)
        result = segmentator(image_path)

        os.remove(image_path)
        return jsonify({
            'error': False,
            'result': result
        })


def register(main_api):
    main_api.add_namespace(ns)
