
class User(db.Model):
    __tablename__ = "user_info"
    username = db.Column(db.String(100),primary_key=True)
    password = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)
    link = db.relationship('Card', backref='card_linker',lazy='dynamic')

    # Constructor
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<user_data %r>' % self.username

    def get_id(self): # Return Username to for flask login
        return self.username

    def is_authenticated(self): # return user authentification status
        return self.authenticated

    def is_active(self): # all users
        return True

    def is_anonymous(self): # anonymous users are not supported
        return False

class Card(db.Model):
   __tablename__ = "card_info"
    #: Database primary key for the row (running counter)
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100))
    inputName = db.Column(db.String(100))
    status = db.Column(db.Boolean)
    content = db.Column(db.String(1000))
    category = db.Column(db.String(100))
    author = db.Column(db.String(100))
    f_key = db.Column(db.String(100), db.ForeignKey('user_info.username'), unique=True)


    def __init__(self, username, inputName, status, content, category, author):
        self.username = username
        self.inputName = inputName
        self.status = status
        self.content = content
        self.category = category
        self.author = author 
        

    def __repr__(self):
        return '<inputName %r, status %r, content %r, category %r, author %r>' % (self.inputName, self.status, self.content,self.category, self.author) 
