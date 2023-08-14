from flask import Flask, render_template, request, url_for, jsonify # nuevo
from flask_cors import cross_origin
from utils.validate import *
from database.db import *
from werkzeug.utils import secure_filename
import os
import hashlib
import filetype
from math import ceil

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# rutas:

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/agregar-donacion", methods=["GET", "POST"])
def agregar_donacion():
    error = None
    confirmacion = None
    if request.method == "POST":
        region = request.form["region"]
        comuna = request.form["comuna"]
        calle_numero = request.form["calle-numero"]
        tipo = request.form["tipo"]
        cantidad = request.form["cantidad"]
        fecha_disponibilidad = request.form["fecha-disponibilidad"]
        descripcion = request.form["descripcion"]
        condiciones_retirar = request.form["condiciones"]
        fotos = []
        fotos.append(request.files.get("foto"))
        foto2 = request.files.get("foto2")
        foto3 = request.files.get("foto3")
        if foto2:
            fotos.append(foto2)
        if foto3:
            fotos.append(foto3)
        nombre = request.form["nombre"]
        email = request.form["email"]
        celular = request.form["celular"]

        if validar_donacion(region, comuna, calle_numero, tipo, cantidad, fecha_disponibilidad, fotos, nombre, email, celular):

            comuna_id = get_comuna_id(comuna)
            donacion_id = insert_donacion(comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular)
            confirmacion = "Donación realizada con éxito"

            # guardar fotos:
            for foto in fotos:
                # 1. generate random name for img
                _filename = hashlib.sha256(
                    secure_filename(foto.filename).encode("utf-8")
                    ).hexdigest()
                _extension = filetype.guess(foto).extension
                img_filename = f"{_filename}.{_extension}"
                # 2. save img as a file
                foto.save(os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"], img_filename).replace('\\', '/'))

                # Agregar a la base de datos:
                insert_foto(url_for('static', filename=img_filename), img_filename, donacion_id)

            return render_template("agregar-donacion.html", confirmacion=confirmacion)
        
        else:
            error = "Error en los datos ingresados. Verifique que sus imagenes sean de tamaño menor a 16 MB."
            return render_template("agregar-donacion.html", error=error)
        
    elif request.method == "GET":
        return render_template("agregar-donacion.html")

          
@app.route("/agregar-pedido", methods=["GET", "POST"])
def agregar_pedido():
    error = None
    confirmacion = None
    if request.method == "POST":
        region = request.form["region"]
        comuna = request.form["comuna"]
        tipo = request.form["tipo"]
        desc = request.form["descripcion"]
        cantidad = request.form["cantidad"]
        nombre = request.form["nombre"]
        email = request.form["email"]
        celular = request.form["celular"]
        if validar_pedido(region, comuna, tipo, desc, cantidad, nombre, email, celular):
             # agregar a la base de datos:
             comuna_id = get_comuna_id(comuna)
             insert_pedido(comuna_id, tipo, desc, cantidad, nombre, email, celular)
             confirmacion = "Pedido realizado con éxito"
             return render_template("agregar-pedido.html", confirmacion=confirmacion)
        else:
            error = "Error en los datos ingresados"
            return render_template("agregar-pedido.html", error=error)
    elif request.method == "GET":
        return render_template("agregar-pedido.html")


@app.route("/ver-donaciones/<int:pagina>")
def ver_donaciones(pagina):
    p = ceil(n_donaciones()[0][0] / 5)
    dona = donaciones(pagina)
    comunas = []
    fotos = []
    for donacion in dona:
        comuna_id = donacion[1]
        comuna = get_nombre_comuna(comuna_id)
        comunas.append(comuna)
        donacion_id = donacion[0]
        fotos.append(get_foto_donacion(donacion_id))

    return render_template("ver-donaciones.html", donaciones=dona, comunas=comunas, fotos=fotos, p=p)

@app.route("/ver-pedidos/<int:pagina>")
def ver_pedidos(pagina):
    # obtener los datos:
    p = ceil(n_pedidos()[0][0] / 5)
    pedi2 = pedidos(pagina)
    comunas = []
    for pedido in pedi2:
        comuna_id = pedido[1]
        comuna = get_nombre_comuna(comuna_id)
        comunas.append(comuna)

    return render_template("ver-pedidos.html", pedidos=pedi2, comunas=comunas, p=p)


@app.route("/informacion-donacion/<int:donacion_id>/<int:foto_id1>/<int:foto_id2>/<int:foto_id3>")
def informacion_donacion(donacion_id, foto_id1, foto_id2, foto_id3):
    donacion = select_donacion(donacion_id)
    comuna_id = donacion[0][1]
    comuna = get_nombre_comuna(comuna_id)
    region = get_nombre_region(comuna_id)
    # obtener fotos:
    foto_id = [foto_id1, foto_id2, foto_id3]
    nombres_fotos = []
    for id in foto_id:
        if id == 0:
            continue
        foto = get_info_foto(id)
        nombre_foto = foto[0][2]
        nombres_fotos.append(nombre_foto)

    return render_template("informacion-donacion.html", donacion=donacion, comuna=comuna, region=region, nombres_fotos=nombres_fotos)


@app.route("/informacion-pedido/<int:pedido_id>")
def informacion_pedido(pedido_id):
    pedido = select_pedido(pedido_id)
    # obtener comuna y region:
    comuna_id = pedido[0][1]
    comuna = get_nombre_comuna(comuna_id)
    region = get_nombre_region(comuna_id)
    return render_template("informacion-pedido.html", pedido=pedido, comuna=comuna, region=region)

# ----------------------------------------------------------------

# De aqui para abajo es nuevo

@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")


@app.route('/grafico-donacion', methods=['GET'])
def grafico_donacion():
    # obtenemos los numeros de cada tipo de donacion
    fruta = fruta_don()
    verdura = verdura_don()
    otro = otro_don()
    data = [
        {'label': 'Fruta', 'data': fruta},
        {'label': 'Verdura', 'data': verdura},
        {'label': 'Otros', 'data': otro}
    ]
    return jsonify({'data': data})


@app.route('/grafico-pedido', methods=['GET'])
def grafico_pedido():
    # obtenemos los numeros de cada tipo de pedido
    fruta = fruta_ped()
    verdura = verdura_ped()
    otro = otro_ped()
    data = [
        {'label': 'Fruta', 'data': fruta},
        {'label': 'Verdura', 'data': verdura},
        {'label': 'Otros', 'data': otro}
    ]
    return jsonify({'data': data})


@app.route('/mapa-donaciones', methods=['GET'])
@cross_origin(origin='localhost', supports_credentials=True) # creo que esto no es necesario
def mapa_donaciones():
    # obtener donaciones:
    dons = donaciones(1)
    markers = []
    for don in dons:
        cor = coordenadas_donacion(don[0])
        # crear marcadores:
        marker = {
            'coordinates': [cor[0], cor[1]],
            'items': [
                {'label': 'ID', 'value': don[0]},
                {'label': 'Dirección', 'value': don[2]},
                {'label': 'Tipo', 'value': don[3]},
                {'label': 'Cantidad', 'value': don[4]},
                {'label': 'Fecha disponibilidad', 'value': don[5].strftime('%Y-%m-%d')},
                {'label': 'Email donante', 'value': don[9]}
            ]
        }
        markers.append(marker)

    return jsonify(markers)

@app.route('/mapa-pedidos', methods=['GET'])
@cross_origin(origin='localhost', supports_credentials=True)
def mapa_pedidos():
    # obtener pedidos
    peds = pedidos(1)
    markers = []
    for ped in peds:
        cor = coordenadas_pedido(ped[0])
        # crear marcadores
        marker = {
            'coordinates': [cor[0] + 0.004, cor[1] + 0.005],
            'items': [
                {'label': 'ID', 'value': ped[0]},
                {'label': 'Tipo', 'value': ped[2]},
                {'label': 'Cantidad', 'value': ped[4]},
                {'label': 'Email solicitante', 'value': ped[6]}
            ]
        }
        markers.append(marker)

    return jsonify(markers)


if __name__ == "__main__":
    app.run(debug=True)