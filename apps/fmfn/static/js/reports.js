$(document).on('click', '#insert-report', function () {
    var description = $('#report-content').val();
    var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
    var material = $("input[name=report-material-id]").val();
    var url = '/manage/reports/create/' + material + '/';
    $.ajax({
        url: url,
        type: "POST",
        data: {
            csrfmiddlewaretoken: csfrToken,
            description: description
        },
        success: function (response) {
            $('#report-content').val('');
            $('#success-report').foundation('reveal', 'open');
            $('#report-material').foundation('reveal', 'close');
        },
        error: function (xhr, textStatus, thrownError) {
            alert('Error:' + xhr.statusText);
        }
    });
});

$(document).on('click', '#show-report-material', function () {
    $('#report-material').foundation('reveal', 'open');
});

$(document).on('click', '#close-sucess-report', function () {
    $('#success-report').foundation('reveal', 'close');
});

$(document).on('click', '.solve-report', function () {
    var reportId = $(this).data('value');
    var url = '/manage/reports/' + reportId + '/';
    var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: url,
        type: "PATCH",
        headers: {
            'X-CSRFToken': csfrToken
        },
        success: function () {
            $('#report-card-' + reportId).hide();
            var html = '<div data-alert class="alert-box success radius">';
            html += 'El reporte ha sido marcado como resuelto de manera exitosa';
            html += '<a href="#" class="close report-notif-close">&times;</a></div>';
            $('#reports-notifications').append(html);
        },
        error: function (xhr, textStatus, thrownError) {
            if (xhr.statusText) {
                alert(textStatus);
            }
        }
    });
});

$(document).on('click', '.reject-report', function () {
    var reportId = $(this).data('value');
    var url = '/manage/reports/' + reportId + '/';
    var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: url,
        type: "DELETE",
        headers: {
            'X-CSRFToken': csfrToken
        },
        success: function () {
            $('#report-card-' + reportId).hide();
            var html = '<div data-alert class="alert-box success radius">';
            html += 'El reporte ha sido rechazado como error de manera exitosa';
            html += '<a href="#" class="close report-notif-close">&times;</a></div>';
            $('#reports-notifications').append(html);
        },
        error: function (xhr, textStatus, thrownError) {
            if (xhr.statusText) {
                alert(textStatus);
            }
        }
    });
});

$(document).on('click', '.report-notif-close',function(){
    var notification = this.parentNode;
    notification.remove();
});