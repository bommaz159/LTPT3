from flask import Flask
from Controllers.InventoryController import inventory_controller
from Infrastructure.Database import init_db
from Infrastructure.MessageBus import MessageBus
import threading

app = Flask(__name__)

init_db()

app.register_blueprint(inventory_controller, url_prefix="/api")

def run_message_bus():
    message_bus = MessageBus()
    message_bus.start_listening()

if __name__ == '__main__':
    threading.Thread(target=run_message_bus, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=8001)
