$(document).on('click', '#remove-portfolio', function () {
    console.log('probando');
    var url = $("input[name=put-tag]").val();
    var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: url,
        type: "DELETE",
        headers: {
            'X-CSRFToken': csfrToken
        },
        success: function (response) {
            $('#remove-portfolio').hide();
            var html = '<a class="add-favorites" id="add-portfolio"><i class="fa fa-heart-o"></i> add to favorites </a>';
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

$(document).on('click', '#add-portfolio', function () {
    var url = $("input[name=put-tag]").val();
    var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: url,
        type: "PUT",
        headers: {
            'X-CSRFToken': csfrToken
        },
        success: function (response) {
            $('#add-portfolio').hide();
            var html = '<a class="add-favorites" id="remove-portfolio"><i class="fa fa-heart"></i> remove from favorites </a>';
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