from typing import Optional, Dict, Any, List
from .episode import Episode


class Anime:
    def __init__(
        self, id: str, title: str, n_ep: int, episodes: Optional[List[Episode]] = None
    ):
        if not id or not title:
            raise ValueError("Invalid anime data")

        try:
            n_ep = int(n_ep)
        except (TypeError, ValueError):
            raise ValueError("Invalid episode count")

        self.id: str = id
        self.title: str = title
        self.n_ep: int = n_ep

        self.start_from_zero = False

        self.__episodes: Optional[List[Episode]] = None

        if episodes != None:
            self.episodes = episodes

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Anime":
        id = data.get("id")
        title = data.get("title")
        n_ep = data.get("n_ep")

        if not id or not title or not n_ep:
            raise ValueError("Data is missing")

        try:
            n_ep_int = int(n_ep)
        except (TypeError, ValueError):
            raise ValueError(f"{n_ep} is not a valid number of episodes")

        episodes = data.get("episodes")
        if not isinstance(episodes, list):
            return cls(id=id, title=title, n_ep=n_ep_int)

        ep_objs = []
        for ep in episodes:
            if isinstance(ep, Episode):
                ep_objs.append(ep)
            elif isinstance(ep, dict):
                ep_objs.append(Episode.from_dict(ep))
            else:
                raise ValueError(f"Invalid episode entry: {ep}")

        return cls(id=id, title=title, n_ep=n_ep_int, episodes=data.get("episodes"))

    @classmethod
    def from_unity_dict(cls, data: Dict[str, Any]) -> "Anime":
        new_data = {
            "id": f"{data.get('id', '')}{data.get('slug', '')}",
            "title": data.get("title") or data.get("title_eng", "Anime Sconosciuto"),
            "n_ep": data.get("real_episodes_count") or data.get("episodes_count") or 0,
            # image_url is unused for now but may be used in the future
            "image_url": data.get("imageurl") or data.get("imageurl_cover"),
        }

        return cls.from_dict(new_data)

    @property
    def episodes(self) -> Optional[List[Episode]]:
        return self.__episodes

    @episodes.setter
    def episodes(self, episodes: List[Episode]) -> None:
        if not isinstance(episodes, list):
            raise ValueError("Episodes must be a list")

        for e in episodes:
            if not isinstance(e, Episode):
                raise ValueError("Invalid episode format")

        if len(episodes) > self.n_ep:
            raise ValueError("Number of episodes can't exceed expected length")

        self.__episodes = sorted(episodes)
        if self.__episodes and self.__episodes[0].num == 0:
            self.start_from_zero = True

    def has_episodes(self) -> bool:
        return bool(self.__episodes)

    def __repr__(self) -> str:
        return f"<Anime id={self.title} title={self.title} n_ep={self.n_ep}>"
