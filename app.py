"""
Application runner on non-production environments.
"""

from redirectioneaza import app
from redirectioneaza.config import DEV

if __name__ == '__main__':
    app.run(host=app.config['SERVER_HOST'],
            port=app.config['SERVER_PORT'],
            debug=False)
