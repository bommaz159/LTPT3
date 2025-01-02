from Entities.Order import Order
from Infrastructure.Database import SessionLocal
from Infrastructure.MessageBus import MessageBus
import requests
import logging


class CreateOrderUseCase:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)
        self.db = SessionLocal()

    def execute(self, product_id: str, quantity: int):
        inventory_url = f"http://inventory_service:8001/api/inventory/{product_id}"
        self.logger.debug(f"Calling Inventory Service at {inventory_url}")

        response = requests.get(inventory_url)
        self.logger.debug(f"Response status: {response.status_code}, Response body: {response.text}")

        if response.status_code == 404:
            raise ValueError("Product not found in inventory")

        try:
            inventory_data = response.json()
        except ValueError as e:
            self.logger.error("Invalid JSON response from Inventory Service")
            raise ValueError("Invalid response from Inventory Service")

        available_quantity = inventory_data.get("quantity", 0)
        if quantity > available_quantity:
            raise ValueError("Khong du so luong ton kho")

        # Tạo đơn hàng mới
        new_order = Order(product_id=product_id, quantity=quantity)
        self.db.add(new_order)
        self.db.commit()  # Lưu thay đổi vào cơ sở dữ liệu
        self.db.refresh(new_order)  # Cập nhật `id` tự động từ cơ sở dữ liệu

        # Gửi thông báo tới RabbitMQ
        message_bus = MessageBus()
        message_bus.publish({
            "id": new_order.id,
            "product_id": product_id,
            "quantity": quantity
        })

        return new_order
