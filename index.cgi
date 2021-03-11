#!/home/seedplus-cam/.pyenv/versions/3.8.1/envs/3.8.1_flask/bin/python

# #!/home/seedplus-cam/.pyenv/versions/3.8.1_flask/bin/python
# -*- coding: utf-8 -*-

from wsgiref.handlers import CGIHandler
from app import app
from sys import path

path.insert(0, '/seedplus-cam/www/apps')


class ProxyFit(object):
	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		environ['SERVER_NAME'] = 'seedplus-cam.sakura.ne.jp'
		environ['SERVER_PORT'] = '80'
		environ['REQUEST_METHOD'] = 'GET'
		environ['SCRIPT_NAME'] = ''
		environ['PATH_INFO'] = '/'
		environ['QUERY_STRING'] = ''
		environ['SERVER_PROTOCOL'] = 'HTTP/1.1'
		return self.app(environ, start_response)

if __name__ == '__main__':
	app.wsgi_app = ProxyFit(app.wsgi_app)
	# print('Content-Type: text/html\n')
	CGIHandler().run(app)