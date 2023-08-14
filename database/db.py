import pymysql
import json

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

with open('database/sentencias.json', 'r') as querys:
	QUERY_DICT = json.load(querys)

# -- conn ---

def get_conn():
	conn = pymysql.connect(
		db=DB_NAME,
		user=DB_USERNAME,
		passwd=DB_PASSWORD,
		host=DB_HOST,
		port=DB_PORT,
		charset=DB_CHARSET
	)
	return conn

# -- querys -

def insert_donacion(comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["insert_donacion"], (comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular))
    conn.commit()
    donacion_id = cursor.lastrowid
    return donacion_id
	
def primeras_donaciones():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["primeras_donaciones"])
	donaciones = cursor.fetchall()
	return donaciones

def segundas_donaciones():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["segundas_donaciones"])
	donaciones = cursor.fetchall()
	return donaciones

def select_donacion(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["select_donacion"], (id))
    donaciones = cursor.fetchall()
    return donaciones


def insert_pedido(comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["insert_pedido"], (comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante))
	conn.commit()

def primeros_pedidos():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["primeros_pedidos"])
	pedidos = cursor.fetchall()
	return pedidos

def segundos_pedidos():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["segundos_pedidos"])
	pedidos = cursor.fetchall()
	return pedidos

def select_pedido(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(QUERY_DICT["select_pedido"], (id))
    pedidos = cursor.fetchall()
    return pedidos
	
def insert_foto(ruta_archivo, nombre_archivo, donacion_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["insert_foto"], (ruta_archivo, nombre_archivo, donacion_id))
	conn.commit()
	
def get_foto_donacion(donacion_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_foto_donacion"], (donacion_id))
	foto = cursor.fetchall()
	return foto

def get_info_foto(foto_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_info_foto"], (foto_id))
	foto = cursor.fetchall()
	return foto

def get_comuna_id(comuna):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_comuna_id"], (comuna))
	comuna_id = cursor.fetchall()
	return comuna_id

def get_nombre_comuna(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_nombre_comuna"], (id))
	nombre_comuna = cursor.fetchall()
	return nombre_comuna

def get_nombre_region(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_nombre_region"], (id))
	nombre_region = cursor.fetchall()
	return nombre_region

# ojo que esta funcion es distinto a lo que pidieron
def pedidos(pagina):
	conn = get_conn()
	cursor = conn.cursor()
	n = (pagina - 1) * 5
	cursor.execute(QUERY_DICT["pedidos"], (n))
	pedidos = cursor.fetchall()
	return pedidos

def n_pedidos():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["n_pedidos"])
	n_pedidos = cursor.fetchall()
	return n_pedidos

# ojo que esta funcion es distinto a lo que pidieron
def donaciones(pagina):
	conn = get_conn()
	cursor = conn.cursor()
	n = (pagina - 1) * 5
	cursor.execute(QUERY_DICT["donaciones"], (n))
	donaciones = cursor.fetchall()
	return donaciones

def n_donaciones():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["n_donaciones"])
	n_donaciones = cursor.fetchall()
	return n_donaciones

# ----------------------------------------------------------------

# de aqui pa abajo es nuevo:

# las siguientes funciones retornan el numero de tipos de donaciones/pedidos

def fruta_don():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["fruta_don"])
	fruta_don = cursor.fetchall()
	return fruta_don[0][0]

def verdura_don():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["verdura_don"])
	verdura_don = cursor.fetchall()
	return verdura_don[0][0]

def otro_don():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["otro_don"])
	otro_don = cursor.fetchall()
	return otro_don[0][0]

def fruta_ped():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["fruta_ped"])
	fruta_ped = cursor.fetchall()
	return fruta_ped[0][0]

def verdura_ped():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["verdura_ped"])
	verdura_ped = cursor.fetchall()
	return verdura_ped[0][0]

def otro_ped():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["otro_ped"])
	otro_ped = cursor.fetchall()
	return otro_ped[0][0]


# funcion para obtener las coordenadas de una donacion
# no tiene que ver con sql asi que no se que hace aqui xd
def coordenadas_donacion(donacion_id):
	donacion = select_donacion(donacion_id)
	comuna_id = donacion[0][1]
	nombre_comuna = get_nombre_comuna(comuna_id)[0][0]
	with open('database/comunas-Chile.json', 'r') as comunas_file:
		comunas_data = json.load(comunas_file)
        
	comunas_dict = {comuna['name']: (float(comuna['lat']), float(comuna['lng'])) for comuna in comunas_data}
	coordenadas = comunas_dict[nombre_comuna]
	return coordenadas

def coordenadas_pedido(pedido_id):
	pedido = select_pedido(pedido_id)
	comuna_id = pedido[0][1]
	nombre_comuna = get_nombre_comuna(comuna_id)[0][0]
	with open('database/comunas-Chile.json', 'r') as comunas_file:
		comunas_data = json.load(comunas_file)
        
	comunas_dict = {comuna['name']: (float(comuna['lat']), float(comuna['lng'])) for comuna in comunas_data}
	coordenadas = comunas_dict[nombre_comuna]
	return coordenadas

