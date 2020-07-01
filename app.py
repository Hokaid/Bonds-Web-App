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


def detflujo(resultshow, infla):
    resultado = calbonos(str(resultshow.mcalculo), infla, float(resultshow.ianual)/100, float(resultshow.vnominal), float(resultshow.vcomercial), 
                         int(resultshow.nanos), str(resultshow.fpago), int(resultshow.dxano), str(resultshow.ttasa), 
                         str(resultshow.capi), str(resultshow.pgracia), float(resultshow.tinteres)/100, float(resultshow.tdesc)/100,
                         float(resultshow.irenta)/100, resultshow.femision.strftime('%d/%m/%Y'), float(resultshow.prima)/100, 
                         float(resultshow.estruc)/100, float(resultshow.coloc)/100, float(resultshow.flota)/100, float(resultshow.cavali)/100)
    resultado = list(resultado)
    for i in range(15):
        if resultado[i] < 0:
            resultado[i] = "(" + str(-1*resultado[i]) + ")"
    for renta in resultado[15]:
        for i in range(2, 4):
            if renta[i] != "":
                renta[i] = round(renta[i], 2)
        for i in range(5, 15):
            if renta[i] != "":
                renta[i] = round(renta[i], 2)
                if renta[i] < 0:
                    renta[i] = "(" + str(-1*renta[i]) + ")"
    return resultado

def detmon(bono):
    mon = ""
    if bono.tmoneda == "Sol": mon = "S/"
    elif bono.tmoneda == "Dolar": mon = "US$"
    elif bono.tmoneda == "Euro": mon = "€"
    return mon

def checkempty(request):
    if ((request.form['mcalculo'] == "") or (request.form['tmoneda'] == "") or 
       (request.form['vnominal'] == '') or (request.form['vcomercial'] == '') or
       (request.form['nanos'] == '') or (request.form['fpago'] == '') or
       (request.form['dxano'] == '') or (request.form['ttasa'] == '') or
       (request.form['capi'] == '') or (request.form['tinteres'] == '') or
       (request.form['tdesc'] == '') or (request.form['irenta'] == '') or (request.form['prima'] == '') or 
       (request.form['estruc'] == '') or (request.form['coloc'] == '') or 
       (request.form['flota'] == '') or (request.form['cavali'] == '')): return False
    if (current_user.rol == "Emisor"):
        if (request.form['ianual'] == ''): return False
    return True

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(200))
    rol = db.Column(db.String(200))
    password = db.Column(db.String(200))
    firstname = db.Column(db.String(200))
    lastname = db.Column(db.String(200))
    email = db.Column(db.String(200))
    birthday = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    companyname = db.Column(db.String(200),nullable=True)
    companyphone = db.Column(db.String(200),nullable=True)
    bonos = db.relationship('Bono', backref='user', lazy=True)

