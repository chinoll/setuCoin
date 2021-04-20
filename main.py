import sys
import http
from websocket import create_connection
import asyncio
import chain
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options
import json
from flask import Flask
import asyncio
import requests
server = ["127.0.0.1:8787"]

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler), (r"/query_all", query_all),(r"/query_lastet",query_lastet),("/update_chain",update_chain)]
        settings = {}
        super().__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class chainbase(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def get_compression_options(self):
        return {}

    def open(self):
        chainbase.waiters.add(self)

    def on_close(self):
        chainbase.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size :]

    @classmethod
    def send_updates(cls, chat):
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        pass

class query_all(chainbase):
    def open(self):
        update_chain.waiters.add(self)

    def on_close(self):
        update_chain.waiters.remove(self)

    def on_message(self, message):
        if message == "OK":
            query_all.update_cache(str(_chain))
            query_all.send_updates(str(_chain))

class query_lastet(chainbase):
    def open(self):
        update_chain.waiters.add(self)

    def on_close(self):
        update_chain.waiters.remove(self)

    def on_message(self, message):
        if message == "OK":
            d = json.dumps([_chain.chain[-1].__dict__])
            query_lastet.update_cache(d)
            query_lastet.send_updates(d)

class update_chain(chainbase):
    def open(self):
        update_chain.waiters.add(self)

    def on_close(self):
        update_chain.waiters.remove(self)

    def on_message(self, message):
        newchain = chain.Chain(chain=message)
        if _chain.replaceChain(newchain.chain):
            update_chain.update_cache(str(newchain))
            update_chain.send_updates(str(newchain))


if __name__ == '__main__':
    _chain = chain.Chain(db_path = 'chain.json')
    if sys.argv[1] == 'node':
        define("port", default=8989, help="run on the given port", type=int)
        tornado.options.parse_command_line()
        app = Application()
        app.listen(options.port)
        tornado.ioloop.IOLoop.current().start()
    elif sys.argv[1] == "server":
        app = Flask(__name__)
        @app.route('/')
        def hello():
            return "hello"
        @app.route("/blocks")
        def get_blocks():
            ws = create_connection("ws://localhost:8989/query_all")
            ws.send("OK")
            return ws.recv()
        @app.route("/mineBlock")
        def mineBlock():
            _chain.generateNextBlock("")
            ws = create_connection("ws://localhost:8989/update_chain")
            ws.send(str(_chain))
            return str(_chain)
        app.run(host='localhost',port=8383)
    elif sys.argv[1] == "run":
        while True:
            print(requests.get("http://localhost:8383/mineBlock").text)