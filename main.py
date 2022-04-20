from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, URL


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


# Creating DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cities.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(250), unique=True, nullable=False)
    country = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    favorite_place = db.Column(db.String(250), unique=True)
    ranking = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(1000), unique=True, nullable=False)


db.create_all()


class AddForm(FlaskForm):
    name = StringField('City Name', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    favorite_place = StringField('Favorite Place to visit', validators=[DataRequired()])
    ranking = StringField('The Rank', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    img_url = URLField('Image URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Add City')


class UpdateForm(FlaskForm):
    ranking = StringField('New Ranking', validators=[DataRequired()])
    favorite_place = StringField('New Favorite Place (Not Required)')
    submit = SubmitField('Update')


@app.route("/")
def home():
    all_cities = db.session.query(City).all()
    for i in range(len(all_cities)):
        # This line gives each movie a new ranking reversed from their order in all_movies
        all_cities[i].ranking = len(all_cities) - i
    db.session.commit()
    return render_template("index.html", cities=all_cities)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if request.method == "POST":
        new_city = City(
            city=request.form["name"],
            country=request.form["country"],
            favorite_place=request.form["favorite_place"],
            ranking=request.form["ranking"],
            description=request.form["description"],
            img_url=request.form["img_url"]
        )
        db.session.add(new_city)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = UpdateForm()
    city_id = request.args.get("id")
    selected_city = City.query.get(city_id)
    if form.validate_on_submit():
        selected_city.ranking = form.ranking.data
        selected_city.favorite_place = form.favorite_place.data
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, city=selected_city)


@app.route("/delete")
def delete():
    city_id = request.args.get("id")
    city_to_delete = City.query.get(city_id)
    db.session.delete(city_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
