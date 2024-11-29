from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    manufacturer: str
    brand: str
    price: float
    size: float
    unit: str
    main_property: str
    category_id: int
    id: int = field(default=None)
