from dataclasses import dataclass, field
from uuid import uuid4


class BurgerData:
    BUN = "Флюоресцентная булка R2-D3"
    SAUCE = "Соус фирменный Space Sauce"
    INGREDIENTS = (BUN, SAUCE)


@dataclass(frozen=True)
class User:
    email: str
    password: str = field(repr=False)
    name: str

    @classmethod
    def unique(cls):
        suffix = uuid4().hex
        return cls(f"ui_{suffix}@example.com", f"UiPassword_{suffix}", f"UI {suffix[:8]}")

    def registration_data(self):
        return {"email": self.email, "password": self.password, "name": self.name}


@dataclass(frozen=True)
class Order:
    number: int
    ingredients: tuple = BurgerData.INGREDIENTS
