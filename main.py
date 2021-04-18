import sys
import http
import websockets
import asyncio
import chain
import pickle
import logging
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options
import json
server = ["127.0.0.1:8787"]

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler), (r"/chatsocket", ChatSocketHandler)]
        settings = {}
        super().__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=ChatSocketHandler.cache)


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def get_compression_options(self):
        return {}

    def open(self):
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size :]

    @classmethod
    def send_updates(cls, chat):
        logging.info("broadcast")
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        j = json.dumps(message)
        
        ChatSocketHandler.update_cache(message)
        ChatSocketHandler.send_updates(message)

if __name__ == '__main__':
    if sys.argv[1] == 'node':
        chain = chain.Chain('chain.json')
        define("port", default=8989, help="run on the given port", type=int)
        tornado.options.parse_command_line()
        app = Application()
        app.listen(options.port)
        tornado.ioloop.IOLoop.current().start()
    else:
        pass