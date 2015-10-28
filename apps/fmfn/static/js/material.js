$(document).ready(function () {

    // GET operations for modals -- START
    //GET Themes
    $('#show-themes').click(function () {
        $.get(
            "/tags/theme",
            function (data) {
                var container = document.getElementById('themes-modal-content');
                $('#themes-modal-content').html('');
                var output = [];
                for (var i = 0; i < data.data.length; i++) {
                    var iterable = data.data[i];

                    createTagModal('themes-modal-content',
                        'theme_id_',
                        iterable,
                        'edit-themes-modal',
                        'delete-tag-modal',
                        'edit-theme-tag',
                        'delete-tag delete-theme');
                }
            }
        );
    });

    //GET Types
    $('#show-types').click(function () {
        $.get(
            "/tags/type",
            function (data) {
                $('#types-modal-content').html('');
                for (var i = 0; i < data.data.length; i++) {
                    var iterable = data.data[i];
                    createTagModal('types-modal-content',
                        'type_id_',
                        iterable,
                        'edit-types-modal',
                        'delete-tag-modal',
                        'edit-type-tag',
                        'delete-tag delete-type');
                }
            }
        );
    });

    //GET Languages
    $('#show-languages').click(function () {
        $.get(
            "/tags/language",
            function (data) {
                $('#languages-modal-content').html('');
                for (var i = 0; i < data.data.length; i++) {
                    var iterable = data.data[i];
                    createTagModal('languages-modal-content',
                        'language_id_',
                        iterable,
                        'edit-languages-modal',
                        'delete-tag-modal',
                        'edit-language-tag',
                        'delete-tag delete-language');
                }
            }
        );
    });
    // GET operations for modals -- END

    // POST CREATE operations for modals -- START

    //POST theme
    $('#insert-theme-button').click(function () {
        var theme = $('#new-theme').val();
        var themeTest = theme.replace(/\s+/g, '');
        var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
        var url = $("input[name=create-theme-url]").val();
        if (theme.length <= 0 || themeTest == 0) {
            $('#theme-error').show();
        } else {
            $('#theme-error').hide();
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csfrToken,
                    action: 'create',
                    name: theme
                },
                success: function (response) {
                    //console.log(response);
                    var newTag = response.data;

                    //add to modal
                    createTagModal('themes-modal-content',
                        'theme_id_',
                        newTag,
                        'edit-themes-modal',
                        'delete-tag-modal',
                        'edit-theme-tag',
                        'delete-tag delete-theme');

                    //add to select2
                    var select = document.getElementById('id_themes');
                    var opt = document.createElement('option');
                    opt.value = newTag.id;
                    opt.innerHTML = newTag.name;
                    select.appendChild(opt);

                    //clear input
                    $('#new-theme').val('');

                    //display notification
                    displaySucessNotification(
                        'The tag ' + newTag.name + ' has been added successfully',
                        'themes-notifications');
                },
                error: function (xhr, textStatus, thrownError) {
                    if (xhr.statusText == 'FOUND') {
                        alert('Error: Estas tratando de dar de alta una etiqueta ya existente');
                    }
                }
            });
        }
    });

    //POST type
    $('#insert-type-button').click(function () {
        var type = $('#new-type').val();
        var typeTest = type.replace(/\s+/g, '');
        var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
        var url = $("input[name=create-type-url]").val();

        if (type.length <= 0 || typeTest == 0) {
            $('#type-error').show();
        } else {
            $('#type-error').hide();
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csfrToken,
                    action: 'create',
                    name: type
                },
                success: function (response) {
                    //console.log(response);
                    var newTag = response.data;
                    //add to modal
                    createTagModal('types-modal-content',
                        'type_id_',
                        newTag,
                        'edit-types-modal',
                        'delete-tag-modal',
                        'edit-type-tag',
                        'delete-tag delete-type');

                    //add to options
                    var container = document.getElementById('tags-types');
                    var checkbox = document.createElement('input');
                    checkbox.type = "checkbox";
                    checkbox.name = "types";
                    checkbox.value = newTag.id;
                    checkbox.id = "id_types_" + newTag.id;
                    checkbox.style.visibility = "hidden";

                    var label = document.createElement('label');
                    label.htmlFor = "id_types_" + newTag.id;
                    label.appendChild(document.createTextNode(newTag.name));

                    container.appendChild(checkbox);
                    container.appendChild(label);

                    //Clear input
                    $('#new-type').val('');

                    //Display notification
                    displaySucessNotification(
                        'The tag ' + newTag.name + ' has been successfully added',
                        'types-notifications'
                    );
                },
                error: function (xhr, textStatus, thrownError) {
                    if (xhr.statusText == 'FOUND') {
                        alert('Error: Estas tratando de dar de alta una etiqueta ya existente');
                    }
                }
            });
        }
    });

    //POST Language
    $('#insert-language-button').click(function () {
        var language = $('#new-language').val();
        var languageTest = language.replace(/\s+/g, '');
        var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
        var url = $("input[name=create-language-url]").val();

        if (language.length <= 0 || languageTest.length == 0) {
            $('#language-error').show();
        } else {
            $('#language-error').hide();
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csfrToken,
                    action: 'create',
                    name: language
                },
                success: function (response) {
                    //console.log(response);
                    var newTag = response.data;
                    //add to modal
                    createTagModal('languages-modal-content',
                        'language_id_',
                        newTag,
                        'edit-languages-modal',
                        'delete-tag-modal',
                        'edit-language-tag',
                        'delete-tag delete-language');

                    //add to options
                    var container = document.getElementById('tags-languages');
                    var checkbox = document.createElement('input');
                    checkbox.type = "checkbox";
                    checkbox.name = "languages";
                    checkbox.value = newTag.id;
                    checkbox.id = "id_languages_" + newTag.id;
                    checkbox.style.visibility = "hidden";

                    var label = document.createElement('label');
                    label.htmlFor = "id_languages_" + newTag.id;
                    label.appendChild(document.createTextNode(newTag.name));

                    container.appendChild(checkbox);
                    container.appendChild(label);

                    //Clear input
                    $('#new-language').val('');

                    //Display notification
                    displaySucessNotification(
                        'The tag ' + newTag.name + ' has been successfully added',
                        'languages-notifications'
                    );
                },
                error: function (xhr, textStatus, thrownError) {
                    if (xhr.statusText == 'FOUND') {
                        alert('Error: Estas tratando de dar de alta una etiqueta ya existente');
                    }
                }
            });
        }
    });
    // POST CREATE operations for modals -- END

    // POST EDIT operations for modals -- START

    //EDIT Theme tags
    $('#send-theme-edition').click(function () {
        var theme = $('#edit-theme').val();
        var themeTest = theme.replace(/\s+/g, '');
        var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
        var divToChange = $('input[name="div-theme-change"]');
        var divId = divToChange.val().toString();
        var id = divToChange.val().toString().replace('theme_id_', '');
        var url = '/tags/theme/' + id + '/edit/';
        //console.log(url);
        //console.log(csfrToken);
        if (theme.length <= 0 || themeTest == 0) {
            $('#theme-edit-error').show();
        } else {
            $('#theme-edit-error').hide();
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csfrToken,
                    name: theme
                },
                success: function (response) {
                    //console.log(theme);
                    //console.log(response);
                    var newTag = response.data;
                    document.getElementById(divId).remove();

                    //add to modal
                    createTagModal('themes-modal-content',
                        'theme_id_',
                        newTag,
                        'edit-themes-modal',
                        'delete-themes-modal',
                        'edit-theme-tag',
                        'delete-tag delete-theme');

                    //add to select2
                    var select = document.getElementById('id_themes');
                    var opt = document.createElement('option');
                    opt.value = newTag.id;
                    opt.innerHTML = newTag.name;
                    var optDelete = $("#id_themes option[value='" + newTag.id + "']")[0];
                    isSelected = optDelete.selected;
                    opt.selected = isSelected;
                    var selectedOptions = $(".select2-selection__choice");
                    for (var i = 0; i < selectedOptions.length; i++) {
                        if (selectedOptions[i].title == optDelete.textContent) {
                            selectedOptions[i].remove();
                            var select2opt = '<li title="' + newTag.name + '" class="select2-selection__choice">';
                            select2opt += '<span class="select2-selection__choice__remove" role="presentation">×</span>' + newTag.name;
                            select2opt += '</li>';
                            $(".select2-selection__rendered").append(select2opt);
                        }
                    }
                    $("#id_themes option[value='" + newTag.id + "']").remove();
                    select.appendChild(opt);

                    //<li title="Calculus" class="select2-selection__choice"></li>
                    //close edition modal
                    $('#edit-themes-modal').foundation('reveal', 'close');

                    //display Notification
                    displaySucessNotification('The tag ' + theme + ' has been edited', 'themes-notifications');
                },
                error: function (xhr, textStatus, thrownError) {
                    //console.log(xhr.statusText);
                    if (xhr.statusText == 'FOUND') {
                        alert('Error: Estas tratando de dar de alta una etiqueta ya existente');
                    }
                }
            });
        }
    });

    //EDIT Type tags
    $('#send-type-edition').click(function () {
        var type = $('#edit-type').val();
        var typeTest = type.replace(/\s+/g, '');
        var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
        var divToChange = $('input[name="div-type-change"]');
        var divId = divToChange.val().toString();
        var id = divToChange.val().toString().replace('type_id_', '');
        var url = '/tags/type/' + id + '/edit/';
        if (type.length <= 0 || typeTest == 0) {
            $('#type-edit-error').show();
        } else {
            $('#type-edit-error').hide();
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csfrToken,
                    name: type
                },
                success: function (response) {
                    //console.log(type);
                    //console.log(response);
                    var newTag = response.data;
                    document.getElementById(divId).remove();

                    //add to modal
                    createTagModal('types-modal-content',
                        'type_id_',
                        newTag,
                        'edit-types-modal',
                        'delete-tag-modal',
                        'edit-type-tag',
                        'delete-tag delete-type');

                    //delete old from options
                    var toDelete = $("#tags-types input[value='" + newTag.id + "']")[0];
                    var labelDelete = $("#tags-types label[for='" + toDelete.id + "']");
                    labelDelete.remove();
                    toDelete.remove();
                    var isChecked = toDelete.checked;

                    //add to options
                    var container = document.getElementById('tags-types');
                    var checkbox = document.createElement('input');
                    checkbox.type = "checkbox";
                    checkbox.name = "types";
                    checkbox.value = newTag.id;
                    checkbox.id = "id_types_" + newTag.id;
                    checkbox.style.visibility = "hidden";
                    checkbox.checked = isChecked;

                    var label = document.createElement('label');
                    label.htmlFor = "id_types_" + newTag.id;
                    label.appendChild(document.createTextNode(newTag.name));

                    container.appendChild(checkbox);
                    container.appendChild(label);

                    //Clear input
                    $('#new-type').val('');

                    //Close edition modal
                    $('#edit-types-modal').foundation('reveal', 'close');

                    //Display notification
                    displaySucessNotification(
                        'The tag ' + newTag.name + ' has been successfully edited',
                        'types-notifications'
                    );

                },
                error: function (xhr, textStatus, thrownError) {
                    //console.log(xhr.statusText);
                    if (xhr.statusText == 'FOUND') {
                        alert('Error: Estas tratando de dar de alta una etiqueta ya existente');
                    }
                }
            });
        }
    });

    //EDIT Language tags
    $('#send-language-edition').click(function () {
        var language = $('#edit-language').val();
        var languageTest = language.replace(/\s+/g, '');
        var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
        var divToChange = $('input[name="div-language-change"]');
        var divId = divToChange.val().toString();
        var id = divToChange.val().toString().replace('language_id_', '');
        var url = '/tags/language/' + id + '/edit/';
        if (language.length <= 0 || languageTest == 0) {
            $('#language-edit-error').show();
        } else {
            $('#language-edit-error').hide();
            //console.log(url);
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csfrToken,
                    name: language
                },
                success: function (response) {
                    //console.log(language);
                    //console.log(response);
                    var newTag = response.data;
                    document.getElementById(divId).remove();

                    //add to modal
                    createTagModal('languages-modal-content',
                        'language_id_',
                        newTag,
                        'edit-languages-modal',
                        'delete-tag-modal',
                        'edit-language-tag',
                        'delete-tag delete-language');

                    //delete old from options
                    var toDelete = $("#tags-languages input[value='" + newTag.id + "']")[0];
                    var labelDelete = $("#tags-languages label[for='" + toDelete.id + "']");
                    labelDelete.remove();
                    toDelete.remove();
                    var isChecked = toDelete.checked;

                    //add to options
                    var container = document.getElementById('tags-languages');
                    var checkbox = document.createElement('input');
                    checkbox.type = "checkbox";
                    checkbox.name = "languages";
                    checkbox.value = newTag.id;
                    checkbox.id = "id_languages_" + newTag.id;
                    checkbox.style.visibility = "hidden";
                    checkbox.checked = isChecked;

                    var label = document.createElement('label');
                    label.htmlFor = "id_languages_" + newTag.id;
                    label.appendChild(document.createTextNode(newTag.name));

                    container.appendChild(checkbox);
                    container.appendChild(label);

                    //Clear input
                    $('#new-language').val('');

                    //Close edition modal
                    $('#edit-languages-modal').foundation('reveal', 'close');

                    //Display notification
                    displaySucessNotification(
                        'The tag ' + newTag.name + ' has been successfully edited',
                        'languages-notifications'
                    );

                },
                error: function (xhr, textStatus, thrownError) {
                    //console.log(xhr.statusText);
                    if (xhr.statusText == 'FOUND') {
                        alert('Error: Estas tratando de dar de alta una etiqueta ya existente');
                    }
                }
            });
        }
    });
    // POST EDIT operations for modals -- END

    //DELETE Operations
    $('#send-delete-tag').click(function () {
        var classList = $('input[name="type-of-tag"]').val().split(/\s+/);
        var divToDelete = $('input[name="div-to-erase"]');
        var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
        var url, id, divId;

        if ($.inArray('delete-theme', classList) >= 0) {
            divId = divToDelete.val().toString();
            id = divToDelete.val().toString().replace('theme_id_', '');
            url = '/tags/theme/' + id + '/delete/';
            //console.log(url);
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csfrToken
                },
                success: function (response) {
                    //console.log(response);
                    document.getElementById(divId).remove();

                    //Delete from select2
                    var optDelete = $("#id_themes option[value='" + id + "']")[0];
                    var deletedText = $('#tag-to-delete').textContent;
                    isSelected = optDelete.selected;
                    var selectedOptions = $(".select2-selection__choice");
                    if (isSelected) {
                        for (var i = 0; i < selectedOptions.length; i++) {
                            if (selectedOptions[i].title == optDelete.textContent) {
                                selectedOptions[i].remove();
                            }
                        }
                    }
                    $("#id_themes option[value='" + id + "']").remove();

                    //close edition modal
                    $('#delete-tag-modal').foundation('reveal', 'close');

                    //display Notification
                    displaySucessNotification('The tag has been deleted', 'themes-notifications');
                },
                error: function (xhr, textStatus, thrownError) {
                    //console.log(xhr.statusText);
                    if (xhr.statusText == 'FOUND') {
                        alert('Error: Estas tratando de dar de alta una etiqueta ya existente');
                    }
                }
            });
        } else if ($.inArray('delete-type', classList) >= 0) {
            divId = divToDelete.val().toString();
            id = divToDelete.val().toString().replace('type_id_', '');
            url = '/tags/type/' + id + '/delete/';
            //console.log(url);

            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csfrToken
                },
                success: function (response) {
                    //console.log(response);
                    document.getElementById(divId).remove();

                    //delete old from options
                    var toDelete = $("#tags-types input[value='" + id + "']")[0];
                    var labelDelete = $("#tags-types label[for='" + toDelete.id + "']");
                    labelDelete.remove();
                    toDelete.remove();
                    var isChecked = toDelete.checked;

                    //Close edition modal
                    $('#delete-tag-modal').foundation('reveal', 'close');

                    //Display notification
                    displaySucessNotification(
                        'The tag has been successfully deleted',
                        'types-notifications'
                    );

                },
                error: function (xhr, textStatus, thrownError) {
                    //console.log(xhr.statusText);
                    if (xhr.statusText == 'FOUND') {
                        alert('Error: Estas tratando de dar de alta una etiqueta ya existente');
                    }
                }
            });

        } else if ($.inArray('delete-language', classList) >= 0) {
            //TODO check why deleted tags keep appearing
            divId = divToDelete.val().toString();
            id = divToDelete.val().toString().replace('language_id_', '');
            url = '/tags/language/' + id + '/delete/';
            //console.log(url);
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csfrToken
                },
                success: function (response) {
                    //console.log(response);
                    var newTag = response.data;
                    document.getElementById(divId).remove();

                    //delete old from options
                    var toDelete = $("#tags-languages input[value='" + id + "']")[0];
                    var labelDelete = $("#tags-languages label[for='" + toDelete.id + "']");
                    labelDelete.remove();
                    toDelete.remove();
                    var isChecked = toDelete.checked;

                    //Close edition modal
                    $('#delete-tag-modal').foundation('reveal', 'close');

                    //Display notification
                    displaySucessNotification(
                        'The tag has been successfully deleted',
                        'languages-notifications'
                    );

                },
                error: function (xhr, textStatus, thrownError) {
                    //console.log(xhr.statusText);
                    if (xhr.statusText == 'FOUND') {
                        alert('Error: Estas tratando de dar de alta una etiqueta ya existente');
                    }
                }
            });
        }
    });
});

