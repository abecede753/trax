var laptimetable;var vehicletable;var vehiclelaptimetable;$(document).ready(function(){vehicletable=$('#vehicletable').DataTable({order:[[0,"asc"]],lengthMenu:[[50,100,10000],[50,100,'all']],});$('#vehicletable tbody').on('click','tr.group',function(){var currentOrder=table.order()[0];if(currentOrder[0]===1&&currentOrder[1]==='asc'){table.order([1,'desc']).draw();}
else{table.order([1,'asc']).draw();}});laptimetable=$('#laptimetable').DataTable({ajax:"laptimes.json",columns:[{data:"vehicle"},{data:{_:"duration.display",sort:"duration.millis"}},{data:"name"},{data:{_:"date.display",sort:"date.timestamp"}}],"deferRender":true});vehiclelaptimetable=$('#vehiclelaptimetable').DataTable({order:[[0,"asc"]],lengthMenu:[[50,100,10000],[50,100,'all']],});$('#loginreg').on('fadeout',function(){$(this).fadeTo("slow",0.1,function(){$(this).trigger('fadein');});});$('#loginreg').on('fadein',function(){$(this).fadeTo("slow",1,function(){$(this).delay(500).trigger('fadeout');});});$('#loginreg').trigger('fadeout');$('.combobox').combobox({bsVersion:'3'});});function convert_from_laptime_to_cc_millis(){"use strict";var value=$("#calc_laptime").val();if(value.indexOf(":")>-1){var items=value.split(":");var millis=parseFloat(items[0])*60+parseFloat(items[1]);}else{var millis=parseFloat(value);}
millis=millis/2.59*1000.0;$("#calc_millis").val(Math.round(millis));}