var laptimetable;
var vehicletable;
var vehiclelaptimetable;

function format_laptimestableinfo ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Link:</td>'+
            '<td>'+d.link+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Comment:</td>'+
            '<td>'+d.comment+'</td>'+
        '</tr>'+
    '</table>';
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
        columns: [
            { className:      "details-control",
              orderable:      false,
              data:           null,
              defaultContent: ""
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
            } }
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



    /* vehicle laptime table */
    vehiclelaptimetable = $('#vehiclelaptimetable').DataTable( {
        // ajax: "laptimes.json",
        order: [[ 0, "asc" ]],
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


});


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
