from flask import Blueprint

bp = Blueprint("health", __name__, url_prefix="/health")

@bp.route('/')
def health_check():
    return {'status': 'UP'}
