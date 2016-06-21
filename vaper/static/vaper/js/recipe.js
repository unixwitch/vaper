/* vim:set sw=4 ts=4 et: */

$(document).ready(function() {
    $('#index-dialog-add-recipe')
        .off('dialogopen')
        .on('dialogopen', function() {
            recipe_add_flavour();
        });

  /*
   * Main dialog setup.
   */
  $("#stock-dialog").dialog({
    width: 400,
    autoOpen: false,
    modal: true,
    buttons: [
      {
        text: "Update",
        click: do_update_stock,
      },
      {
        text: "Cancel",
        click: function() {
          $(this).dialog("close");
        },
      },
    ],
  });

  $('button#mix-update-stock').on("click", function(event) {
      $('#stock-dialog').dialog("open");
  });


  $("#updating-dialog").dialog({
    width: 400,
    autoOpen: false,
    modal: true,
  });

  /*
   * VG/PG ratio slider setup.
   */
  $("#vg-slider").slider({
    animate: true,
    max: 100,
    min: 0,
    step: 5,
    range: "min",
    change: ratio_slider_update,
    slide:  ratio_slider_update,
  });

  $("#vg-slider").append('<div id="vg-label" class="ratio-label"></div>');
  $("#vg-slider").append('<div id="pg-label" class="ratio-label"></div>');

  $("#vg-slider").slider("value", 60);

  /*
   * Nicotine base strength buttons.
   */
  $("#nic-pgvg-buttons button").on("click", nic_pgvg_button_click);
  $("#nic-base-buttons button").on("click", nic_base_button_click);
  $('#nic-target-value').on("click", function(event, ui) {
    recalculate();
  });

  /*
   * Amount to make buttons.
   */
  $("#amount-buttons button").on("click", amount_button_click);
});

/***
 *
 * Helper functions.
 */

/*
 * Calculate the recipe and display results in the table.
 */
function recalculate(slider_value) {
  /*
   * Depending on where we're called from, the slider_value might
   * be passed into the function if it differs from the current
   * value.  Otherwise, we take it from the slider.
   */
  if (typeof slider_value == "undefined") {
    slider_value = $('#vg-slider').slider('value');
  }

  var nic_in_vg = $('#nic-pgvg-buttons button.btn-primary').data('value');

  /* First, find out how much we're making. */
  var total_ml = $('#amount-buttons button.btn-primary').data("value");

  /* Base PG and VG amounts */
  var vg_pct = slider_value;
  var pg_pct = 100 - vg_pct;

  /* Nicotine calculation. */
  var nic_base_strength = $('#nic-base-buttons button.btn-primary').data('value');

  if (nic_base_strength) {
    var nic_target_strength = $('#nic-target-value').val();
    var nic_mg = total_ml * nic_target_strength;
    var nic_ml = nic_mg / nic_base_strength;
    nic_ml = Math.round(nic_ml * 10) / 10; /* round to 1dp */
    $('#mix-nicotine td').html(nic_ml + " ml");
  } else {
    nic_ml = 0;
    $('#mix-nicotine td').html('0 ml');
  }

  var target_vg_ml = total_ml * (vg_pct / 100.0);
  var target_pg_ml = total_ml * (pg_pct / 100.0);

  var extra_vg = 0, extra_pg = 0;
  var actual_vg = 0, actual_pg = 0;

  if (nic_in_vg == '1') {
    extra_vg += nic_ml;
  } else {
    extra_pg += nic_ml;
  }

  /*
   * Add flavours; assume all flavours come in PG.
   */
  document.used_flavours = [];

  for (let f of document.flavours) {
    var f_ml = Math.round(total_ml * (f.strength / 100.0) * 100) / 100;
    $('#mix-flavour-'+f.id+' td').html(f_ml + " ml (" + f.strength + "%)");
    extra_pg += f_ml;

    document.used_flavours.push({
      id: f.id,
      ml: f_ml,
    });
  }

  actual_pg = (target_pg_ml - extra_pg);
  actual_vg = (target_vg_ml - extra_vg);

  if (actual_pg < 0) {
    actual_vg -= -actual_pg;
    actual_pg = 0;
  } else if (actual_vg < 0) {
    actual_pg -= -actual_vg;
    actual_vg = 0;
  }

  var total_pg = actual_pg + extra_pg;
  var total_vg = actual_vg + extra_vg;

  $('#mix-vg td').html(Math.round(actual_vg * 10) / 10 + " ml");
  $('#mix-pg td').html(Math.round(actual_pg * 10) / 10 + " ml");

  var actual_vg_ratio = Math.round((total_vg / total_ml) * 100);
  $('#mix-ratio td').html(actual_vg_ratio + "/" + (100 - actual_vg_ratio));
}

/*
 * Update the labels on the ratio slider when it changes.
 */
