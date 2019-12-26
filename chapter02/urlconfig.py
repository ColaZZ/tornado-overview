import time

from tornado import web
import tornado



class MainHandler(web.RequestHandler):
    async def get(self, *args, **kwargs):
        self.write("hello world")

urls = [
    ("/", MainHandler),
]

if __name__ == "__main__":
    app = web.Application(urls, debug=True)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
