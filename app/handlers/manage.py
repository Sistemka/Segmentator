import os
from pathlib import Path

import numpy as np
from flask import jsonify, request
from flask_restplus import Resource, Namespace, fields
from werkzeug.utils import secure_filename

from src import indexing, predictor
from app.app import basic_args, search_image_args
from settings.paths import FILES_DIR


ns = Namespace(
    '',
    description='SearchEngine',
    validate=True
)

search_from_vector_model = ns.model('SearchFromVectorModel', {
    'vector': fields.List(fields.Float(), required=True),
})


@ns.route('/indexing')
@ns.expect(basic_args)
class Predict(Resource):
    @staticmethod
    def get():
        basic_args.parse_args()
        indexing()
        return jsonify({
            'error': False,
            'message': 'indexing finished'
        })


@ns.route('/search')
@ns.expect(basic_args)
class Search(Resource):
    @ns.expect(search_image_args)
    def post(self):
        basic_args.parse_args()
        args = search_image_args.parse_args()
        image = args['image']
        image_name = secure_filename(image.filename)
        image_path = Path(FILES_DIR, image_name).as_posix()
        image.save(image_path)
        prediction = predictor(file_path=image_path)
        os.remove(image_path)
        return jsonify({
            'error': False,
            'result': [p[0] for p in prediction]
        })


@ns.route('/search/from_vector')
@ns.expect(basic_args)
class SearchFromVector(Resource):
    @ns.expect(search_from_vector_model)
    def post(self):

        prediction = predictor(vec=np.array(request.json['vector']))

        return jsonify({
            'error': False,
            'result': [p[0] for p in prediction]
        })


def register(main_api):
    main_api.add_namespace(ns)
