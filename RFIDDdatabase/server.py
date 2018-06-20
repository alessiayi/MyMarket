from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json

#configuracion inicial
app = Flask(__name__)
#creadion de la db
'''
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="camilaferno",
    password="mydatabase",
    hostname="camilaferno.mysql.pythonanywhere-services.com",
    databasename="camilaferno$RFIDdatabase",
)
'''

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/camilaferno/RFIDDdatabase/RFIDdatabase.db"

db = SQLAlchemy(app)

class Productos(db.Model):
    __tablename__='Base de Datos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UID_Code = db.Column(db.String(50))
    Nombre_Producto = db.Column(db.String(50))
    Precio = db.Column(db.Integer)
    Stock = db.Column(db.Integer)

db.create_all()

@app.before_first_request
def set_database():
    #si la base de datos esta vacia
    if (Productos.query.all()==[]):
        db.session.add(Productos(id=1, UID_Code="22715318128211", Nombre_Producto="Leche",Precio=5, Stock=16))
        db.session.add(Productos(id=2, UID_Code="1501592416254", Nombre_Producto="Chocolate", Precio=3, Stock=4))
        db.session.add(Productos(id=3, UID_Code="6173235670", Nombre_Producto="Cereal", Precio=14, Stock=5))

        db.session.commit()

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

#revisar dsp
@app.route('/etc')
def algo():
    for m in db.session.query(Productos):
        return str(m.Nombre_Producto)

@app.route('/table')
def Page_for_cashier():

    inventario = Productos.query.all()

    database = "["
    for x in inventario:
        database += '{"id":' + str(x.id) + ', "UID_Code":" ' + str(x.UID_Code) + '","Nombre_Producto":"' + str(x.Nombre_Producto) + '","Precio":"' + str(x.Precio) + '","Stock":"' + str(x.Stock) + '"},'
    database = database[0:len(database) - 1]  #borras ultima coma
    database += ']'


    #database = '{"id": 1, "UID_Code": " 22715318128211", "Nombre_Producto": "Leche", "Precio": "5", "Stock": "15"}'

    return database

#app route para disminuir Stock -1
@app.route("/compras", methods=["POST"])
def postcompras():
    if request.method == "POST":
        form =request.get_json()
        nombre = form['nombre']
        query=Productos.query.filter_by(UID_Code=nombre).first() #agarra la fila del UID que escaneas
        if query != None:
            if query.Stock > 1: #para que no haya un Stock negativo
                query.Stock=query.Stock-1
                db.session.commit()
                return 'ok'
            else:
                return 'no stock'
        else:
            return 'error'
    else:
        return 'error'

##########CRUD##############

@app.route("/database", methods=['GET'])
def getProductos():

    inventario = Productos.query.all()

    accept = request.headers["Accept"]

    if accept == "application/xml":
        database = "<database>"
        for x in inventario:
            database += '<Productos><id>' + str(x.id) + '</id> <UID_Code>' + str(x.UID_Code) + '</UID_Code><Nombre_Producto>' + str(
                x.Nombre_Producto) + '</Nombre_Producto><Precio>' + str(x.Precio) + '</Precio><Stock>' + str(x.Stock) + '</Stock></Productos>'
        database += '</database>'

        return database

    elif "application/json" in accept:


        database = "["
        for x in inventario:
            database += '{"id":' + str(x.id) + ', "UID_Code":" ' + str(x.UID_Code) + '","Nombre_Producto":"' + str(
                x.Nombre_Producto) + '","Precio":"' + str(x.Precio) + '","Stock":"' + str(x.Stock) + '"},'
        database = database[0:len(database) - 1]  #borras ultima coma
        database += ']'

        return database



@app.route("/database/<id>", methods = ["GET"])
def getOneProduct(id):
    if request.method == "GET":
        x = Productos.query.get(id)
        data_json = '[{"id":'+str(x.id)+',"UID_Code":"'+str(x.UID_Code)+'","Nombre_Producto":"'+str(x.Nombre_Producto)+'","Precio":"'+str(x.Precio)+'","Stock":"'+str(x.Stock)+'"}]'
        return data_json

@app.route("/database", methods = ["POST"])
def createNewProducto():
    if request.method == "POST":
        c = json.loads(request.form["values"]) #json.loads  string->json
        new = Productos(id=int(c["id"]),UID_Code=c["UID_Code"], Nombre_Producto=c["Nombre_Producto"], Precio=int(c["Precio"]),Stock=int(c["Stock"]))
        #lo metemos a la db
        db.session.add(new)
        db.session.commit()

        return "Se ha anadido el dato"

@app.route("/database", methods = ["PUT"])
def updateDatabase():
    if request.method == "PUT":
        id = int(request.form["key"])
        x = Productos.query.get(id)
        cd = json.loads(request.form["values"])
        c = list(cd.keys())[0]

        #si el nombre de la columna es igual a tal atributo
        if c == "UID_Code":
            x.UID_Code = cd[c]
        elif c == "Nombre_Producto":
            x.Nombre_Producto = cd[c]
        elif c == "Precio":
            x.Precio = cd[c]
        elif c == "Stock":
            x.Stock = cd[c]


        db.session.commit()

        return "Put"

@app.route("/database", methods = ["DELETE"])
def deleteProductos():
    if request.method == "DELETE":
        id = int(request.form["key"])
        x = Productos.query.get(id)  # devuelve el elemento que tiene ese id

        #lo sacamos de la db
        db.session.delete(x)
        db.session.commit()

        return "Borrado"

##########CRUD##############

##########log-in#############
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard", methods=["POST"])
def dashboard():
    data = request.form
    if data['username'] == 'admin' and data['password'] == '1234':
        return render_template("crud_database.html")
    elif data['username'] == 'cajero' and data['password'] == '1234':
        return render_template("staticTable.html")
    else:
        return redirect("/login")

##########log-in#############

if __name__ == '__main__':
    app.run(debug=True)
