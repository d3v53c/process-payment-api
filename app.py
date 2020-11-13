from flask_api import FlaskAPI
from settings import config
from api import ProcessPayment

app = FlaskAPI(__name__)
app.config.from_object(config['development'])

app.add_url_rule(
    '/process-payment',
    view_func=ProcessPayment.as_view('payment_request'),
    methods=['GET', 'POST'],
)