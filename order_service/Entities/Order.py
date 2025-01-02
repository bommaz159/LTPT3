from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Order(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
