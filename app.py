from flask import Flask
from settings import config
from api import ProcessPayment

app = Flask(__name__)
app.config.from_object(config['development'])

app.add_url_rule(
    '/process-payment',
    view_func=ProcessPayment.as_view('payment'),
    methods=['GET', 'POST'],
)

if __name__ == "__main__":
    app.run()