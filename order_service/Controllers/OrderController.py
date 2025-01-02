from flask import Blueprint, request, jsonify
from UseCases.CreateOrder import CreateOrderUseCase

order_controller = Blueprint('order_controller', __name__)
create_order_use_case = CreateOrderUseCase()

@order_controller.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or not quantity:
        return jsonify({"error": "Missing product_id or quantity"}), 400

    try:
        new_order = create_order_use_case.execute(product_id, quantity)
        return jsonify({
            "message": "Order created",
            "order": {
                "id": new_order.id,
                "product_id": new_order.product_id,
                "quantity": new_order.quantity
            }
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
