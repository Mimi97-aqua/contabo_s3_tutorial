"""
Bluepirint for CRUD operations in S3
"""

import os
import requests

from flask import Blueprint, jsonify, request

from utils.utils import check_size_and_type, generate_presigned_url

s3_ops = Blueprint("s3_ops", __name__, url_prefix="/api")


@s3_ops.route('/', methods=['POST'])
def upload_file():
    """
	Generates presigned URL for uploading file to object storage
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


@s3_ops.route('/', methods=['GET'])
def view_file():
    """
    Renders uploaded content using the file URL and content type generated during upload
    
    returns: a presigned URL for viewing/downloading the content
    """
    data = request.json
    file_url = data.get('file_url')
    content_type = data.get('content_type')
	
    if not file_url or not content_type:
        return jsonify({
            "status": "error",
            "message": "Both 'file_url' and 'content_type' must be provided."
		}), 400

	# the file url ends with /bucketname/filenamme.extension e.g /mybucket/image.jpg
    # so to get the filename, we must split from the bucketname and take the last item
    filename = file_url.split(f"{os.environ.get('BUCKET_NAME')}/")[-1]

    return jsonify({
        "status": "success",
        "message":{
            'file_url': generate_presigned_url(method='get_object', content_type=content_type, key=filename)
		}
	}), 200
    

@s3_ops.route('/', methods=['DELETE'])
def delete_file():
    """
    Generates preseigned URL for deleting and makes an HTTP DELETE request to
    remove the specified file from the s3 bucket
    """
    file_url = request.json.get('file_url')
    if not file_url:
        return jsonify({
            'status': 'error',
            'message': "'file_url' required"
		}), 400

    filename = file_url.split(f"{os.environ.get('BUCKET_NAME')}/")[-1]
    delete_url = generate_presigned_url(method='delete_object', key=filename)
    response = requests.delete(delete_url)

    if response.status_code != 204:
        return jsonify({
            'status': 'error',
            'message': f'Failed to delete file: {response.reason}'
		}), 400

    return jsonify({
        'status': 'success',
        'message': 'File successfully deleted'
	}), 200