import time

from tornado import web
import tornado
import tornado.ioloop


class MainHandler(web.RequestHandler):
    async def get(self, *args, **kwargs):
        self.write("hello world")


class PeopleIdHandler(web.RequestHandler):
    def initialize(self, name):
        self.db_name = name

    async def get(self, id, *args, **kwargs):
        self.write("用户id:{}".format(id))


class PeopleNameHandler(web.RequestHandler):
    async def get(self, name, *args, **kwargs):
        self.write("用户名字:{}".format(name))


people_db = {
    "name": "people"
}

urls = [
    tornado.web.URLSpec("/", MainHandler, name="index"),
    tornado.web.URLSpec("/people/(\d+)/", PeopleIdHandler, people_db, name="people_id"),
    tornado.web.URLSpec("/people/(\w+)/", PeopleNameHandler)
]

if __name__ == "__main__":
    app = web.Application(urls, debug=True)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
