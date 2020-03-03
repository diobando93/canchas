from flask import Flask, render_template, request, make_response, request, send_from_directory, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os

UPLOAD_FOLDER = os.path.abspath("guias/")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


ENV = 'dev'

if ENV == 'dev' :
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://sammy:hola@localhost/sammy'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://jxltfzavclcqeo:b5fc4c357bda6fb9b1b08fd2a096767262243f2da408f877ed0b910ddabf744f@ec2-54-235-163-246.compute-1.amazonaws.com:5432/ddg9qoeqjojuba'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Text(), primary_key=True)
    producto = db.Column(db.Text())
    ingreso = db.Column(db.Float)
    egreso = db.Column(db.Float)
    fisico = db.Column(db.Float)
    costcom = db.Column(db.Float)

    def __init__(self, id, producto, ingreso, egreso, fisico, costcom):
        self.id = id
        self.producto = producto
        self.ingreso = ingreso
        self.egreso = egreso
        self.fisico = fisico
        self.costcom = costcom


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        if request.form['Submit'] == 'Guia':
            return redirect(url_for('uploader'))
        if request.form['Submit'] == 'Consulta de Productos':
            return redirect(url_for('query'))
        if request.form['Submit'] == 'Ingreso de Productos':
            return redirect(url_for('entry'))
        if request.form['Submit'] == 'Egreso de Productos':
            return redirect(url_for('out'))

@app.route('/uploader', methods=['POST', 'GET'])
def uploader():
    if request.method == 'POST':
        if request.form['Submit'] == 'aceptar':
            f = request.files["ourfile"]
            filename = f.filename
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            print( 'your file has been uploaded' + filename)
    return render_template('upload.html')
    #return 'holi'

@app.route('/query', methods=['POST', 'GET'])
def query():
    if request.method == 'POST':
        if request.form['Submit'] == 'Consultar':
            customer = request.form['customer']
            aux3 = db.session.query(Productos).filter(Productos.producto == customer).first()
            aux3 = str(aux3.fisico)
            return aux3
    return render_template('query.html')

@app.route('/entry', methods=['POST', 'GET'])
def entry():
    if request.method == 'POST':
        if request.form['Submit'] == 'Ingreso':
            producto = request.form['producto']
            print(producto)
    #admin = User.query.filter_by(username='admin').update(dict(email='my_new_email@example.com')))
    #db.session.commit()
    return render_template('ingreso.html')

@app.route('/out', methods=['POST', 'GET'])
def out():
    return render_template('egreso.html')

if __name__ == '__main__':
    app.run()
