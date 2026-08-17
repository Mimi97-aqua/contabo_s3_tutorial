"""
Bluepirint for CRUD operations in S3
"""

import os

from flask import Blueprint, jsonify, request

from utils.utils import check_size_and_type, generate_presigned_url

s3_ops = Blueprint("s3_ops", __name__, url_prefix="/api")


@s3_ops.route('/', methods=['POST'])
def upload_file():
    """
	Generates URL for uploading file to object storage
	"""
    if not 'file' in request.files:
        return jsonify({
			'status': 'error',
			'message': 'No file part'
		}), 400

    file = request.files['file']
    filename = file.filename

    file_type, content_type, size = check_size_and_type(file, filename)

    if not file_type:
        return jsonify({
			'status': 'error',
			'message': 'The uploaded file must be a media file.'
		}), 400

    if not size:
        return jsonify({
			'status': 'error',
			'message': 'File is more than 5MB'
		}), 400

    file_url = f"{os.environ.get('ENDPOINT_URL')}/{os.environ.get('BUCKET_NAME')}/{filename}"
    upload_url = generate_presigned_url(method='put_object', key=filename,
                                        content_type=content_type)

    if not upload_url:
        return jsonify({
			'satus': 'fail',
			'message': 'Upload URL failed to generate'
		}), 400

    return jsonify({
		'status': 'success',
		'message': {
			'file_url': file_url,
			'upload_url': upload_url,
			'content_type': content_type
		}
	}), 200
