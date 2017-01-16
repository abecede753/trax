'use strict';if(!Date.now){Date.now=function(){return new Date().getTime();}}
var ServerDateInSync=false;var ServerDate=(function(serverNow){var
scriptLoadTime=Date.now(),URL="/robots.txt",synchronizationIntervalDelay,synchronizationInterval,precision,offset,target=null,synchronizing=false;function ServerDate(){return this?ServerDate:ServerDate.toString();}
ServerDate.parse=Date.parse;ServerDate.UTC=Date.UTC;ServerDate.now=function(){return Date.now()+offset;};["toString","toDateString","toTimeString","toLocaleString","toLocaleDateString","toLocaleTimeString","valueOf","getTime","getFullYear","getUTCFullYear","getMonth","getUTCMonth","getDate","getUTCDate","getDay","getUTCDay","getHours","getUTCHours","getMinutes","getUTCMinutes","getSeconds","getUTCSeconds","getMilliseconds","getUTCMilliseconds","getTimezoneOffset","toUTCString","toISOString","toJSON"].forEach(function(method){ServerDate[method]=function(){return new Date(ServerDate.now())[method]();};});ServerDate.getPrecision=function()
{if(typeof target.precision!="undefined")
return target.precision+Math.abs(target-offset);};ServerDate.amortizationRate=25;ServerDate.amortizationThreshold=100;ServerDate.sync_done=false;Object.defineProperty(ServerDate,"synchronizationIntervalDelay",{get:function(){return synchronizationIntervalDelay;},set:function(value){synchronizationIntervalDelay=value;clearInterval(synchronizationInterval);synchronizationInterval=setInterval(synchronize,ServerDate.synchronizationIntervalDelay);log("Set synchronizationIntervalDelay to "+value+" ms.");}});ServerDate.synchronizationIntervalDelay=60*60*1000;function Offset(value,precision){this.value=value;this.precision=precision;}
Offset.prototype.valueOf=function(){return this.value;};Offset.prototype.toString=function(){return this.value+(typeof this.precision!="undefined"?" +/- "+this.precision:"")+" ms";};function setTarget(newTarget){var message="Set target to "+String(newTarget),delta;if(target)
message+=" ("+(newTarget>target?"+":"-")+" "
+Math.abs(newTarget-target)+" ms)";target=newTarget;log(message+".");delta=Math.abs(target-offset);if(delta>ServerDate.amortizationThreshold){log("Difference between target and offset too high ("+delta
+" ms); skipping amortization.");offset=target;}}
function synchronize(){var iteration=1,requestTime,responseTime,best;function requestSample(){var request=new XMLHttpRequest();request.open("GET",URL+"?x="+Date.now());request.onreadystatechange=function(){if((this.readyState==this.HEADERS_RECEIVED)&&(this.status==200))
responseTime=Date.now();};request.onload=function(){if(this.status==200){try{processSample((new Date(this.getResponseHeader("Date"))).getTime());}
catch(exception){log("Unable to read the server's response.");}}};requestTime=Date.now();request.send();}
function processSample(serverNow){var precision=(responseTime-requestTime)/2,sample=new Offset(serverNow+precision-responseTime,precision);log("sample: "+iteration+", offset: "+String(sample));if((iteration==1)||(precision<=best.precision))
best=sample;if(iteration<10){iteration++;setTimeout(function(){requestSample();},400+Math.round(Math.random()*200));console.log("iteration");}
else{setTarget(best);synchronizing=false;ServerDateInSync=true;}}
if(!synchronizing){synchronizing=true;setTimeout(function(){synchronizing=false;},10*1000);requestSample();}}
function log(message){}
offset=serverNow-scriptLoadTime;if(typeof performance!="undefined"){precision=(scriptLoadTime-performance.timing.domLoading)/2;offset+=precision;}
setTarget(new Offset(offset,precision));setInterval(function()
{var delta=Math.max(-ServerDate.amortizationRate,Math.min(ServerDate.amortizationRate,target-offset));offset+=delta;if(delta)
log("Offset adjusted by "+delta+" ms to "+offset+" ms (target: "
+target.value+" ms).");},1000);window.addEventListener('pageshow',synchronize);synchronize();return ServerDate;})(Date.now());var player=document.getElementById("gogogo");var bell_url="/static/bell.m4a";var DDEBUG;var WindowLoadFinished=false;function LOG(txt){}
function audio_loaded(){player.src=bell_url;$("#testsoundbtn").show();}
function launchApp(l){LOG("AUDIO JQUERY LOADED???");}
function loadAudio(){var audio=new Audio();audio.src=bell_url;audio.preload="auto";audio.volume=1;$(audio).on("loadeddata",launchApp);return audio;}
var bellsound=loadAudio();function enlist_car(btn){$.ajax({url:btn.value}).done(function(data){$(".enlist_btn").removeClass("btn-primary");$(btn).addClass("btn-primary");$("#showvehiclelist").collapse("hide");$("#togglevehiclelist").text(btn.textContent);});}
function greenlight(pk){LOG("imgracer"+pk+" is now green?");}
function usergreenlight(){bellsound.play();$("body").stop().css("background-color","#00FF00").animate({backgroundColor:"#FFFFFF"},5000);}
function teststart(){setTimeout(function(){meSpeak.speak("5",{variant:"f5"});},100);setTimeout(function(){meSpeak.speak("4",{variant:"f5"});},1100);setTimeout(function(){meSpeak.speak("3",{variant:"f5"});},2100);setTimeout(function(){meSpeak.speak("2",{variant:"f5"});},3100);setTimeout(function(){usergreenlight();},5100);}
function getReady(){meSpeak.speak("Get ready!",{variant:"f5",wordgap:5});}
meSpeak.loadConfig("/static/mespeak/mespeak_config.json");meSpeak.loadVoice('/static/mespeak/voices/en/en-us.json');function fill_participants_table(data){var tb=$("#participantsbody");tb.html("");for(idx=0;idx<data.length;idx++){var entry=data[idx];var row=$("<tr />",{}).appendTo(tb);$("<td />",{"text":" ","class":"text-center"}).appendTo(row);$("<td />",{"text":entry.username}).appendTo(row);$("<td />",{"text":entry.vehicle}).appendTo(row);$("<td />",{"text":entry.start_after_first}).appendTo(row);}}
function show_result_form(){console.log("show result form");$("#twocols").hide();$("#racescreen").hide();$("#loading").hide();$("#resultform").show();}
function start_race(data){var tb=$("#racebody");var myself=$("#username").html();var idx;tb.html("");var serverdatenow=ServerDate.now();for(idx=0;idx<data.length;idx+=1){var entry=data[idx];var row=$("<tr />",{}).appendTo(tb);var imgcol=$("<td />",{"class":"text-center"}).appendTo(row);var img=$("<img />",{"src":"/static/red_light.png","style":"width:16px;height:16px","id":"imgracer"+data[idx].pk}).appendTo(imgcol);$("<td />",{"text":data[idx].username}).appendTo(row);$("<td />",{"text":data[idx].vehicle}).appendTo(row);$("<td />",{"text":entry.start_after_first}).appendTo(row);var start_in_millis=data[idx].timestamp-serverdatenow;LOG("start_ts "+data[idx].pk+"="+data[idx].username+" "+start_in_millis);if(data[idx].username===myself){LOG("data[idx].username is myself"+data[idx].username+" = "+myself);if(start_in_millis>8000){meSpeak.speak("You are in position, number "+(idx+1)+".",{variant:"f5",wordgap:5});}
if(start_in_millis>7100){setTimeout(function(){getReady();},start_in_millis-7000);}
if(start_in_millis>5100){setTimeout(function(){meSpeak.speak("5",{variant:"f5",wordgap:0});},start_in_millis-5000);setTimeout(function(){meSpeak.speak("4",{variant:"f5",wordgap:0});},start_in_millis-4000);setTimeout(function(){meSpeak.speak("3",{variant:"f5",wordgap:0});},start_in_millis-3000);setTimeout(function(){meSpeak.speak("2",{variant:"f5",wordgap:0});},start_in_millis-2000);}
if(start_in_millis>400){setTimeout(function(){usergreenlight();},start_in_millis);}}
if(start_in_millis>100){setTimeout('$("#imgracer'+data[idx].pk+'").attr("src", "/static/green_light.png")',start_in_millis);}}
var resultformshow=data[data.length-1].timestamp-serverdatenow+10000;setTimeout(function(){show_result_form();},resultformshow);}
function process_ajax(jsn){LOG("process_ajax");if(jsn.status==="i"||jsn.status==="p"){$("#twocols").show();$("#racescreen").hide();LOG("jsn.status i");fill_participants_table(jsn.players);LOG("settingtimeout");window.setTimeout(call_ajax,1700);}
if(jsn.status==="r"){$("#twocols").hide();$("#racescreen").show();LOG("jsn.status r");start_race(jsn.players);}}
function call_ajax(){LOG("call_ajax");$.ajax({url:$("#json_url").html()+'?r='+Math.random()}).done(function(result){process_ajax(result.data);});}
$(window).load(function(){LOG("window load starting");$("#showvehiclelist").collapse();$("#startraceform").submit(function(event){event.preventDefault();var $form=$(this);var url=$form.attr('action');$.get(url+'?'+$('#startraceform').serialize())});LOG("window load finished");WindowLoadFinished=true;});function wait_for_other_stuff(){var done=true;if(!ServerDateInSync){LOG("Waiting for server time to finish synchronizing.")
done=false;}
if(!ServerDateInSync){LOG("Waiting for window load finish.")
done=false;}
if(!done){setTimeout(wait_for_other_stuff,300);}
else{$("#twocols").show();$("#loading").hide();call_ajax();}}
wait_for_other_stuff();