from flask import Blueprint, request, jsonify
from Infrastructure.Database import SessionLocal
from Entities.Product import Product

inventory_controller = Blueprint('inventory_controller', __name__)

@inventory_controller.route('/inventory', methods=['POST'])
def add_or_update_product():
 
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or quantity is None:
        return jsonify({"error": "Missing product_id or quantity"}), 400
    if quantity < 0:
        return jsonify({"error": "Quantity must be positive"}), 400

    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if product:
            product.quantity += quantity
        else:
            product = Product(product_id=product_id, quantity=quantity)
            db.add(product)

        db.commit()
        db.refresh(product)

        return jsonify({
            "message": "Sản phẩm đã được thêm vào kho",
            "product": {
                "product_id": product.product_id,
                "quantity": product.quantity
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@inventory_controller.route('/inventory/<product_id>', methods=['GET'])
def get_inventory_by_product(product_id):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            return jsonify({"error": "Không tìm thấy product"}), 404

        return jsonify({
            "product_id": product.product_id,
            "quantity": product.quantity
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@inventory_controller.route('/inventory', methods=['GET'])
def get_inventory():
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        result = [{"product_id": product.product_id, "quantity": product.quantity} for product in products]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

