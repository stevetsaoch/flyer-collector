from pydantic import BaseModel, Field


class Product(BaseModel):
    brand: str | None = Field(default=None)
    name: str
    package_unit: str
    package_size: float
    package_price: float
    item_unit: str
    item_size: float
    item_price: float
    previous_package_price: float | None = Field(default=None)
    discount_rate: float | None = Field(default=None)