function ratio_slider_update(event, ui) {
  $("#vg-label").html(ui.value + "% VG");
  $("#pg-label").html((100 - ui.value) + "% PG");
  recalculate(ui.value);
}

/*
 * Handle user clicks on nicotine base strength buttons.
 */
function nic_base_button_click(event) {
  $('#nic-base-buttons button').removeClass('btn-primary').addClass('btn-default');
  $(event.target).addClass('btn-primary');
  recalculate();
}

function nic_pgvg_button_click(event) {
  $('#nic-pgvg-buttons button').removeClass('btn-primary').addClass('btn-default');
  $(event.target).addClass('btn-primary');
  recalculate();
}

/*
 * Handle user clicks on amount to make buttons.
 */
function amount_button_click(event) {
  $('#amount-buttons button').removeClass('btn-primary').addClass('btn-default');
  $(event.target).addClass('btn-primary');
  recalculate();
}

function do_update_stock_success(data, status, xhr) {
  $('#updating-dialog').dialog("close");
}

function do_update_stock_error(xhr, status, error) {
  $('#updating-dialog p').html('<strong>Error:</strong> '+error);
}

function do_update_stock(event) {
  $('#stock-dialog').dialog('close');
  $('#updating-dialog p').html('<strong>Sending update to server...</strong>');
  $('#updating-dialog').dialog('open');
  $.ajax('/api/stock/mix/', {
    method: "POST",
    error: do_update_stock_error,
    success: do_update_stock_success,
    headers: {
      'X-CSRFToken': Cookies.get('csrftoken'),
    },
    data: {
      stock: JSON.stringify(document.used_flavours),
    },
  });
}

/*
 * Add recipe UI support.
 */

/* Add another flavour to the recipe */
function recipe_make_flavourinstance_ui(fnum, id, name, strength) {
    var input = 
        $('<div class="form-group" id="vui-form-group-flavour-'+fnum+'"/>', {
            style: 'margin: 0 0 0 0',
        })
        .append($('<div class="vui-form-input col-sm-9"/>')
            .append($('<input/>', {
                class: 'form-control vui-autocomplete',
                placeholder: 'Name...',
                type: 'text',
                id: 'id_flavour_'+fnum+'_name',
                name: 'flavour_'+fnum+'_name',
                required: 'required',
                maxlength: '64',
                value: name,
            })
            .append($('<input/>', {
                type: 'hidden',
                id: 'id_flavour_'+fnum+'_name_data',
                name: 'flavour_'+fnum+'_name_data',
                value: id,
            }))
            .data('vui-autocomplete-uri', '/api/flavour/autocomplete')
            .data('vui-no-suggestion-notice', '<em>Not found.</em>')
        ))
        .append($('<div class="vui-form-input col-sm-3"/>')
            .append($('<div class="input-group"/>')
                .append($('<input/>', {
                    class: 'form-control',
                    value: 0,
                    type: 'number',
                    dir: 'rtl',
                    id: 'id_flavour_'+fnum+'_strength',
                    name: 'flavour_'+fnum+'_strength',
                    required: 'required',
                    step: '0.1',
                    value: strength,
                }))
                .append($('<div class="input-group-addon">%</div>'))
            )
        )
        .append($('<ul class="help-block"></ul>'))
    ;

    return input;
}

function recipe_add_flavour(event) {
    var flavour_group = $('#recipe-flavour-group');

    if (typeof flavour_group.data('numflavours') == 'undefined') {
        flavour_group.data('numflavours', 0);
    }
    fnum = flavour_group.data('numflavours');

    flavour_group.data('numflavours', flavour_group.data('numflavours') + 1);
    $('#recipe-numflavours').val(flavour_group.data('numflavours'));

    input = recipe_make_flavourinstance_ui(fnum, '', '', 0);
    ui_setup(input);
    $('#recipe-flavour-group').append(input);

    return false;
}

$(document).off("vaper:ui:dialog:load");
$(document).on("vaper:ui:dialog:load", function() {
    var add_flavour_button = $('#recipe-flavour-add-button');

    if (typeof add_flavour_button != 'undefined') {
        add_flavour_button.off('click');
        add_flavour_button.on("click", recipe_add_flavour);
    }

    /*
     * After adding a new flavour, put it in the recipe.
     */
    $('#recipe-dialog-add-flavour')
        .off('dialogclose')
        .on('dialogclose', function(event, ui) {
        });

    /*
     * For editing (as opposed to adding), pre-populate the existing
     * flavours.
     */
    if (document.flavours) {
        var flavour_group = $('#recipe-flavour-group');
        var fnum = 0;

        for (let fl of document.flavours) {
            input = recipe_make_flavourinstance_ui(fnum++,
                        fl.id, fl.name, fl.strength);
            ui_setup(input);
            flavour_group.append(input);
        }

        flavour_group.data('numflavours', fnum);
        $('#recipe-numflavours').val(flavour_group.data('numflavours'));
    }
});
