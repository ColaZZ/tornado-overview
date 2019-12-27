import time

from tornado import web
import tornado


class MainHandler(web.RequestHandler):
    async def get(self, *args, **kwargs):
        time.sleep(5)
        self.write("hello world")


class MainHandler2(web.RequestHandler):
    async def get(self, *args, **kwargs):
        self.write("hello world2")


if __name__ == "__main__":
    app = web.Application([
        ("/", MainHandler),
        ("/2/", MainHandler2)
    ], debug=True)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
