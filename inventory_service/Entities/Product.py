from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Product(product_id={self.product_id}, quantity={self.quantity})>"
