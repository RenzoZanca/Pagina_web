// Obtener los elementos select
const regionSelect = document.getElementById('region');
const comunaSelect = document.getElementById('comuna');

// Obtener la información del archivo JSON
fetch('static/region_comuna.json')
  .then(response => response.json())
  .then(data => {
  	// Llenar el elemento select de regiones con los valores del archivo JSON
    data.regiones.forEach(region => {
    	const option = document.createElement('option');
    	option.value = region.nombre;
    	option.textContent = region.nombre;
    	regionSelect.appendChild(option);
    });

    // Llenar el elemento select de comunas según la región seleccionada
    regionSelect.addEventListener('change', () => {
    	// Obtener la región seleccionada
    	const regionSeleccionada = regionSelect.value;
    	// Obtener las comunas de la región seleccionada
    	const comunas = data.regiones.find(region => region.nombre === regionSeleccionada).comunas;

    	// Limpiar el elemento select de comunas
    	comunaSelect.innerHTML = '';
    	// Agregar una opción predeterminada
    	const defaultOption = document.createElement('option');
    	defaultOption.value = '';
    	defaultOption.textContent = 'Selecciona una Comuna';
    	comunaSelect.appendChild(defaultOption);

    	// Llenar el elemento select de comunas con los valores del archivo JSON
    	comunas.forEach(comuna => {
    		const option = document.createElement('option');
    		option.value = comuna.nombre;
    		option.textContent = comuna.nombre;
    		comunaSelect.appendChild(option);
    	});
    });
  });


