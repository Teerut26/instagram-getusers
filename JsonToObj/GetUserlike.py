# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = json_res_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, cast, Callable


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class Typename(Enum):
    GRAPH_USER = "GraphUser"


@dataclass
class Owner:
    typename: Typename
    id: str
    profile_pic_url: str
    username: str

    @staticmethod
    def from_dict(obj: Any) -> 'Owner':
        assert isinstance(obj, dict)
        typename = Typename(obj.get("__typename"))
        id = from_str(obj.get("id"))
        profile_pic_url = from_str(obj.get("profile_pic_url"))
        username = from_str(obj.get("username"))
        return Owner(typename, id, profile_pic_url, username)

    def to_dict(self) -> dict:
        result: dict = {}
        result["__typename"] = to_enum(Typename, self.typename)
        result["id"] = from_str(self.id)
        result["profile_pic_url"] = from_str(self.profile_pic_url)
        result["username"] = from_str(self.username)
        return result


@dataclass
class Reel:
    id: str
    expiring_at: int
    has_pride_media: bool
    seen: None
    owner: Owner
    latest_reel_media: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Reel':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        expiring_at = from_int(obj.get("expiring_at"))
        has_pride_media = from_bool(obj.get("has_pride_media"))
        seen = from_none(obj.get("seen"))
        owner = Owner.from_dict(obj.get("owner"))
        latest_reel_media = from_union([from_int, from_none], obj.get("latest_reel_media"))
        return Reel(id, expiring_at, has_pride_media, seen, owner, latest_reel_media)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["expiring_at"] = from_int(self.expiring_at)
        result["has_pride_media"] = from_bool(self.has_pride_media)
        result["seen"] = from_none(self.seen)
        result["owner"] = to_class(Owner, self.owner)
        result["latest_reel_media"] = from_union([from_int, from_none], self.latest_reel_media)
        return result


@dataclass
class Node:
    id: str
    username: str
    full_name: str
    profile_pic_url: str
    is_private: bool
    is_verified: bool
    followed_by_viewer: bool
    requested_by_viewer: bool
    reel: Reel

    @staticmethod
    def from_dict(obj: Any) -> 'Node':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        username = from_str(obj.get("username"))
        full_name = from_str(obj.get("full_name"))
        profile_pic_url = from_str(obj.get("profile_pic_url"))
        is_private = from_bool(obj.get("is_private"))
        is_verified = from_bool(obj.get("is_verified"))
        followed_by_viewer = from_bool(obj.get("followed_by_viewer"))
        requested_by_viewer = from_bool(obj.get("requested_by_viewer"))
        reel = Reel.from_dict(obj.get("reel"))
        return Node(id, username, full_name, profile_pic_url, is_private, is_verified, followed_by_viewer, requested_by_viewer, reel)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["username"] = from_str(self.username)
        result["full_name"] = from_str(self.full_name)
        result["profile_pic_url"] = from_str(self.profile_pic_url)
        result["is_private"] = from_bool(self.is_private)
        result["is_verified"] = from_bool(self.is_verified)
        result["followed_by_viewer"] = from_bool(self.followed_by_viewer)
        result["requested_by_viewer"] = from_bool(self.requested_by_viewer)
        result["reel"] = to_class(Reel, self.reel)
        return result


@dataclass
class Edge:
    node: Node

    @staticmethod
    def from_dict(obj: Any) -> 'Edge':
        assert isinstance(obj, dict)
        node = Node.from_dict(obj.get("node"))
        return Edge(node)

    def to_dict(self) -> dict:
        result: dict = {}
        result["node"] = to_class(Node, self.node)
        return result


@dataclass
class PageInfo:
    has_next_page: bool
    end_cursor: str

    @staticmethod
    def from_dict(obj: Any) -> 'PageInfo':
        assert isinstance(obj, dict)
        has_next_page = from_bool(obj.get("has_next_page"))
        end_cursor = from_str(obj.get("end_cursor"))
        return PageInfo(has_next_page, end_cursor)

    def to_dict(self) -> dict:
        result: dict = {}
        result["has_next_page"] = from_bool(self.has_next_page)
        result["end_cursor"] = from_str(self.end_cursor)
        return result


@dataclass
class EdgeLikedBy:
    count: int
    page_info: PageInfo
    edges: List[Edge]

    @staticmethod
    def from_dict(obj: Any) -> 'EdgeLikedBy':
        assert isinstance(obj, dict)
        count = from_int(obj.get("count"))
        page_info = PageInfo.from_dict(obj.get("page_info"))
        edges = from_list(Edge.from_dict, obj.get("edges"))
        return EdgeLikedBy(count, page_info, edges)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_int(self.count)
        result["page_info"] = to_class(PageInfo, self.page_info)
        result["edges"] = from_list(lambda x: to_class(Edge, x), self.edges)
        return result


@dataclass
class ShortcodeMedia:
    id: str
    shortcode: str
    edge_liked_by: EdgeLikedBy

    @staticmethod
    def from_dict(obj: Any) -> 'ShortcodeMedia':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        shortcode = from_str(obj.get("shortcode"))
        edge_liked_by = EdgeLikedBy.from_dict(obj.get("edge_liked_by"))
        return ShortcodeMedia(id, shortcode, edge_liked_by)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["shortcode"] = from_str(self.shortcode)
        result["edge_liked_by"] = to_class(EdgeLikedBy, self.edge_liked_by)
        return result


@dataclass
class Data:
    shortcode_media: ShortcodeMedia

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        shortcode_media = ShortcodeMedia.from_dict(obj.get("shortcode_media"))
        return Data(shortcode_media)

    def to_dict(self) -> dict:
        result: dict = {}
        result["shortcode_media"] = to_class(ShortcodeMedia, self.shortcode_media)
        return result


@dataclass
class JSONRes:
    data: Data
    status: str

    @staticmethod
    def from_dict(obj: Any) -> 'JSONRes':
        assert isinstance(obj, dict)
        data = Data.from_dict(obj.get("data"))
        status = from_str(obj.get("status"))
        return JSONRes(data, status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = to_class(Data, self.data)
        result["status"] = from_str(self.status)
        return result


def json_res_from_dict(s: Any) -> JSONRes:
    return JSONRes.from_dict(s)


def json_res_to_dict(x: JSONRes) -> Any:
    return to_class(JSONRes, x)
