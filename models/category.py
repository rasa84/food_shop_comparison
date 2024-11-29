from dataclasses import dataclass, field


@dataclass
class Category:
    name: str
    shop_id: int
    parent_id: int = field(default=None)
    id: int = field(default=None)
