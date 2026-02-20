from typing import Dict, Any


class Episode:
    def __init__(self, id: str, num: int) -> None:
        if not id:
            raise ValueError("Episode ID cannot be empty")

        try:
            num = int(num)
        except (TypeError, ValueError):
            raise ValueError("Episode number must be an integer")

        if num <= 0:
            raise ValueError("Episode number must be positive")

        self.id: str = id
        self.num: int = num

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Episode":
        ep_id = data.get("id")
        ep_num_raw = data.get("num")

        if ep_id is None:
            raise ValueError("Episode ID missing")
        if ep_num_raw is None:
            raise ValueError("Episode number missing")

        try:
            ep_num = int(ep_num_raw)
        except (TypeError, ValueError):
            raise ValueError("Invalid episode number")

        return cls(id=ep_id, num=ep_num)

    @classmethod
    def from_unity_dict(cls, data: Dict[str, Any]) -> "Episode":
        data["num"] = data.get("number")

        return cls.from_dict(data)

    def __repr__(self) -> str:
        return f"<Episode id={self.id} num={self.num}>"
