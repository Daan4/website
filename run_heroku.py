from app import create_app
import os
import waitress

app = create_app('config.heroku_config')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    waitress.serve(app, host='0.0.0.0', port=port, url_scheme='https')
