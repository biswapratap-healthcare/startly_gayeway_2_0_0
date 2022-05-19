from flask import Flask
from waitress import serve
from flask_cors import CORS
from flask_restplus import Resource, Api, reqparse
from functions import search_image_fn


def create_app():
    app = Flask("foo", instance_relative_config=True)

    api = Api(
        app,
        version='1.0.0',
        title='Startly Gateway App',
        description='Startly Gateway App',
        default='Startly Gateway App',
        default_label=''
    )

    CORS(app)

    search_image = reqparse.RequestParser()
    search_image.add_argument('search_string',
                              type=str,
                              help='The search string.',
                              required=True)
    search_image.add_argument('style',
                              type=str,
                              help='The style filer.',
                              required=True)

    @api.route('/search_image')
    @api.expect(search_image)
    class SearchImageService(Resource):
        @api.expect(search_image)
        @api.doc(responses={"response": 'json'})
        def post(self):
            try:
                args = search_image.parse_args()
            except Exception as e:
                rv = dict()
                rv['status'] = str(e)
                return rv, 404
            try:
                search_string = args['search_string']
                style = args['style']
                rv = dict()
                rv['result'] = search_image_fn(search_string, style)
                rv['status'] = 'Success'
                return rv, 200
            except Exception as e:
                rv = dict()
                rv['status'] = str(e)
                return rv, 404

    return app


if __name__ == "__main__":
    serve(create_app(), host='0.0.0.0', port=8000, threads=100)
