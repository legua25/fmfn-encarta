$(document).ready(function () {
    $('#users-table').DataTable({
        language: {
            "decimal": "",
            "emptyTable": "No hay usuarios dados de alta",
            "info": "Mostrando de _START_ a _END_ de _TOTAL_ usuarios",
            "infoEmpty": "Mostrando de 0 a 0 usuarios",
            "infoFiltered": "(Filtrado de un total de _MAX_ usuarios)",
            "infoPostFix": "",
            "thousands": ",",
            "lengthMenu": "Muestrame _MENU_ elementos",
            "loadingRecords": "Cargando...",
            "processing": "Procesando...",
            "search": "Busqueda:",
            "zeroRecords": "No se encontraron coincidencias",
            "paginate": {
                "first": "Primera",
                "last": "Última",
                "next": "Siguiente",
                "previous": "Anterior"
            },
            "aria": {
                "sortAscending": ": activa para ordernar la columna de manera ascendente",
                "sortDescending": ": activa para ordernar la columna de manera descendente"
            }
        }
    });
});