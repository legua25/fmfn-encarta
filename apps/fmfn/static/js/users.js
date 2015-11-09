$(document).on('click', '#remove-user', function () {
    $('#delete-user-modal').foundation('reveal', 'open');
});

$(document).on('click', '#send-delete-user', function () {
    var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
    var user = $('#send-delete-user').data('value');
    var url = '/users/' + user + '/edit/';
    $.ajax({
        url: url,
        type: "DELETE",
        headers: {
            'X-CSRFToken': csfrToken
        },
        success: function () {
            $('#delete-user-modal').foundation('reveal', 'close');
            window.location.replace("/users/");
        },
        error: function (xhr, textStatus, thrownError) {
            if (xhr.statusText) {
                alert(thrownError);
                alert('Oops algo salio mal.\n asegurate de no estar intentando borrar tu propia cuenta');
            }
        }
    });
});

$(document).on('click', '.abort-delete-user', function () {
    $('#delete-user-modal').foundation('reveal', 'close');
});