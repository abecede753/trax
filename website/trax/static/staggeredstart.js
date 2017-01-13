var player = document.getElementById("gogogo");
var bell_url = "/static/bell.mp3";
var participantstable;
var DDEBUG;
// function receive_ajax(data) {
//     if (data.status === "i") {  // still initializing
//         $("#participantsdiv").html(data.table);
//         window.setTimeout("updateScreen", 1600);
//     }
// }


$(document).ready(function() {

    function audio_loaded() {
        player.src = bell_url;
        $("#testsoundbtn").show();
    }

    var audio = new Audio();
    audio.addEventListener("canplaythrough", audio_loaded, false);
    audio.src = bell_url;

//    if ($("#event_status").text() === "i") {
//        // setInterval(function () { participantstable.ajax.reload(); }, 2000);
//        setInterval(function () { $.ajax( { url: "get_status/"} ).
//            done( function(data) {
//                if (data.result !== "i") { window.location.reload(); }
//
//            }); }, 1600);
//    }
    call_ajax();
    $("#showvehiclelist").collapse();
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
    DBG = btn;
    $.ajax({url: btn.value})
        .done(function (data) {
            $(".enlist_btn").removeClass("btn-primary");
            $(btn).addClass("btn-primary");
            $("#showvehiclelist").collapse("hide");
            $("#togglevehiclelist").text(btn.textContent);
        });
}

function greenlight(pk) {
    $("#img" + pk).attr("src", "/static/green_light.png");
}
function usergreenlight(pk) {
    start_now();
    $("#img" + pk).attr("src", "/static/green_light.png");
}

function getReady() {
    meSpeak.speak("Get ready!", {variant:"f5", wordgap:5});
}

$("<img/>")[0].src = "/static/green_light.png";

meSpeak.loadConfig("/static/mespeak/mespeak_config.json");
meSpeak.loadVoice('/static/mespeak/voices/en/en-us.json');

function fill_participants_table(data) {
    var tb = $("#participantsbody");
    tb.html("");
    for (idx = 0; idx < data.length; idx++) {
        var entry = data[idx];
        var row = $("<tr />", {}).appendTo(tb);
        $("<td />", {"text": " ", "class": "text-center"}).appendTo(row);
        $("<td />", {"text": entry.username}).appendTo(row);
        $("<td />", {"text": entry.vehicle}).appendTo(row);
    }
}

function process_ajax(response) {
    var jsn = response.data;
    DDEBUG = jsn;
    // initializing / invitation state
    if (jsn.status === "i") {
        fill_participants_table(jsn.players);
        window.setTimeout("call_ajax", 900);
    }

    // racing starts
    if (jsn.status === "r") {
        start_race(jsn.players);
    }
}

function call_ajax() {
    $.ajax(
        { url: $("#json_url").html() + '?r=' + Math.random() }
    ).done(
        function(result) {
            process_ajax(result.data);
        }
    );
}

function start_race(data) {
    var tb = $("#racebody");
    var myself = $("#username").html();
    var idx;
    tb.html("");
    for (idx = 0; idx < data.length; idx+=1) {
        var entry = data[idx];
        var row = $("<tr />", {}).appendTo(tb);
        $("<td />", {"text": "<img src=\"/static/red_light.png\" id=\"" + entry.username + "\">",
                     "class": "text-center"}).appendTo(row);
        $("<td />", {"text": entry.username}).appendTo(row);
        $("<td />", {"text": entry.vehicle}).appendTo(row);
        var start_in_millis = entry.start_timestamp - ServerDate.now();

        if (entry.username === myself) {
            if (start_in_millis > 9000) {
                meSpeak.speak("You are in position, number " + (idx + 1) + ".",
                    {variant:"f5", wordgap:5});
            }
            if (start_in_millis > 2000) {
                setTimeout( function() { usergreenlight( entry.username ); }, start_in_millis );
                setTimeout( function() { getReady(); }, start_in_millis - 5000 );
            }
        } else {
            if (start_in_millis > 2000) {
                setTimeout(function () {
                    greenlight(entry.username);
                }, start_in_millis);
            }
        }
    }
}
