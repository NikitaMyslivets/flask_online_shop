from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_shop.db'
# settings with database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title

@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'
    return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)