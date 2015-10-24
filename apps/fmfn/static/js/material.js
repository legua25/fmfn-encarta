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
                        'delete-tag');
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
                        'delete-tag');
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
                        'delete-tag');
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
                    console.log(response);
                    var newTag = response.data;

                    //add to modal
                    var container = document.getElementById('themes-modal-content');
                    var divElem = document.createElement('div');
                    divElem.id = "theme_id_" + newTag.id;
                    divElem.className = "tag-edit-delete";
                    divElem.appendChild(document.createTextNode(newTag.name));

                    var anchorEdit = '<a href="#" data-reveal-id="edit-themes-modal" class="edit-theme-tag">';
                    anchorEdit += '<i class="fa fa-pencil"></i>';
                    anchorEdit += '</a>';

                    var anchorDelete = '<a href="#" data-reveal-id="delete-themes-modal" class="delete-tag">';
                    anchorDelete += '<i class="fa fa-trash-o"></i>';
                    anchorDelete += '</a>';

                    container.appendChild(divElem);
                    $('#theme_id_' + newTag.id).prepend(anchorDelete);
                    $('#theme_id_' + newTag.id).prepend(anchorEdit);

                    //add to select2
                    var select = document.getElementById('id_themes');
                    var opt = document.createElement('option');
                    opt.value = newTag.id;
                    opt.innerHTML = newTag.name;
                    select.appendChild(opt);

                    //clear input
                    $('#new-theme').val('');
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
                    console.log(response);
                    var newTag = response.data;
                    //add to modal
                    var modal = "<input type=\"text\" value=\"" + newTag.name + "\" name = \"" + newTag.id + "\" disabled=\"disabled\">";
                    $('#types-modal-content').append(modal);
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
                    console.log(response);
                    var newTag = response.data;
                    //add to modal
                    var modal = "<input type=\"text\" value=\"" + newTag.name + "\" name = \"" + newTag.id + "\" disabled=\"disabled\">";
                    $('#languages-modal-content').append(modal);
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
        console.log(url);
        console.log(csfrToken);
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
                    console.log(theme);
                    console.log(response);
                    var newTag = response.data;
                    document.getElementById(divId).remove();

                    //add to modal
                    createTagModal('themes-modal-content',
                        'theme_id_',
                        newTag,
                        'edit-themes-modal',
                        'delete-themes-modal',
                        'edit-theme-tag',
                        'delete-tag');

                    //add to select2
                    var select = document.getElementById('id_themes');
                    var opt = document.createElement('option');
                    opt.value = newTag.id;
                    opt.innerHTML = newTag.name;
                    $("#id_themes option[value='" + newTag.id + "']").remove();
                    select.appendChild(opt);

                    //display Notification
                    $('#edit-themes-modal').foundation('reveal', 'close');
                    displaySucessNotification('The tag ' + theme + ' has been edited', '#themes-notifications');
                },
                error: function (xhr, textStatus, thrownError) {
                    console.log(xhr.statusText);
                    if (xhr.statusText == 'FOUND') {
                        alert('Error: Estas tratando de dar de alta una etiqueta ya existente');
                    }
                }
            });
        }
    });

    // POST EDIT operations for modals -- END

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

function displaySucessNotification(message, id) {
    var html = '<div data-alert class="alert-box success radius">';
    html += message;
    html += '<a href="#" class="close">&times;</a></div>';
    $(id).prepend(html);
}

function createTagModal(containerId, idSufix, newTag, editModalId, deleteModalId, editClass, deleteClass) {

    var container = document.getElementById(containerId);
    var divElem = document.createElement('div');
    divElem.id = idSufix + newTag.id;
    divElem.className = "tag-edit-delete";
    divElem.appendChild(document.createTextNode(newTag.name));

    var anchorEdit = '<a href="#" data-reveal-id="' + editModalId + '" class="' + editClass + '">';
    anchorEdit += '<i class="fa fa-pencil"></i>';
    anchorEdit += '</a>';

    var anchorDelete = '<a href="#" data-reveal-id="' + deleteModalId + '" class="' + deleteClass + '">';
    anchorDelete += '<i class="fa fa-trash-o"></i>';
    anchorDelete += '</a>';

    container.appendChild(divElem);
    var newDiv = $('#' + idSufix + newTag.id);
    newDiv.prepend(anchorDelete);
    newDiv.prepend(anchorEdit);
}