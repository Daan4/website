from app import create_app

app = create_app('config.config')
port=80

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False,port=port)
