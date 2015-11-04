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