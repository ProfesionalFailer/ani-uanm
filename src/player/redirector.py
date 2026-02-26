import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from ..apis import AnimeUnity
from ..utils import REDIRECT_PORT


class RedirectServer:
    __server = None

    class RedirectHandler(BaseHTTPRequestHandler):
        anime = AnimeUnity()

        cache = {}
        
        def log_message(self, format, *args):
            return

        def do_GET(self):
            ep_id = urlparse(self.path).path.lstrip("/")
            if not ep_id:
                self._send_response(404, "Missing episode id")
                return

            try:
                if ep_id not in self.cache.keys():
                    self.cache[ep_id] = self.anime.get_episode_stream(ep_id)
                
                url = self.cache[ep_id]

                
                self.send_response(302)
                self.send_header("Location", url)
                self.end_headers()
            except Exception as e:
                self._send_response(500, f"Error: {e}")

        def _send_response(self, code, message):
            self.send_response(code)
            self.end_headers()
            self.wfile.write(message.encode())

    @classmethod
    def start(cls):
        if cls.__server:
            return
        
        cls.__server = HTTPServer(
            ("localhost", REDIRECT_PORT),
            cls.RedirectHandler
        )

        threading.Thread(
            target=cls.__server.serve_forever,
        ).start()

    @classmethod
    def stop(cls):
        if cls.__server:
            cls.__server.shutdown()
            cls.__server.server_close()
            cls.__server = None
