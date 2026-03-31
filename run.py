from app import create_app
from app.utils import init_data_files
import os

if __name__ == '__main__':
    init_data_files()
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
