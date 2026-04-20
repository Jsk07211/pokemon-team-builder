@dataclass
class Pokemon:
    name: str
    types: list[str]
    moves: list[str]
    item: str
    ability: str
    base_stats: dict[str, int]
    ev_spread: dict[str, int]
    is_mega: bool = False