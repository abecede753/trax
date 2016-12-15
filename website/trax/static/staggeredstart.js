var player = document.getElementById("gogogo");
var bell_url = "/static/bell.mp3";
var participantstable;

$(document).ready(function() {
    "use strict";
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

    if ($("#event_status").text() === "i") {
        setInterval(function () { participantstable.ajax.reload(); }, 2000);
        setInterval(function () { $.ajax( { url: "get_status/"} ).
            done( function(data) {
                if (data.result !== "i") { window.location.reload(); }

            }); }, 1000);
    }
});

function start_now() {
    "use strict";
    player.play();
    $("body")
        .stop()
        .css("background-color", "#00FF00")
        .animate({ backgroundColor: "#FFFFFF"}, 5000);
}

var DBG;
function enlist_car(btn) {
    "use strict";
    var url = $("#enlist_url").text() + "?slug=";
    url += btn.value;
    $.ajax({url: url})
        .done(function (data) {
            console.log(data);
            $(".enlist_btn").removeClass("btn-primary");
            $(btn).addClass("btn-primary");
        });
}

function greenlight(pk) {
    "use strict";
    $("#img" + pk).attr("src", "/static/green_light.png");
}
function usergreenlight(pk) {
    "use strict";
    start_now();
    $("#img" + pk).attr("src", "/static/green_light.png");
}
