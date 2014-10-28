from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("user_signup.html")


@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    print email
    password = request.form['password']
    print password

    user = model.session.query(model.User).filter_by(email=email).filter_by(password=password).first()

    if user:
        print "Login successful."           # Flash message
    else:
        print "Username/passwordS invalid"
        
    return redirect("/userlist")


@app.route('/userlist')
def user_list(): 
    user_list = model.session.query(model.User).limit(15).all()
    return render_template("user_list.html", users=user_list)

@app.route('/reviews')
def user_reviews():
    user_id = request.args.get("user")
    user = model.session.query(model.User).get(user_id) # User
    user_rating_dict = {}

    for rating in user.ratings:
        movie = model.session.query(model.Movie).get(rating.movie_id)
        movie_name = movie.movie_name
        user_rating_dict[movie_name] = rating.rating

    return render_template("user_rating.html", reviews=user_rating_dict, user=user.id)


@app.route("/newuser", methods=['POST'])
def add_new_user():

    email = request.form['email']
    password = request.form['password']
    age = request.form['age']
    zipcode = request.form['zipcode']
    gender = request.form['gender']
    occupation = request.form['occupation']

    new_user = model.User(email = email, 
                    password = password, 
                    age = age, 
                    gender = gender, 
                    occupation = occupation, 
                    zipcode = zipcode)
    
    model.session.add(new_user)                  
    model.session.commit()

    return render_template("user_signup_success.html", user = new_user)

if __name__ == "__main__":
    app.run(debug = True)
