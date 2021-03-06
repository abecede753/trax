var player = document.getElementById("gogogo");
var bell_url = "/static/bell.m4a";
var DDEBUG;

var WindowLoadFinished = false;

function LOG(txt) {
//    console.log("SSR: " + txt);
}

function audio_loaded() {
  player.src = bell_url;
  $("#testsoundbtn").show();
}

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
var bellsound = loadAudio();

function enlist_car(btn) {
  $.ajax({url: btn.value})
    .done(function (data) {
      $(".enlist_btn").removeClass("btn-primary");
      $(btn).addClass("btn-primary");
      $("#showvehiclelist").collapse("hide");
      $("#togglevehiclelist").text(btn.textContent);
    });
}

function usergreenlight() {
  bellsound.play();
  $("body")
    .stop()
    .css("background-color", "#00FF00")
    .animate({ backgroundColor: "#FFFFFF"}, 5000);
}

function teststart() {
  setTimeout(function () { meSpeak.speak("5", {variant:"f5"}); }, 100);
  setTimeout(function () { meSpeak.speak("4", {variant:"f5"}); }, 1100);
  setTimeout(function () { meSpeak.speak("3", {variant:"f5"}); }, 2100);
  setTimeout(function () { meSpeak.speak("2", {variant:"f5"}); }, 3100);
  setTimeout(function () { meSpeak.speak("1", {variant:"f5"}); }, 4100);
  setTimeout(function () {
    usergreenlight();
  }, 5100);
}

function getReady() {
  meSpeak.speak("Get ready!", {variant:"f5", wordgap:5});
}

meSpeak.loadConfig("/static/mespeak/mespeak_config.json");
meSpeak.loadVoice('/static/mespeak/voices/en/en-us.json');

function fill_participants_table(data) {
  var tb = $("#participantsbody");
  tb.html("");
  for (var idx = 0; idx < data.length; idx++) {
    var entry = data[idx];
    var row = $("<tr />", {}).appendTo(tb);
    $("<td />", {"text": idx+1, "class": "text-center"}).appendTo(row);
    $("<td />", {"text": entry.username}).appendTo(row);
    if (entry.vehicle == "") {
      $("<td />", {"text": "WAITING..."}).appendTo(row);
      $("<td />", {"text": ""}).appendTo(row);

    } else {
      $("<td />", {"text": entry.vehicle}).appendTo(row);
      $("<td />", {"text": entry.start_after_first}).appendTo(row);
    }
  }
  $("#num_participants").html(data.length);
}

function show_result_form() {
  console.log("show result form");
  $("#twocols").hide();
  $("#racescreen").hide();
  $("#loading").hide();
  $("#resultform").show();
}
function start_race(data) {
  var tb = $("#racebody");
  var myself = $("#username").html();
  tb.html("");
  var serverdatenow = ServerDate.now();
  for (var idx = 0; idx < data.length; idx+=1) {
    var entry = data[idx];
    var row = $("<tr />", {}).appendTo(tb);
    var imgcol = $("<td />", {"class": "text-center"}).appendTo(row);
    var img = $("<img />", {"src": "/static/red_light.png",
      "style": "width:16px;height:16px",
      "id":"imgracer" + data[idx].pk
    }).appendTo(imgcol);
    $("<td />", {"text": (idx + 1) + ": " + data[idx].username}).appendTo(row);
    $("<td />", {"text": data[idx].vehicle}).appendTo(row);
    $("<td />", {"text": entry.start_after_first}).appendTo(row);
    var start_in_millis = data[idx].timestamp - serverdatenow;
    LOG("start_ts " + data[idx].pk + "=" + data[idx].username + " " + start_in_millis);

    if (data[idx].username === myself) {
      LOG("data[idx].username is myself" + data[idx].username + " = " + myself);
      if (start_in_millis > 8000) {
        meSpeak.speak("You are in position, number " + (idx + 1) + ".",
          {variant:"f5", wordgap:5});
      }
      if (start_in_millis > 7100) { setTimeout(function () { getReady(); }, start_in_millis - 7000); }
      if (start_in_millis > 5100) {
        setTimeout(function () { meSpeak.speak("5", {variant:"f5", wordgap:0}); }, start_in_millis - 5000);
        setTimeout(function () { meSpeak.speak("4", {variant:"f5", wordgap:0}); }, start_in_millis - 4000);
        setTimeout(function () { meSpeak.speak("3", {variant:"f5", wordgap:0}); }, start_in_millis - 3000);
        setTimeout(function () { meSpeak.speak("2", {variant:"f5", wordgap:0}); }, start_in_millis - 2000);
        setTimeout(function () { meSpeak.speak("1", {variant:"f5", wordgap:0}); }, start_in_millis - 1000);
      }
      if (start_in_millis > 400) { setTimeout( function() { usergreenlight(); }, start_in_millis ); }
    }
    if (start_in_millis > 100) {
      setTimeout('$("#imgracer' + data[idx].pk + '").attr("src", "/static/green_light.png")', start_in_millis);
    }
  }
  var resultformshow = data[data.length - 1].timestamp - serverdatenow + 10000;
  setTimeout(function() {show_result_form();}, resultformshow);
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
  LOG("window load starting");

  $("#showvehiclelist").collapse();

  $("#startraceform").submit(function(event) {

      /* stop form from submitting normally */
    $("#submitstartraceform").attr('disabled', 'disabled');
    $("#submitstartraceform").text('Please wait...');
    event.preventDefault();

      /* get some values from elements on the page: */
    var $form = $(this);
    var url = $form.attr('action');
    $.get(url + '?' + $('#startraceform').serialize())

  });
  LOG("window load finished");
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
