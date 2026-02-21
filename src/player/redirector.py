import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from ..apis import AnimeUnity
from ..utils import REDIRECT_PORT


class RedirectServer:
    __started = False

    class RedirectHandler(BaseHTTPRequestHandler):
        anime = AnimeUnity()

        def do_GET(self):
            ep_id = urlparse(self.path).path.lstrip("/")
            if not ep_id:
                self._send_response(404, "Missing episode id")
                return

            try:
                url = self.anime.get_episode_playlist(ep_id)
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
        if cls.__started:
            return

        cls.__started = True
        threading.Thread(
            target=lambda: HTTPServer(
                ("localhost", REDIRECT_PORT), cls.RedirectHandler
            ).serve_forever(),
            daemon=True,
        ).start()
