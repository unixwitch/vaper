/* vim:set sw=4 ts=4 et: */

$(document).ready(function() {
    ui_setup(this);
});

/*****
 *
 * Forms handling.
 */

/*
 * Return a JSON array of this form's data.
 */
function ui_form_build_data(form) {
    data = {};

    for (let input of $(form).find('input').toArray()) {
        data[$(input).attr('name')] = $(input).val();
    }

    for (let input of $(form).find('textarea').toArray()) {
        data[$(input).attr('name')] = $(input).val();
    }

    return data;
}

/*
 * Set up any UI elements that are children of this element.
 */
function ui_setup_dialog(dialog) {
    var div = dialog.find('.vui-dialog');
    var button = dialog.find('.vui-dialog-open');

    button.off('click');
    button.on("click", function(event) {
        div.load(div.data('uri'), function() {
            div.dialog({
                width: 650,
                autoOpen: false,
                modal: true,
            });

            ui_setup(div);
            div.dialog("open");

            $(document).trigger("vaper:ui:dialog:load");

            return false;
        });
    });
}

function ui_setup_dialog_button(button) {
    var div = $('#'+$(button).data('vui-dialog'));

    $(button).off('click');
    $(button).on("click", function(event) {
        div.load(div.data('uri'), function() {
            attrs = {
                width: 650,
                autoOpen: false,
                modal: true,
            };

            div.dialog(attrs);

            ui_setup(div);
            div.dialog("open");

            $(document).trigger("vaper:ui:dialog:load");

            return false;
        });
    });
}

function ui_on_autocomplete_select(suggestion) {
    var dataname = $(this).attr('id') + '_data';
    if (dataname) {
        $('#' + dataname).val(suggestion.data);
    }
}

function ui_setup(elm) {
    for (let dialog of $('a.vui-dialog-button').toArray()) {
        ui_setup_dialog($(dialog));
    }

    for (let button of $('button.vui-dialog-button').toArray()) {
        ui_setup_dialog_button(button);
    }

    for (let input of $(elm).find('input.vui-autocomplete').toArray()) {
        $(input).autocomplete({
            serviceUrl: $(input).data('vui-autocomplete-uri'),
            onSelect: ui_on_autocomplete_select,
            autoSelectFirst: true,
            showNoSuggestionNotice: $(input).data('vui-no-suggestion-notice') ? true : false,
            noSuggestionNotice: $(input).data('vui-no-suggestion-notice'),
        });
    }

    for (let form of $(elm).find('.vui-form').toArray()) {
        $(form).off('submit');
        $(form).on("submit", function() {
            data = ui_form_build_data(form);

            $.ajax({
                type: 'POST',
                url: $(form).data('uri'),
                data: { 'data': JSON.stringify(data), },
                success: function(data, status, xhr) {
                    var dlg = $(form).closest('.vui-dialog');
                    dlg.dialog("close");
                    dlg.dialog("destroy");

                    switch (dlg.data('vui-close')) {
                    case 'reload':
                        location.reload();
                        break;
                    case 'home':
                        location.href = '/';
                        break;
                    }
                },
                error: function(xhr, status, error) {
                    data = $.parseJSON(xhr.responseText);
                    for (let field of Object.keys(data['errors'])) {
                        var group = $(form).find('div#vui-form-group-'+field);
                        $(group).addClass('has-error');
                        $(group).find('ul.help-block').html("").append('<li>'+data['errors'][field]+'</li>');
                    }
                },
                headers: {
                    'X-CSRFToken': $(form).data('csrftoken'),
                },
            });

            return false;
        });
    }
}
