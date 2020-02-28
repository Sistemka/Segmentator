import io
import os
from pathlib import Path

from flask import jsonify, send_file, Response
from flask_restplus import Resource, Namespace
from werkzeug.utils import secure_filename

from src import segmentator
from app.app import basic_args, segmentation_image_args
from settings.paths import FILES_DIR, BASE_DIR


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
        return_vector = args['return_vector']

        image_name = secure_filename(image.filename)
        image_path = Path(FILES_DIR, image_name).as_posix()
        image.save(image_path)

        result = segmentator(image_path, return_vector=return_vector)
        os.remove(image_path)

        if result is None:
            return Response(status=204)

        if return_vector is False:
            cropped_files_path = Path(BASE_DIR,  f"{result}.zip")
            cropped_files = io.BytesIO()
            with open(cropped_files_path, 'rb') as fp:
                cropped_files.write(fp.read())

            cropped_files.seek(0)
            os.remove(cropped_files_path)

            return send_file(
                filename_or_fp=cropped_files,
                mimetype='application/zip',
                attachment_filename='cropped.zip'
            )

        return jsonify({
            'error': False,
            'result': result
        })


def register(main_api):
    main_api.add_namespace(ns)