//Helper for edit theme tag
//it passes the information from the first modal to the edition modal
$(document).on('click', '.edit-theme-tag', function () {
    var tagText = document.getElementById(this.parentNode.id).textContent;
    $('#edit-theme').val(tagText);
    $('input[name="div-theme-change"]').val(document.getElementById(this.parentNode.id).id.toString());
});

//Helper for edit type tag
//it passes the information from the first modal to the edition modal
$(document).on('click', '.edit-type-tag', function () {
    var tagText = document.getElementById(this.parentNode.id).textContent;
    $('#edit-type').val(tagText);
    $('input[name="div-type-change"]').val(document.getElementById(this.parentNode.id).id.toString());
});

//Helper for edit theme tag
//it passes the information from the first modal to the edition modal
$(document).on('click', '.edit-language-tag', function () {
    var tagText = document.getElementById(this.parentNode.id).textContent;
    $('#edit-language').val(tagText);
    $('input[name="div-language-change"]').val(document.getElementById(this.parentNode.id).id.toString());
});

//Helper for handling notifications
//it deletes the notification when you click the x on the notification
$(document).on('click', '.close', function () {
    var notification = this.parentNode;
    notification.remove();
});

$(document).on('click', '.delete-tag', function () {
    var tagText = document.getElementById(this.parentNode.id).textContent;
    $('#tag-to-delete').html(tagText);
    $('input[name="type-of-tag"]').val(this.className);
    $('input[name="div-to-erase"]').val(document.getElementById(this.parentNode.id).id.toString());
});

