from os import environ

import boto3
from flask import Flask, request


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py', silent=True)
    if 'S3_BUCKET' in environ:
        app.config['S3_BUCKET'] = environ['S3_BUCKET']
    if 'S3_PREFIX' in environ:
        app.config['S3_PREFIX'] = environ['S3_PREFIX']
    s3_bucket = app.config['S3_BUCKET']
    s3_prefix = app.config.get('S3_PREFIX', '')

    @app.route('/')
    def hello():
        return 'Hello, World!'

    @app.route('/webhook', methods=['POST'])
    def receive():
        filename = request.args.get('name')

        if filename:
            app.logger.info(f'Receiving {filename}')

            s3_client = boto3.client('s3')
            s3_key = f'{s3_prefix}{filename}'
            s3_client.put_object(
                Body=request.get_data(), Bucket=s3_bucket, Key=s3_key
            )

            app.logger.info(
                f'{filename} has been uploaded to s3://{s3_bucket}/{s3_key}'
            )

            return (
                '<?xml version="1.0" encoding="utf-8"?>'
                '<Data><Status>True</Status></Data>',
                {'Content-Type': 'application/xml'},
            )

    return app
