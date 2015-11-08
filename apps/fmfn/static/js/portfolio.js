$(document).on('click', '.remove-favorites', function () {
    console.log('remover');
    var url = $("input[name=put-tag]").val();
    var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: url,
        type: "DELETE",
        headers: {
            'X-CSRFToken': csfrToken
        },
        success: function (response) {
            $('.remove-favorites').hide();
            var html = '<a class="add-favorites" id="add-portfolio"><i class="fa fa-heart-o"></i> agregar a favoritos </a>';
            $('#contain-portfolio').append(html);
        },
        error: function (xhr, textStatus, thrownError) {
            console.log('delete:' + xhr.statusText);
            if (xhr.statusText) {
                alert('Error');
            }
        }
    });
    console.log(url);
});

$(document).on('click', '.add-favorites', function () {
    console.log('añadir');
    var url = $("input[name=put-tag]").val();
    var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: url,
        type: "PUT",
        headers: {
            'X-CSRFToken': csfrToken
        },
        success: function (response) {
            $('.add-favorites').hide();
            var html = '<a class="remove-favorites" id="remove-portfolio"><i class="fa fa-heart"></i> eliminar de favoritos </a>';
            $('#contain-portfolio').append(html);
        },
        error: function (xhr, textStatus, thrownError) {
            console.log(xhr.statusText);
            if (xhr.statusText) {
                alert('Error');
            }
        }
    });
});