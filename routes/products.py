from flask import Blueprint

def create_product_blueprint():
    product = Blueprint("products", __name__)

    @product.route('/', methods=['GET'])
    def get_product():
        return None

    return product
