from flask import Flask, render_template, request, redirect,
import json
from app import db
from app.models import User, Card

# Initialize App
login_manager = LoginManager()
app = Flask(_name_, template_folder='templates')
login_manager.init_app(app)

# Error Handler
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def home():
    return redirect('/cards')




# User not logged - Redirect to login page
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('login', code=302, Response=None)

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# User login/create account
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    # Log User In
    if request.method == 'POST' and request.form['buttonType'] == 'Login':
        user = User.query.get(request.form['username'])
        if user and (user.password == request.form['password']):
            print('Logged in User: ', request.form['username'])
            # Logout User if a user is already logged in
            if current_user:
                logout_user()
            login_user(user)
            print('Current User:', current_user)
            return redirect('myCard/' + request.form['username'], code=302, Response=None)
        elif request.form['username'] == '':
            error = 'Invalid Credentials. No username provided.'
        else:
            error = 'Invalid Credentials. Please try again.'

    # Create New Account
    elif request.method == 'POST' and request.form['buttonType'] == 'Create Account':
        user = User.query.get(request.form['newUsername'])

        # Username not taken
        if not user:
            user = User(username=request.form['newUsername'], password=request.form['newPassword'])
            if len(user.username) < 4: # invalid username length
                error = 'Please enter a username of at least 4 characters.'
            elif len(user.password) < 8: # Invalid pswd length
                error = 'Please enter a password of at least 8 characters.'
            else: # add user
                db.session.add(user)
                db.session.commit()
                print('User ', request.form['newUsername'], 'added')
                login_user(user)
                return redirect('myCard/' + request.form['newUsername'], code=302, Response=None)

        # Existing user
        else:
            error = 'User Already Exists. Please select a new Username'

    # Return login html
    return render_template('login.html', error=error)


@app.route('/cards', methods=['GET', 'POST'])
# @login_required 
# adding new cards
def myCard():
    if request.form['buttonType'] == 'Add new card':
        newCard = Card(current_user.username, request.form['inputName'], 
                        request.form['status'], request.form['content'], 
                        request.form['category'], current_user.username)
    return render_template('index.html', cards=cards)

        print('New card added')
        db.session.add(newCard)
        db.session.commit()

#deleting cards
    if request.form['buttonType'] == 'deleteCard':
        card = Cards.query.filter_by(username=current_user.username, id=request.args.get('id')).first()
        if card.username == current_user.username:
        db.session.delete(card)
        db.session.commit()

#editing cards
    if request.form['buttonType'] == 'editCard' and :
            card = Cards.query.filter_by(username=current_user.username, id=request.args.get('id')).first()
            if card.username == current_user.username:
                card = Card(card.username, request.form['inputName'], request.form['status'], request.form['content'], card.category, card.author)
                db.session.update(card)
                db.session.commit()

app.run()