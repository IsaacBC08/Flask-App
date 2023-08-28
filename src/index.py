from flask import Flask, render_template, request, redirect, url_for, flash
from config import config
from flask_mysqldb import MySQL
from models.ModelUser import ModelUser
from models.entities.user import User
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #print(request.form['Username'])
        #print(request.form['password'])
        user = User(0, request.form['Username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Password Invalid...")
                return render_template('auth/login.html')   
        else:
            flash("User not found...")
            return render_template('auth/login.html')       
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('registro'))

@app.route('/protected')
@login_required
def protected():
    return "<h1>Debes Iniciar seción!<h1>"

def status_401(error):
    redirect(url_for('login')) 

def status_404(error):
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/register')
def registro():
    return render_template('register.html')


@app.route('/registrar', methods=['GET','POST'])
def registrar():
    full_name = request.form['nombre']
    user_name = request.form['usuario']   
    password = request.form['contra']
    
    cursor = db.connection.cursor()
    cursor.execute(" INSERT INTO users (fullname, username, password) VALUES (%s, %s, %s) ",(full_name, user_name, password))
    db.connection.commit()
    return render_template('/auth/login.html')


if __name__ == '__main__':
    app.config.from_object(config['deve'])
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()


