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

    return data;
}

/*
 * Set up any UI elements that are children of this element.
 */
function ui_setup_dialog(dialog) {
    var div = dialog.find('.vui-dialog');
    var button = dialog.find('.vui-dialog-open');

    button.on("click", function(event) {
        div.load(div.data('uri'), function() {
            div.dialog({
                width: 650,
                autoOpen: false,
                modal: true,
            });

            ui_setup(div);
            div.dialog("open");
        });

        return false;
    });
}

function ui_setup(elm) {
    for (let dialog of $('.vui-dialog-button').toArray()) {
        ui_setup_dialog($(dialog));
    }

    for (let form of $(elm).find('.vui-form').toArray()) {
        for (let input of $(form).find('input.vui-autocomplete').toArray()) {
            $(input).autocomplete({
                serviceUrl: $(input).data('vui-autocomplete-uri'),
                autoSelectFirst: true,
                //showNoSuggestionNotice: true,
                //noSuggestionNotice: "<em>Creating new manufacturer</em>",
            });
        }

        $(form).on("submit", function() {
            data = ui_form_build_data(form);

            $.ajax({
                type: 'POST',
                url: $(form).data('uri'),
                data: { 'data': JSON.stringify(data), },
                success: function(data, status, xhr) {
                    switch ($(form).data('on-submit')) {
                    case 'reload':
                        location.reload();
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