class Bono(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fcalculo = db.Column(db.DateTime, default=datetime.utcnow)
    mcalculo = db.Column(db.String(20))
    ianual = db.Column(db.Float)
    tmoneda = db.Column(db.String(20))
    vnominal = db.Column(db.Float)
    vcomercial = db.Column(db.Float)
    nanos = db.Column(db.Integer)
    fpago = db.Column(db.String(50))
    dxano = db.Column(db.Integer)
    ttasa = db.Column(db.String(50))
    capi = db.Column(db.String(50))
    pgracia = db.Column(db.String(1000))
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

@app.route('/configbon/<int:id>',methods=['GET'])
def get_configbon(id):
    bono = Bono.query.get_or_404(id)
    return render_template('calflujo.html',bono=bono)

@app.route('/calflujo',methods=['GET'])
def get_calflujo():
    return render_template('calflujo.html')

@app.route('/oldcalcs',methods=['GET'])
def get_oldcalcs():
    bonos = Bono.query.filter_by(user_id = current_user.id).order_by(Bono.fcalculo).all()
    return render_template('oldcalcs.html', calculos=bonos, confiop = False)

@app.route('/emitbons',methods=['GET'])
def get_emitbons():
    emisores = User.query.filter_by(rol="Emisor").all()
    totalbonos = []
    for emi in emisores:
        bonos = Bono.query.filter_by(user_id = emi.id).order_by(Bono.fcalculo).all()
        totalbonos = totalbonos + bonos
    return render_template('oldcalcs.html', calculos=totalbonos, confiop=True)

@app.route('/calflujo',methods=['POST'])
def calflujo_post():
    if not (checkempty(request)):
        flash("No debes dejar campos vacios!", "message")
        return redirect('/calflujo')
    bono = Bono(mcalculo =request.form['mcalculo'], ianual=request.form['ianual'], tmoneda = request.form['tmoneda'], vnominal =request.form['vnominal'], 
                      vcomercial =request.form['vcomercial'], nanos =request.form['nanos'], fpago =request.form['fpago'], 
                      dxano = request.form['dxano'], ttasa =request.form['ttasa'], capi =request.form['capi'], pgracia = request.form['pgracia'],
                      tinteres =request.form['tinteres'], tdesc =request.form['tdesc'], irenta =request.form['irenta'],
                      femision =datetime.strptime(request.form['femision'], '%Y-%m-%d'), prima =request.form['prima'], estruc =request.form['estruc'],
                      coloc =request.form['coloc'], flota =request.form['flota'], cavali =request.form['cavali'], user_id = current_user.id)
    db.session.add(bono)
    db.session.commit()
    return render_template('resultado.html', resultado=detflujo(bono, False), bono=bono, mon=detmon(bono), inflaop=True)

@app.route('/calfluinf/<int:id>')
def calflujo_inf(id):
    bono = Bono.query.get_or_404(id)
    return render_template('resultado.html', resultado=detflujo(bono, True), bono=bono, mon=detmon(bono), inflaop=False)

@app.route('/resultado/<int:id>')
def ver_resultado(id):
    resultshow = Bono.query.get_or_404(id)
    return render_template('resultado.html', resultado=detflujo(resultshow, False), bono=resultshow, mon=detmon(resultshow), inflaop=True)

@app.route('/delete/<int:id>')
def delete(id):
    resultdel = Bono.query.get_or_404(id)
    try:
        db.session.delete(resultdel)
        db.session.commit()
        return redirect('/oldcalcs')
    except:
        return 'There was a problem deleting that task'

@app.route('/login',methods=['POST'])
def login_post():
    name = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=name).first()
    if not user or not (user.password == password):
        flash("Nombre de usuario o contraseña incorrectos!", "message")
        return redirect('/login')
    login_user(user)
    return redirect('/home')

@app.route('/signup',methods=['POST'])
def signup_post():
    username = request.form['username']
    rol = request.form['rol']
    email = request.form['email']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    birthday = request.form['birthday']
    phone = request.form['phone']
    companyname = request.form['companyname']
    companyphone = request.form['companyphone']
    password = request.form['password']
    confirm = request.form['confirm']
    if username == "" or email == "" or password == "" or firstname == "" or lastname == "" or birthday == "" or phone == "" or confirm== "" or rol=="":
        flash("Faltan datos!", "message")
        return redirect('/signup')

    if (password != confirm):
        flash("Contraseña no es igual", "message")
        return redirect('/signup')

    users = User.query.all()
    for u in users:
        if (u.username == username):
            flash("Ya existe un usuario con ese nombre!", "message")
            return redirect('/signup')

    user = User(username=username,rol=rol,email=email,password=password,firstname=firstname,lastname=lastname,birthday=birthday,phone=phone,companyname=companyname,companyphone=companyphone)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/login')
   
@app.route('/xcontra',methods=['GET'])
def get_xcontra():
    return render_template('xcontra.html')

@app.route('/xcontra',methods=['POST'])
def cambiar_contraseña():
    oldpassword = request.form['oldpassword']
    newpassword = request.form['newpassword']
    newconfirm = request.form['newconfirm']
    if current_user.password != oldpassword:
        flash("La contraseña actual ingresada es incorrecta!", "message")
        return redirect('/xcontra')
    elif newpassword == "":
        flash("No ha ingresado una nueva contraseña!", "message")
        return redirect('/xcontra')
    elif (newpassword != newconfirm):
        flash("No es la misma contraseña!", "message")
        return redirect('/xcontra')
    user = User.query.get_or_404(current_user.id)
    user.password = newpassword
    try:
        db.session.commit()
        flash("Contraseña cambiada!")
        return redirect('/xcontra')
    except:
        return 'There was an issue updating your task'

@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')

if __name__=='__main__':
    app.run(debug=True)