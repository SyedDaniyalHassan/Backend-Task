from pydantic import BaseModel


class ProdcutSchema(BaseModel):
    product_name: str
    initial_quantity: int
    categoty_name: str

class InventorySchema(BaseModel):
    product_id: int
    quantity_change: int

class CategorySchema(BaseModel):
    category_name: str
