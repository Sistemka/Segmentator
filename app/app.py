from flask import Flask
from flask_restplus import Api, reqparse, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.datastructures import FileStorage

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


api = Api(
    app=app,
    doc='/swagger-ui',
    title='SearchEngine',
    description='Service to search in our image data base'
)


basic_args = reqparse.RequestParser(bundle_errors=True, trim=True)
basic_args.add_argument('X-SERVICE-NAME', location='headers', required=True, nullable=False)

segmentation_image_args = reqparse.RequestParser(bundle_errors=True, trim=True)
segmentation_image_args.add_argument('image', type=FileStorage, location='files', required=True)
segmentation_image_args.add_argument(
    'mode', type=fields.String(enum=['box', 'mask']), location='args', default='box'
)