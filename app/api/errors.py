from flask import jsonify, request
from app.api import bp

def error_message(message, code):
    return {'response': 'error', 'message': message, 'status_code':code}

@bp.errorhandler(404)
def resource_not_found(e):
    #if request.path.startswith('/api/'):
    return jsonify(error_message('Resource not found', 404))