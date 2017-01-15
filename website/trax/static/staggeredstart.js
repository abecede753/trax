var player = document.getElementById("gogogo");
var bell_url = "/static/bell.m4a";
var DDEBUG;

var WindowLoadFinished = false;

function LOG(txt) {
//    console.log("SSR: " + txt);
}

function audio_loaded() {
    LOG("audio loaded????????????????");
    player.src = bell_url;
    $("#testsoundbtn").show();
}

//var audio = new Audio();
//audio.addEventListener("canplaythrough", audio_loaded, false);
//audio.src = bell_url;

function launchApp(l) {
    LOG("AUDIO JQUERY LOADED???");
}

  function loadAudio(){
    var audio = new Audio();
    audio.src = bell_url;
    audio.preload = "auto";
    audio.volume = 1;
    $(audio).on("loadeddata", launchApp);  // jQuery checking
    return audio;
  }
LOG("AUDIO SHHHIIIIT START");
var bellsound = loadAudio();
  LOG("AUDIO SHHHIIIIT CALLED");





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
    LOG("imgracer" + pk + " is now green?");
//    $("#imgracer" + pk).attr("src", "/static/green_light.png");
}
function usergreenlight() {
    bellsound.play();
    $("body")
        .stop()
        .css("background-color", "#00FF00")
        .animate({ backgroundColor: "#FFFFFF"}, 5000);
}

function teststart() {
    bellsound.play();
    $("body")
        .stop()
        .css("background-color", "#00FF00")
        .animate({ backgroundColor: "#FFFFFF"}, 5000);
}

function getReady() {
    meSpeak.speak("Get ready!", {variant:"f5", wordgap:5});
}

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
    var serverdatenow = ServerDate.now();
    for (idx = 0; idx < data.length; idx+=1) {
        var entry = data[idx];
        var row = $("<tr />", {}).appendTo(tb);
        var imgcol = $("<td />", {"class": "text-center"}).appendTo(row);
        var img = $("<img />", {"src": "/static/red_light.png",
            "style": "width:16px;height:16px",
            "id":"imgracer" + data[idx].pk
                     }).appendTo(imgcol);
        $("<td />", {"text": data[idx].username}).appendTo(row);
        $("<td />", {"text": data[idx].vehicle}).appendTo(row);
        var start_in_millis = data[idx].timestamp - serverdatenow;
        LOG("start_ts " + data[idx].pk + "=" + data[idx].username + " " + start_in_millis);

        if (data[idx].username === myself) {
            LOG("data[idx].username is myself" + data[idx].username + " = " + myself);
            if (start_in_millis > 9000) {
                meSpeak.speak("You are in position, number " + (idx + 1) + ".",
                    {variant:"f5", wordgap:5});
            }
            if (start_in_millis > 5100) {
                setTimeout(function () { getReady(); }, start_in_millis - 5000);
            }
            if (start_in_millis > 2100) {
                setTimeout( function() { usergreenlight(); }, start_in_millis );
            }
        }
        if (start_in_millis > 2100) {
            setTimeout('$("#imgracer' + data[idx].pk + '").attr("src", "/static/green_light.png")', start_in_millis);
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
        window.setTimeout(call_ajax, 1700);
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


$(window).load(function() {
    console.log("window load starting");

    $("#showvehiclelist").collapse();

    $("#startraceform").submit(function(event) {

        /* stop form from submitting normally */
        event.preventDefault();

        /* get some values from elements on the page: */
        var $form = $(this);
        var url = $form.attr('action');
        $.get(url + '?' + $('#startraceform').serialize())

    });
    console.log("window load finished");
    WindowLoadFinished = true;
//    $("#twocols").show();
//    $("#loading").hide();
});

function wait_for_other_stuff() {
    var done = true;
    if (!ServerDateInSync) {
        LOG("Waiting for server time to finish synchronizing.")
        done = false;
    }
    if (!ServerDateInSync) {
        LOG("Waiting for window load finish.")
        done = false;
    }
    if (!done) { setTimeout(wait_for_other_stuff, 300);}
    else {
        $("#twocols").show();
        $("#loading").hide();
        call_ajax();
    }
}
wait_for_other_stuff();
