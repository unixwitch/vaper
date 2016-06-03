/* vim:set sw=4 ts=4 et: */

$(document).ready(function() {
  
  /*
   * Main dialog setup.
   */
  $("#mix-dialog").dialog({
    width: 650,
    autoOpen: false,
    show: "slideDown",
    hide: "slideUp",
    modal: true,
    buttons: [
      {
        text: "Mix",
        click: function() {
        },
      },
    ],
  });

  $("#mix-button").on("click", function() {
    recalculate();
    $("#mix-dialog").dialog("open");
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

  $("#vg-slider").append('<div id="vg-label" class="ratio-label">VG</div>');
  $("#vg-slider").append('<div id="pg-label" class="ratio-label">PG</div>');

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
  for (let f of document.flavours) {
    var f_ml = total_ml * (f.strength / 100.0);
    $('#mix-flavour-'+f.id+' td').html(f_ml + " ml");
    extra_pg += f_ml;
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

  $('#mix-vg td').html(actual_vg + " ml");
  $('#mix-pg td').html(actual_pg + " ml");

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
