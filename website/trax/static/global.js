$(document).ready(function() {
    var dt_table = $('.trackstable').dataTable({
        language: 'en',
        order: [[ 0, "desc" ]],
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        columnDefs: [
            {orderable: true,
                searchable: true,
                className: "center",
                targets: [0, 1]
            }
        ],
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: true,
        ajax: '/t/api/tracks_list/'
    });


    /* animate login/register */

    $('#loginreg').on('fadeout', function () {
        $(this).fadeTo( "slow", 0.1, function(){ $(this).trigger('fadein'); });
    });
    $('#loginreg').on('fadein', function () {
        $(this).fadeTo( "slow", 1, function(){ $(this).delay(500).trigger('fadeout'); });
    });
    $('#loginreg').trigger('fadeout');
});
