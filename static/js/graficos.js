// Esto es pa mostrar los graficos (circular), lo copié de chat gpt asi que copialo igual:

$(document).ready(function() {
    // Obtener los datos para el gráfico de donaciones desde la URL del lado del servidor
    $.ajax({
        url: "/grafico-donacion",
        method: "GET",
        success: function(response) {
            var data = response.data;

            // Opciones del gráfico
            var options = {
                series: {
                    pie: {
                        show: true
                    }
                },
                legend: {
                    show: true
                },
            };

            // Dibujar el gráfico de donaciones
            $.plot("#chart-container", data, options);
        },
    });

    // Obtener los datos para el gráfico de pedidos desde la URL del lado del servidor
    $.ajax({
        url: "/grafico-pedido",
        method: "GET",
        success: function(response) {
            var datos = response.data;

            // Opciones del gráfico
            var options = {
                series: {
                    pie: {
                        show: true
                    }
                },
                legend: {
                    show: true
                },
            };

            // Dibujar el gráfico de pedidos
            $.plot("#chart-container2", datos, options);
        },
    });
});
