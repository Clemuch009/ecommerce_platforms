from flask import Blueprint, jsonify

def create_order_blueprint():
    order = Blueprint('order', __name__)
    
    @order.route('', methods=['GET'])
    def get_order():
        return jsonify({'status': 'OK'})
    
    return order
