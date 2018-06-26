from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json

# configuracion inicial
app = Flask(__name__)
# creadion de la db


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///RFIDdatabase.db"

db = SQLAlchemy(app)


class Productos(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UID_Code = db.Column(db.String(50))
    Nombre_Producto = db.Column(db.String(50))
    Precio = db.Column(db.Integer)
    Stock = db.Column(db.Integer)


class Boletas(db.Model):
    __tablename__ = 'boletas'
    id = db.Column(db.Integer, db.Sequence("boleta_id_sequence"), primary_key=True)
    numeroboleta = db.Column(db.Integer)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))


db.create_all()

if db.session.query(Boletas).count():  # si no esta vacio
    numboleta = db.session.query(Boletas).order_by(Boletas.id.desc()).first().numeroboleta
    jsonproducto = []

    for x in Boletas.query.filter_by(numeroboleta=numboleta):
        producto = Productos.query.filter_by(id=x.producto_id).first()
        jsonproducto.append({
            "UID_Code": producto.UID_Code,
            "Nombre_Producto": producto.Nombre_Producto,
            "Precio": producto.Precio,
            "Boleta": numboleta
        })

    boletalist = {"json_productos": jsonproducto,
                  "current_numboleta": numboleta}
else:
    numboleta = 0
    boletalist = {"json_productos": [],
                  "current_numboleta": numboleta}


@app.before_first_request
def set_database():
    # si la base de datos esta vacia
    if (Productos.query.all() == []):
        db.session.add(Productos(id=1, UID_Code="22715318128211",
                                 Nombre_Producto="Leche", Precio=5, Stock=16))
        db.session.add(Productos(id=2, UID_Code="1501592416254",
                                 Nombre_Producto="Chocolate", Precio=3, Stock=4))
        db.session.add(Productos(id=3, UID_Code="6173235670",
                                 Nombre_Producto="Cereal", Precio=14, Stock=5))

        db.session.commit()


@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

# revisar dsp


@app.route('/etc')
def algo():
    for m in db.session.query(Productos):
        return str(m.Nombre_Producto)


@app.route('/table')
def Page_for_cashier():

    inventario = Productos.query.all()

    database = "["
    for x in inventario:
        database += '{"id":' + str(x.id) + ', "UID_Code":" ' + str(x.UID_Code) + '","Nombre_Producto":"' + str(
            x.Nombre_Producto) + '","Precio":"' + str(x.Precio) + '","Stock":"' + str(x.Stock) + '"},'
    database = database[0:len(database) - 1]  # borras ultima coma
    database += ']'

    # database = '{"id": 1, "UID_Code": " 22715318128211", "Nombre_Producto": "Leche", "Precio": "5", "Stock": "15"}'

    return database

# app route para disminuir Stock -1
# UID_Code, Nombre_Producto, Precio


@app.route("/compras", methods=["POST"])
def postcompras():
    if request.method == "POST":
        global boletalist

        form = request.get_json()
        nombre = form['nombre']
        # agarra la fila del UID que escaneas
        query = Productos.query.filter_by(UID_Code=nombre).first()

        boletalist["json_productos"].append({
            "UID_Code": query.UID_Code,
            "Nombre_Producto": query.Nombre_Producto,
            "Precio": query.Precio,
            "Boleta": numboleta
        })

        db.session.add(Boletas(numeroboleta=numboleta, producto_id=query.id))
        db.session.commit()

        if query != None:
            if query.Stock > 0:  # para que no haya un Stock negativo
                query.Stock = query.Stock-1
                db.session.commit()
                return "ok"
            else:
                return "no stock"
    return "error"


@app.route("/compras", methods=["GET"])
def getcompras():
    return json.dumps(boletalist)


@app.route("/numboleta", methods=['GET'])
def get_currentnumboleta():
    return str(numboleta)


@app.route("/numboleta", methods=['POST'])
def set_currentnumboleta():
    global numboleta
    if request.method == "POST":
        numboleta = int(request.get_json()["numeroboleta"])
        boletalist["json_productos"] = []
        print("numboleta changed to " + str(numboleta))
        return "numboleta changed to " + str(numboleta)
    return "error"

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

    else:  # if "application/json" in accept:

        database = "["
        for x in inventario:
            database += '{"id":' + str(x.id) + ', "UID_Code":" ' + str(x.UID_Code) + '","Nombre_Producto":"' + str(
                x.Nombre_Producto) + '","Precio":"' + str(x.Precio) + '","Stock":"' + str(x.Stock) + '"},'
        database = database[0:len(database) - 1]  # borras ultima coma
        database += ']'

        return database


@app.route("/database/<id>", methods=["GET"])
def getOneProduct(id):
    if request.method == "GET":
        x = Productos.query.get(id)
        data_json = '[{"id":'+str(x.id)+',"UID_Code":"'+str(x.UID_Code)+'","Nombre_Producto":"'+str(
            x.Nombre_Producto)+'","Precio":"'+str(x.Precio)+'","Stock":"'+str(x.Stock)+'"}]'
        return data_json


@app.route("/database", methods=["POST"])
def createNewProducto():
    if request.method == "POST":
        c = json.loads(request.form["values"])  # json.loads  string->json
        new = Productos(id=int(c["id"]), UID_Code=c["UID_Code"], Nombre_Producto=c["Nombre_Producto"], Precio=int(
            c["Precio"]), Stock=int(c["Stock"]))
        # lo metemos a la db
        db.session.add(new)
        db.session.commit()

        return "Se ha anadido el dato"


@app.route("/database", methods=["PUT"])
def updateDatabase():
    if request.method == "PUT":
        id = int(request.form["key"])
        x = Productos.query.get(id)
        cd = json.loads(request.form["values"])
        c = list(cd.keys())[0]

        # si el nombre de la columna es igual a tal atributo
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


@app.route("/database", methods=["DELETE"])
def deleteProductos():
    if request.method == "DELETE":
        id = int(request.form["key"])
        x = Productos.query.get(id)  # devuelve el elemento que tiene ese id

        # lo sacamos de la db
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
        return render_template("stock.html")
    if data['username'] == 'prueba' and data['password'] == '1234':
        return render_template("carrito.html")
    else:
        return redirect("/login")

##########log-in#############


@app.route("/testcarrito")
def carro():
    return render_template("carrito.html")


if __name__ == '__main__':
    app.run(debug=True)
