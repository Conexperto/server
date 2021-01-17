from wsgi import create_wsgi

wsgi = create_wsgi();

if __name__ == '__main__':
    wsgi.run(host='0.0.0.0', port=3000)
