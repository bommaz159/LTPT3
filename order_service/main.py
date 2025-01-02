from flask import Flask
from Controllers.OrderController import order_controller
from Infrastructure.Database import init_db

app = Flask(__name__)

init_db()

app.register_blueprint(order_controller, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
