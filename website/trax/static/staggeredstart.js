var player = document.getElementById("gogogo");
var bell_url = "/static/bell.mp3";
var participantstable;

$(document).ready(function() {
    participantstable = $("#participantstable").DataTable( {
        language: {
            "emptyTable": "Waiting for players to join..."
        },

        ajax: "participantstable.json",
        "deferRender": true
    } );

    function audio_loaded() {
        player.src = bell_url;
        $("#testsoundbtn").show();
    }

    var audio = new Audio();
    audio.addEventListener("canplaythrough", audio_loaded, false);
    audio.src = bell_url;

    setInterval( function () {
        participantstable.ajax.reload();
    }, 2000 );
});

function start_now() {
    player.play();
    $("body")
        .stop()
        .css("background-color", "#00FF00")
        .animate({ backgroundColor: "#FFFFFF"}, 5000);
}

var DBG;
function enlist_car(btn) {
    var url = $('#enlist_url').text() + '?slug='
    url += btn.value;
    $.ajax({url: url})
        .done(function (data) {
            if (data.result !== "OK") {
                window.alert("Error: " + data.result);
            } else {
                $('.enlist_btn').removeClass('btn-primary');
                $(btn).addClass('btn-primary');

            }
        });
}
