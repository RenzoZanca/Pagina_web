// botones y secciones para validar el formulario:

// obtener los elementos del formulario:
const form = document.querySelector('form');
const boton_agregar = document.getElementById("confirmarBtn");
const seccion_confirmar = document.getElementById("confirmacion");
const seccion_form = document.getElementById("seccion_form");
const boton_volver = document.getElementById("volverBtn");

// clickear boton de agregar pedido:
boton_agregar.addEventListener("click", function() {

    if (validarFormulario()) {
        seccion_confirmar.style.display = "block";
        seccion_form.style.display = "none";        
    }
});

// clickear boton de volver:
boton_volver.addEventListener("click", function() { 
    seccion_confirmar.style.display = "none";
    seccion_form.style.display = "block";
});


// funciones auxiliares para validar el formulario:

const validarRegion = (region) => {
    if (!region) return false;
    return region != "Selecciona una Región";
};

const validarComuna = (comuna) => {
    if (!comuna) return false;
    return comuna != "Selecciona una Comuna";
};

const validarTipo = (tipo) => {
    if (!tipo) return false;
    return tipo != "Selecciona una opción"
};

const validarFecha = (fecha) => {
    if (!fecha) return false;
    var hoy = new Date();
    var fecha_ingresada = new Date(fecha);
    fecha_ingresada.setDate(fecha_ingresada.getDate() + 1);
    return fecha_ingresada >= hoy;
};

const validarFotos = (fotos) => {
    if (!fotos) return false;

    // number of fotos validation
    let lengthValid = 1 <= fotos.length && fotos.length <= 3;

    // file type validation
    let typeValid = true;

    for (const file of fotos) {
        // file.type should be "image/<foo>" or "application/pdf"
        let fileFamily = file.type.split("/")[0];
        typeValid &&= fileFamily == "image" || file.type == "application/pdf";
    }

    // return logic AND of validations.
    return lengthValid && typeValid;
};

const validarNombre = (nombre) => {
    if (!nombre) return false;
    let largo = nombre.length;
    return largo >= 3 && largo <= 80;
};

const validarEmail = (email) => {
    if (!email) return false;
    // format validation
    let re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    let formatValid = re.test(email);
    return formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
    if (!phoneNumber) return false;
    // length validation
    let lengthValid = phoneNumber.length >= 8;

    // format validation
    let re = /^[0-9]+$/;
    let formatValid = re.test(phoneNumber);

    // return logic AND of validations.
    return lengthValid && formatValid;
};

// Función para validar los campos del formulario:
function validarFormulario() {
    const region = document.querySelector('#region');
    const comuna = document.querySelector('#comuna');
    const calleNumero = document.querySelector('#calle-numero');
    const tipo = document.querySelector('#tipo');
    const cantidad = document.querySelector('#cantidad');
    const fechaDisponibilidad = document.querySelector('#fecha-disponibilidad');
    const foto = document.querySelector('#foto');
    const nombre = document.querySelector('#nombre');
    const email = document.querySelector('#email');
    const celular = document.querySelector('#celular');

    let errores = [];

    if (!validarRegion(region.value)) {
        errores.push('-Debe seleccionar una región.');
    }

    if (!validarComuna(comuna.value)) {
        errores.push('-Debe seleccionar una comuna.');
    }

    if (calleNumero.value === '') {
        errores.push('-Debe ingresar la calle y número.');
    }

    if (!validarTipo(tipo.value)) {
        errores.push('-Debe seleccionar un tipo de donación.');
    }

    if (cantidad.value === '') {
        errores.push('-Debe ingresar la cantidad.');
    }
    
    if (!validarFecha(fechaDisponibilidad.value)) {
        errores.push('-Fecha no valida (no debe ser anterior a la fecha de hoy día).');
    }

    if (!validarFotos(foto.files)) {
      errores.push('-Debe ingresar entre 1 y 3 fotos.');
    }
    
    if (!validarNombre(nombre.value)) {
        errores.push('-Nombre mal ingresado (debe tener un largo entre 3 y 80 caracteres.');
    }

    if (!validarEmail(email.value)) {
        errores.push('-Correo electronico no valido.');
    }

    if (!validatePhoneNumber(celular.value)) {
        errores.push('-Número de celular mal ingresado.');
    }
    
    if (errores.length > 0) {
        alert('Por favor, corrija los siguientes errores:\n\n' + errores.join('\n'));
        return false;
    }

    return true;
}