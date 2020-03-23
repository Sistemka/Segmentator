from flask import Flask
from flask_restplus import Api, reqparse, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.datastructures import FileStorage

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


api = Api(
    app=app,
    doc='/swagger-ui',
    title='Segmentator',
    description='Service to segmentate fashion images on picture'
)


basic_args = reqparse.RequestParser(bundle_errors=True, trim=True)
basic_args.add_argument('X-SERVICE-NAME', location='headers', required=True, nullable=False)

segmentation_image_args = reqparse.RequestParser(bundle_errors=True, trim=True)
segmentation_image_args.add_argument('image', type=FileStorage, location='files', required=True)
segmentation_image_args.add_argument(
    'mode', type=str, location='args', default='box'
)
