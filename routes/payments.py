from flask import Blueprint

def create_payment_blueprint():
    payment = Blueprint("payments", __name__)

    @payment.route('/', methods=['GET'])
    def get_payment():
        return None

    return payment
