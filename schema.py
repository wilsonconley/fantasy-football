import enum
import typing as t
from dataclasses import dataclass, field
from decimal import Decimal

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
class DBRanking:
    rank: int
    proj_pts: Decimal


@dataclass
class DBSchema:
    name: str
    pos: str
    rankings: t.Mapping[str, DBRanking]
    avg_rank: Decimal = field(init=False)
    avg_proj_pts: Decimal = field(init=False)


class DBItem(DBSchema):
    name: str
    pos: str
    rankings: t.Mapping[str, DBRanking]

    @property
    def avg_rank(self) -> Decimal:
        ranks = [x.rank for x in self.rankings.values()]
        avg = sum(ranks) / len(ranks)
        return Decimal(str(avg))

    @property
    def avg_proj_pts(self) -> Decimal:
        proj_pts = [x.proj_pts for x in self.rankings.values()]
        avg = sum(proj_pts) / len(proj_pts)
        return Decimal(str(avg))
