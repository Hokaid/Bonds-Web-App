from flask import Flask , redirect , render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager , UserMixin , login_required ,login_user, logout_user,current_user
from finanzas import *

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'
app.config['SECRET_KEY']='619619'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))
    bonos = db.relationship('Bono', backref='user', lazy=True)

class Bono(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fcalculo = db.Column(db.DateTime, default=datetime.utcnow)
    mcalculo = db.Column(db.String(20))
    tmoneda = db.Column(db.String(20))
    vnominal = db.Column(db.Float)
    vcomercial = db.Column(db.Float)
    nanos = db.Column(db.Integer)
    fpago = db.Column(db.String(50))
    dxano = db.Column(db.Integer)
    ttasa = db.Column(db.String(50))
    capi = db.Column(db.String(50))
    tinteres = db.Column(db.Float)
    tdesc = db.Column(db.Float)
    irenta = db.Column(db.Float)
    femision = db.Column(db.DateTime)
    prima = db.Column(db.Float)
    estruc = db.Column(db.Float)
    coloc = db.Column(db.Float)
    flota = db.Column(db.Float)
    cavali = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

@login_manager.user_loader
def get(id):
    return User.query.get(id)

@app.route('/',methods=['POST','GET'])
def index():
    return redirect('/login')

@app.route('/home',methods=['GET'])
@login_required
def get_home():
    return render_template('home.html')

@app.route('/login',methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/signup',methods=['GET'])
def get_signup():
    return render_template('signup.html')

@app.route('/calflujo',methods=['GET'])
def get_calflujo():
    return render_template('calflujo.html')

@app.route('/oldcalcs',methods=['GET'])
def get_oldcalcs():
    bonos = Bono.query.order_by(Bono.fcalculo).all()
    return render_template('oldcalcs.html', calculos=bonos)

@app.route('/calflujo',methods=['POST'])
def calflujo_post():
    bono = Bono(mcalculo =request.form['mcalculo'], tmoneda = request.form['tmoneda'], vnominal =float(request.form['vnominal']), 
                      vcomercial =float(request.form['vcomercial']), nanos =request.form['nanos'], fpago =request.form['fpago'], 
                      dxano = int(request.form['dxano']), ttasa =request.form['ttasa'], capi =request.form['capi'],
                      tinteres =request.form['tinteres'], tdesc =request.form['tdesc'], irenta =request.form['irenta'],
                      femision =datetime.strptime(str(request.form['femision']),'%Y-%m-%d'), prima =request.form['prima'], estruc =request.form['estruc'],
                      coloc =request.form['coloc'], flota =request.form['flota'], cavali =request.form['cavali'], user_id = current_user.id)
    db.session.add(bono)
    db.session.commit()
    parametros = []
    parametros.append(str(request.form['mcalculo']))
    parametros.append(str(request.form['tmoneda']))
    parametros.append(float(request.form['vnominal']))
    parametros.append(float(request.form['vcomercial']))
    parametros.append(int(request.form['nanos']))
    parametros.append(str(request.form['fpago']))
    parametros.append(int(request.form['dxano']))
    parametros.append(str(request.form['ttasa']))
    parametros.append(str(request.form['capi']))
    parametros.append(float(request.form['tinteres']))
    parametros.append(float(request.form['tdesc']))
    parametros.append(float(request.form['irenta']))
    parametros.append(str(request.form['femision']))
    parametros.append(float(request.form['prima']))
    parametros.append(float(request.form['estruc']))
    parametros.append(float(request.form['coloc']))
    parametros.append(float(request.form['flota']))
    parametros.append(float(request.form['cavali']))
    resultado = calbonos(parametros)
    return render_template('resultado.html', resultado=resultado)

@app.route('/login',methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if not user or not (user.password == password):
        flash("Correo electronico o contraseña incorrectos!")
        return redirect('/login')
    login_user(user)
    return redirect('/home')
    

@app.route('/signup',methods=['POST'])
def signup_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User(username=username,email=email,password=password)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/home')

@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')

if __name__=='__main__':
    app.run(debug=True)