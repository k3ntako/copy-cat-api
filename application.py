import logging
from waitress import serve
from copycat import create_app

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

application = create_app()

if __name__ == '__main__':
    serve(application, host='0.0.0.0', port=5000)
  