import requests
from urllib.parse import unquote, urlencode
from html import unescape

import re

from json import loads as jsloads

from PIL import Image
from io import BytesIO

from ..utils import ANIMEUNITY_URL
from ..utils.consts import GET, POST, APP_JSON, XSRF, USER_AGENT, RGB

from ..model import Anime, Episode


class AnimeUnity:
    _instance = None  # Singleton instance

    DEFAULT_TIMEOUT = 60

    GET_ANIMES_ENDPOINT = "archivio/get-animes"
    ANIME_ENDPOINT = "anime"
    EMBED_ENDPOINT = "embed-url"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.URL = ANIMEUNITY_URL
        if self.URL is None:
            raise Exception("The program can't work without an env")

        self.session = None
        self._create_session()
        self._initialized = True  # Mark as initialized

    def _create_session(self, recreate: bool = False) -> None:
        if self.session and not recreate:
            return

        self.session = requests.Session()
        self.session.headers.update(USER_AGENT)

        self._request(GET, self.URL)  # type: ignore

        xsrf_token = self.session.cookies.get(XSRF)
        if not xsrf_token:
            raise Exception("Token XSRF non trovato")

        xsrf_token = unquote(xsrf_token)

        # Step 4: set header
        self.session.headers.update(
            {
                "x-xsrf-token": xsrf_token,
                "content-type": APP_JSON,
            }
        )

    def _request(self, method: str, url: str, **kwargs):
        if not self.session:
            raise Exception("You can't do any request without a valid session")

        kwargs.setdefault("timeout", self.DEFAULT_TIMEOUT)
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def search_animes(self, title: str, dubbed: bool = False) -> list[Anime]:
        return [
            Anime.from_unity_dict(anime)
            for anime in self._request(
                POST,
                f"{self.URL}/{self.GET_ANIMES_ENDPOINT}",
                json={"title": title, "dubbed": dubbed},
            )
            .json()
            .get("records", [])
        ]

    def load_image(
        self, url: str, max_size: tuple[int, int] = (200, 200)
    ) -> Image.Image | None:
        if not url:
            return None

        try:
            img = Image.open(BytesIO(self._request(GET, url, timeout=5).content))
            img = img.convert(RGB)

            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            return img
        except Exception as e:
            return None

    def get_episodes(self, url: str) -> list[Episode]:
        match = re.search(
            r'episodes="([^"]*)"',
            self._request(GET, f"{self.URL}/{self.ANIME_ENDPOINT}/{url}").text,
        )
        if not match:
            return []

        return sorted(
            [Episode.from_unity_dict(ep) for ep in jsloads(unescape(match.group(1)))]
        )

    def get_episode_playlist(self, episode_id: str) -> str:
        if not isinstance(episode_id, str) or not episode_id.isnumeric():
            return ""

        embed_url = self._request(
            GET, f"{self.URL}/{self.EMBED_ENDPOINT}/{episode_id}"
        ).text

        response_text = self._request(GET, embed_url).text

        params_match = re.search(
            r"params\s*:\s*(\{.*?\})\s*,", response_text, re.DOTALL
        )
        if not params_match:
            raise ValueError("Parametri non trovati")

        params = jsloads(
            re.sub(r",\s*([\}\]])", r"\1", params_match.group(1)).replace("'", '"')
        )

        url_match = re.search(r'url\s*:\s*[\'"]([^\'"]+)[\'"]', response_text)
        if not url_match:
            raise ValueError("Url non trovato")

        return f"{url_match.group(1)}?" + urlencode(
            {
                "token": params.get("token"),
                "expires": params.get("expires"),
                "h": "1",
            }
        )
