import time

from tornado import web
import tornado
import tornado.ioloop


class MainHandler(web.RequestHandler):
    async def get(self, *args, **kwargs):
        self.write("hello world")


class PeopleIdHandler(web.RequestHandler):
    async def get(self, *args, **kwargs):
        self.write("用户id:{}".format(id))


urls = [
    ("/", MainHandler),
    ("/people/(\d+)/", PeopleIdHandler)
]

if __name__ == "__main__":
    app = web.Application(urls, debug=True)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
