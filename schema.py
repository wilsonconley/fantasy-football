import enum
import typing as t
from dataclasses import dataclass

Website: t.TypeAlias = str


class Position(enum.Enum):
    QB = enum.auto()
    RB = enum.auto()
    WR = enum.auto()
    TE = enum.auto()
    K = enum.auto()
    DST = enum.auto()


@dataclass(frozen=True)
class Ranking:
    website: Website
    rank: int
    proj_pts: float


@dataclass(frozen=True)
class Player:
    name: str
    pos: Position


@dataclass(frozen=True)
class DBItem:
    # TODO: pydantic model?

    name: str
    pos: str
    rankings: t.Mapping[str, t.Any]