$(document).on('click', '.abort-delete-tag', function () {
    $('#delete-tag-modal').foundation('reveal', 'close');
});

$(document).on('click', '.abort-delete-material', function () {
    console.log(this);
    $('#delete-material-modal').foundation('reveal', 'close');
});

$(document).on('click', '#send-delete-material', function () {
    var url = $('input[name="url-material-delete"]').val();
    var csfrToken = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: url,
        type: "DELETE",
        headers: {
            'X-CSRFToken': csfrToken
        },
        success: function (response) {
            console.log(response);
            window.location.replace("/");
        },
        error: function (xhr, textStatus, thrownError) {
            console.log(xhr.statusText);
        }
    });
});


function displaySucessNotification(message, id) {
    var html = '<div data-alert class="alert-box success radius">';
    html += message;
    html += '<a href="#" class="close">&times;</a></div>';
    $('#' + id).prepend(html);
}

function createTagModal(containerId, idSufix, newTag, editModalId, deleteModalId, editClass, deleteClasses) {

    var container = document.getElementById(containerId);
    var divElem = document.createElement('div');
    divElem.id = idSufix + newTag.id;
    divElem.className = "tag-edit-delete";
    divElem.appendChild(document.createTextNode(newTag.name));

    var anchorEdit = '<a href="#" data-reveal-id="' + editModalId + '" class="' + editClass + '">';
    anchorEdit += '<i class="fa fa-pencil"></i>';
    anchorEdit += '</a>';

    var anchorDelete = '<a href="#" data-reveal-id="' + deleteModalId + '" class="' + deleteClasses + '">';
    anchorDelete += '<i class="fa fa-trash-o"></i>';
    anchorDelete += '</a>';

    container.appendChild(divElem);
    var newDiv = $('#' + idSufix + newTag.id);
    newDiv.prepend(anchorDelete);
    newDiv.prepend(anchorEdit);
}