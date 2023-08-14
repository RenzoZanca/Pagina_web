import datetime
import re
import os

# validaciones de los formularios:

def validarRegion(region):
    if not region:
        return False
    return region != "Selecciona una Región"

def validarComuna(comuna):
    if not comuna:
        return False
    return comuna != "Selecciona una Comuna"

def validarTipo(tipo):
    if not tipo:
        return False
    return tipo != "Selecciona una opción"

def validarFecha(fecha):
    if not fecha:
        return False
    hoy = datetime.datetime.now()
    fecha_ingresada = datetime.datetime.fromisoformat(fecha)
    fecha_ingresada = fecha_ingresada + datetime.timedelta(days=1)
    return fecha_ingresada >= hoy

def validarFotos(fotos):
    if len(fotos) < 1 or len(fotos) > 3:
        return False
    
    for foto in fotos:
        if not validate_img(foto):
            return False
    
    return True


def validate_img(img):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}
    max_size = 16 * 1024 * 1024  # 16MB

    # check if a file was submitted
    if img is None:
        return False

    # check if the browser submitted an empty file
    if img.filename == "":
        return False
    
    # check file extension
    _, ext = os.path.splitext(img.filename)
    if ext[1:].lower() not in ALLOWED_EXTENSIONS:
        return False

    # check mimetype
    if img.mimetype not in ALLOWED_MIMETYPES:
        return False

    # check file size
    img.seek(0, os.SEEK_END)
    if img.tell() > max_size:
        return False
    img.seek(0)
    
    return True


def validarNombre(nombre):
    if not nombre:
        return False
    largo = len(nombre)
    return 3 <= largo <= 80

def validarCantidad(cantidad):
    if not cantidad:
        return False
    return True

def validarEmail(email):
    if not email:
        return False
    # validación de formato
    regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    formatValid = re.match(regex, email)
    return formatValid is not None


def validatePhoneNumber(phoneNumber):
    if not phoneNumber:
        return False
    # validación de longitud
    lengthValid = len(phoneNumber) >= 8

    # validación de formato
    regex = r'^[0-9]+$'
    formatValid = re.match(regex, phoneNumber)

    # lógica de retorno usando AND de las validaciones.
    return lengthValid and formatValid is not None

def validar_desc(desc):
    if not desc:
        return False
    return len(desc) < 251



def validar_donacion(region, comuna, calle_numero, tipo, cantidad, fecha_disponibilidad, fotos, nombre, email, celular):
    val_region = validarRegion(region)
    val_comuna = validarComuna(comuna)
    val_calle_numero = validarNombre(calle_numero)
    val_tipo = validarTipo(tipo)
    val_cantidad = validarCantidad(cantidad)
    val_fecha_disponibilidad = validarFecha(fecha_disponibilidad)
    val_fotos = validarFotos(fotos)
    val_nombre = validarNombre(nombre)
    val_email = validarEmail(email)
    val_celular = validatePhoneNumber(celular)
    return val_region and val_comuna and val_calle_numero and val_tipo and val_cantidad and val_fecha_disponibilidad and val_fotos and val_nombre and val_email and val_celular  


def validar_pedido(region, comuna, tipo, desc, cantidad, nombre, email, celular):
    val_region = validarRegion(region)
    val_comuna = validarComuna(comuna)
    val_tipo = validarTipo(tipo)
    val_desc = validar_desc(desc)
    val_cantidad = validarNombre(cantidad)
    val_nombre = validarNombre(nombre)
    val_email = validarEmail(email)
    val_celular = validatePhoneNumber(celular)
    return val_region and val_comuna and val_tipo and val_cantidad and val_desc and val_nombre and val_email and val_celular  