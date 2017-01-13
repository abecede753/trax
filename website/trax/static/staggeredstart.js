var player = document.getElementById("gogogo");
var bell_url = "/static/bell.mp3";
var DDEBUG;

function LOG(txt) { console.log(txt);}

$(document).ready(function() {

    function audio_loaded() {
        player.src = bell_url;
        $("#testsoundbtn").show();
    }

    var audio = new Audio();
    audio.addEventListener("canplaythrough", audio_loaded, false);
    audio.src = bell_url;
    call_ajax();
    $("#showvehiclelist").collapse();
});

function enlist_car(btn) {
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
    player.play();
    $("body")
        .stop()
        .css("background-color", "#00FF00")
        .animate({ backgroundColor: "#FFFFFF"}, 5000);
    greenlight(pk);
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
        LOG("start_ts " + entry.timestamp)
        LOG("NOW " + ServerDate.now())
        var start_in_millis = entry.timestamp - ServerDate.now();
        LOG("start_in_millis " + start_in_millis)

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


function process_ajax(jsn) {
    LOG("process_ajax");

    // initializing / invitation state, needs continuous refresh
    if (jsn.status === "i" || jsn.status === "p") {
        $("#twocols").show();
        $("#racescreen").hide();
        LOG("jsn.status i");
        fill_participants_table(jsn.players);
        LOG("settingtimeout");
        window.setTimeout(call_ajax, 900);
    }

    // racing starts; don't refresh the page automatically anymore.
    if (jsn.status === "r") {
        $("#twocols").hide();
        $("#racescreen").show();
        LOG("jsn.status r");
        start_race(jsn.players);
    }
}

function call_ajax() {
    LOG("call_ajax");
    $.ajax(
        { url: $("#json_url").html() + '?r=' + Math.random() }
    ).done(
        function(result) {
            process_ajax(result.data);
        }
    );
}


