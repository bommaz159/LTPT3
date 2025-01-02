from Infrastructure.Database import SessionLocal
from Entities.Product import Product

class UpdateInventoryUseCase:
    def __init__(self):
        self.db = SessionLocal()

    def execute(self, product_id: str, quantity_change: int):
        product = self.db.query(Product).filter(Product.product_id == product_id).first()

        if not product:
            product = Product(product_id=product_id, quantity=max(0, quantity_change))
            self.db.add(product)
        else:
            product.quantity = max(0, product.quantity + quantity_change)

        self.db.commit()
        self.db.refresh(product)
        print(f"Updated product: {product}")
        return product
