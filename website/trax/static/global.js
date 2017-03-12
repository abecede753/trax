var laptimetable;
var vehicletable;
var vehiclelaptimetable;

function format_laptimestableinfo ( d ) {
  // `d` is the original data object for the row
  var strg = '';
  strg += '<table cellpadding="0" cellspacing="0" border="0" style="padding-left:50px;">';
  if (d.link !== null && d.link !== '') {
    strg += '<tr>'+
      '<td>Link:</td>'+
      '<td><a href="'+d.link+'" target="_blank">' + d.link + '</a></td>'+
      '</tr>';
  }
  if (d.comment !== null && d.comment !== '') {
    strg += '<tr>' +
      '<td>Comment:</td>' +
      '<td>' + d.comment + '</td>' +
      '</tr>';
  }
  strg += '</table>';
  return strg;
}

$(document).ready(function() {
//    var dt_table = $('.laptimetable').dataTable({
//        language: 'en',
//        order: [[ 0, "desc" ]],
//        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
//        columnDefs: [
//            {orderable: true,
//                searchable: true,
//                className: "center",
//                targets: [0, 1]
//            }
//        ],
//        searching: true,
//        processing: true,
//        serverSide: true,
//        stateSave: true,
//        ajax: '/t/api/tracks_list/'
//    });



  /* vehicles table */
  vehicletable = $('#vehicletable').DataTable( {
    // ajax: "laptimes.json",
    order: [[ 0, "asc" ]],
    lengthMenu: [[50, 100, 10000], [50, 100, 'all']],
    "initComplete": function(settings, json) {
      $(".dataTables_filter input").select().focus();
    }
  } );

  // Order by the grouping
  $('#vehicletable tbody').on( 'click', 'tr.group', function () {
    var currentOrder = table.order()[0];
    if ( currentOrder[0] === 1 && currentOrder[1] === 'asc' ) {
      table.order( [ 1, 'desc' ] ).draw();
    }
    else {
      table.order( [ 1, 'asc' ] ).draw();
    }
  } );

  /* tracks table */
  laptimetable = $('#laptimetable').DataTable( {
    ajax: "laptimes.json",
    order: [[ 2, "asc" ]],
    columns: [
      { className:      "details-control text-center",
        orderable:      false,
        data:           null,
        defaultContent: "<span role=\"button\" class=\"glyphicon glyphicon-info-sign\"></span>"
      },
      { data: "vehicle" },
      { data: {
        _: "duration.display",
        sort: "duration.millis"
      } },
      { data: "name" },
      { data: {
        _:    "date.display",
        sort: "date.timestamp"
      } },
      { data: "classes",
        visible: false}
    ],
    "deferRender": true
  } );
  // Add event listener to laptimetable for opening and closing details
  $('#laptimetable tbody').on('click', 'td.details-control', function () {
    var tr = $(this).closest('tr');
    var row = laptimetable.row( tr );

    if ( row.child.isShown() ) {
      // This row is already open - close it
      row.child.hide();
      tr.removeClass('shown');
    }
    else {
      // Open this row
      row.child( format_laptimestableinfo(row.data()) ).show();
      tr.addClass('shown');
    }
  } );

  $('#filterbyvehicleclass').on( 'click', 'button', function () {
    laptimetable.columns(5).search($(this).data("value")).draw();
  });


  /* ################################################################################### */



  /* vehicle laptime table */
  vehiclelaptimetable = $('#vehiclelaptimetable').DataTable( {
    // ajax: "laptimes.json",
    order: [[ 0, "asc" ]],
    lengthMenu: [[50, 100, 10000], [50, 100, 'all']],
  } );

  /* main tracks table */
  tracktable = $('#tracktable').DataTable( {
    // ajax: "laptimes.json",
    order: [[ 1, "asc" ]],
    lengthMenu: [[50, 100, 10000], [50, 100, 'all']],
    "initComplete": function(settings, json) {
      $(".dataTables_filter input").select().focus();
    }
  } );

  /* player laptime table */
  playerlaptimetable = $('#playerlaptimetable').DataTable( {
    // ajax: "laptimes.json",
    order: [[ 1, "asc" ]],
    lengthMenu: [[50, 100, 10000], [50, 100, 'all']],
  } );

  /* player laptime table */
  playerstable = $('#playerstable').DataTable( {
    // ajax: "laptimes.json",
    order: [[ 1, "asc" ]],
    lengthMenu: [[50, 100, 10000], [50, 100, 'all']],
  } );

  /* animate login/register */
  $('#loginreg').on('fadeout', function () {
    $(this).fadeTo( "slow", 0.1, function(){ $(this).trigger('fadein'); });
  });
  $('#loginreg').on('fadein', function () {
    $(this).fadeTo( "slow", 1, function(){ $(this).delay(500).trigger('fadeout'); });
  });
  $('#loginreg').trigger('fadeout');

  /* various settings */
  $('.combobox').combobox({bsVersion: '3'});


  /* if we have a datatable, focus the filter field */

  $('[data-toggle="tooltip"]').tooltip();

  /* submit any form only once */
  $('form').submit(function(){
    $('button[type=submit]', this).attr('disabled', 'disabled');
  });

  show_platforms();



});

function show_platforms() {
  var currents = Cookies.get('traxpf');
  if (currents === undefined) {
    Cookies.set('traxpf', 'pc xb1 ps4');
    currents = 'pc xb1 ps4';
  }
  for (let pf of ['pc', 'xb1', 'ps4']) {
    if (currents.indexOf(pf) != -1) { $('#platform_' + pf).css('opacity', '1.0'); }
  }
}
function toggle_platform(p) {
  var currents = Cookies.get('traxpf');
  Cookies.set('traxpf', 'pc', { expires: 365 });
// Cookies.get('name'); // => 'value'
// Cookies.remove('name');

}

function convert_from_laptime_to_cc_millis() {
  "use strict";
  var value = $("#calc_laptime").val();
  if (value.indexOf(":") > -1) {
    var items = value.split(":");
    var millis = parseFloat(items[0]) * 60 + parseFloat(items[1]);
  } else {
    var millis = parseFloat(value);
  }
  millis = millis / 2.59 * 1000.0;
  $("#calc_millis").val(Math.round(millis));

}
