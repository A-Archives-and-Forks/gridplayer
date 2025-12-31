from pathlib import Path
from typing import Generic, Iterable, List, Optional, TypeVar, Union

from gridplayer.models.video_uri import VideoURI, parse_uri

T = TypeVar("T")

IN_PATH = Union[str, Path]


class RecentList(Generic[T]):
    def __init__(self):
        self._list: List[T] = []

    def __bool__(self) -> bool:
        return bool(self._list)

    def __iter__(self) -> Iterable[T]:
        return iter(self._list)

    def __len__(self):
        return len(self._list)

    def add(self, items: List[T]) -> None:
        for item in reversed(items):
            if item in self._list:
                self._list.remove(item)
            self._list.insert(0, item)

    def truncate(self, limit: int) -> None:
        if len(self._list) > limit:
            self._list = self._list[:limit]


class RecentListVideos(RecentList[VideoURI]):
    def __init__(self, uris: Optional[List[VideoURI]] = None):
        super().__init__()

        if not uris:
            return

        for uri in uris:
            self._list.append(parse_uri(str(uri)))


class RecentListPlaylists(RecentList[Path]):
    def __init__(self, paths: Optional[List[IN_PATH]] = None):
        super().__init__()

        if not paths:
            return

        for path in paths:
            self._list.append(Path(path))
