var laptimetable;
var vehicletable;
var vehiclelaptimetable;
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

//    vehicletable = $('#vehicletable').DataTable({
//        "columnDefs": [
//            { "visible": false, "targets": 1 }
//        ],
//        "order": [[ 1, 'asc' ]],
//        "displayLength": 50,
//        "drawCallback": function ( settings ) {
//            var api = this.api();
//            var rows = api.rows( {page:'current'} ).nodes();
//            var last=null;
//
//            api.column(1, {page:'current'} ).data().each( function ( group, i ) {
//                if ( last !== group ) {
//                    $(rows).eq( i ).before(
//                        '<tr class="group"><td colspan="5">'+group+'</td></tr>'
//                    );
//                    last = group;
//                }
//            } );
//        }
//    } );

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
