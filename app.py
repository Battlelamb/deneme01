from flask import Flask, render_template, redirect, url_for
from flask.globals import request
from wtforms import Form, StringField, validators
from flask_mongoengine import MongoEngine
from uuid import uuid4

app = Flask(__name__)

# test
# test1

# Veritabanı bağlantısı
app.config['MONGODB_SETTINGS'] = {
    "db": "todo_app_data",
    "host": "localhost",  # 196.15.16.287
    'port': 27017
}

db = MongoEngine()
db.init_app(app)


class User(db.Document):
    _id = db.StringField()
    uuid = db.StringField()
    firstname = db.StringField()
    lastname = db.StringField()
    adres = db.StringField()

    def to_json(self):
        return {
            "_id": self._id,
            "uuid": self.uuid,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "adres": self.adres
        }


class RegisterForm(Form):
    firstname = StringField(u'First Name', validators=[
                            validators.input_required()])
    lastname = StringField(u"Last Name", validators=[validators.optional()])
    adres = StringField(u'Adres', validators=[validators.optional()])


@app.route("/")  # => http://127.0.0.1:5000/ = https://www.hepsiburada.com/
def index():

    number = 10
    sayilar = [1, 2, 3, 4, 5]
    isim = "Ömer"

    return render_template("index.html", number=number, sayilar=sayilar, isim=isim)


# => http://127.0.0.1:5000/about = https://www.hepsiburada.com/about
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/article/<string:id>")
def article(id):
    return "Article Id = " + id
    # UID => unique identifier => Eşsiz tanımlama

# Register Page Start


@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm(request.form)

    if request.method == "POST":  # Sunucuya Gönderme İşlemi

        firstname = form.firstname.data  # data == text == değeri
        uuid = uuid4().hex
        lastname = form.lastname.data
        adres = form.adres.data

        # print(form.firstname.data)
        # print(form.lastname.data)

        user = User(firstname=firstname, lastname=lastname,
                    adres=adres, uuid=uuid)
        user.save()

        return redirect(url_for("register"))
    else:
        users = list(User.objects)
        # for x in users:
        #     print(x.firstname)
        return render_template("register.html", form=form, users=users)


@app.route("/delete/<id>", methods=["GET"])
def delete_user(id):
    try:
        print(User)
        print("ID: ", id)
        # user = User.objects(uuid=str(id)).first()
        user = User.objects(uuid=str(id)).delete()
        # user.delete()
        print(user)
        # users = list(User.objects)
        # for x in users:
        #     print(x.firstname)
        # try:
        #     user.delete()
        # except Exception as ex:
        #     print("****", ex, "****")
        if not user:
            print("yok artık")
        else:
            user.delete()
    except Exception as ex:
        print("((((", ex, "))))")

    return redirect(url_for("register"))

# Register Page End

# @app.route("/layout") # => http://127.0.0.1:5000/layout
# def layout():
#     return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
