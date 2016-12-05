$(document).ready(function () {

  // update vehicle class button event
  $('.container .form-group button#vclass-update-btn').click(function (event) {
    const vclass = $('.container  .form-control#vclass :selected').text();
    console.log('updating selected class:', vclass);
    jQuery.ajax({
      url: '/staggeredstart/vehicles',
      type: 'POST',
      cache: false,
      timeout: 15000,
      success: function (data) {
        updateVehicleList(data);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.error('error ' + textStatus + " " + errorThrown);
      },
      data: { "vclass": vclass }
    });
  });

  function submitBtn() { return $('.container form .btn#submit'); };
  // compute start times button event
  submitBtn().click(function (event) {
    const selectedRows = $('.container form table#vehicles tr').has('td > input:checked');
    const selectedVehicles = [];
    selectedRows.each(function (i) {
      const time = $(this).data('laptime');
      const name = $(this).children('td').eq(1).text();
      selectedVehicles.push({ name: name, time: time });
    });
    const offset = $('.container form #startoffset').val();
    const tracklength = $('.container form #tracklength').val();
    const numlaps = $('.container form #numlaps').val();
    const overtakedeficit = $('.container form #overtakedeficit').val();
    console.log('offset:', offset, '- tracklength:', tracklength, '- numlaps:', numlaps, '- overtakedeficit:', overtakedeficit);
    const startTimes = computeStartingTimes(selectedVehicles, offset, numlaps, tracklength, overtakedeficit);
    // add starting times to results display
    const table = $('.container #results #starttimes tbody');
    table.empty();
    startTimes.forEach(function (v) {
      const tr = $('<tr><td>' + formattedTime(v.start, 0) + '</td><td>' + v.name + '</td></tr>');
      tr.data('starttime', v.start);
      const pmButtons = $('<td><button type="button" class="btn btn-sm btn-secondary">-</button>' +
        '<button type="button" class="btn btn-sm btn-secondary">+</button>');
      pmButtons.children('button').click(function (event) { // plus minus click event
        const sign = $(this).text() == '+' ? 1 : -1;
        const start = Math.max(0, tr.data('starttime') + sign * 1000);
        tr.data('starttime', start);
        tr.children('td').first().text(formattedTime(start, 0));
        insertStarttimeOrdered(tr, start); // order may change
      });
      tr.append(pmButtons);
      table.append(tr);
    });
    $('.container #results').prop('hidden', false);
  });

  function insertStarttimeOrdered(tr, starttime) {
    const laterRows = tr.siblings().filter(function () {
      return $(this).data('starttime') > starttime;
    });
    const first = laterRows[0];
    if (first) {
      tr.detach().insertBefore(first);
    } else {
      const table = tr.parent();
      tr.detach().appendTo(table);
    }
  }

//  function sortTableRows(table) {
//    table.children('tr').toArray().map(function (tr) {
//      return $(tr);
//    }).sort(function ($a, $b) {
//      return $a.data('starttime') - $b.data('starttime');
//    }).forEach(function ($tr) {
//      $tr.detach().appendTo(table);
//    });
//  }

  // addVehicle button event
  function addVehicle() { return $('.container .form-group table #addVehicle'); };
  addVehicle().find('.btn#addVehicleBtn').click(function (event) {
    //console.log('add button clicked');
    const addVehicleTime = addVehicle().find('input#addVehicleTime');
    // validate input
    const time = parseTime(addVehicleTime.val());
    if (!time) { // invalid time
      addVehicleTime.addClass('form-control-danger');
      addVehicleTime.parent().addClass('has-danger');
    } else { // valid time, proceed
      addVehicleTime.removeClass('form-control-danger');
      addVehicleTime.parent().removeClass('has-danger');
      addVehicleTime.val('');
      const addVehicleName = addVehicle().find('input#addVehicleName');
      const name = addVehicleName.val();
      addVehicleName.val('');
      // add custom element
      const removeBtn = $('<button type="button" class="btn btn-sm btn-secondary">Remove</button>');
      const tr = $('<tr><td><input type="checkbox" checked></td><td>' +
        name + '</td><td>' + formattedTime(time, 3) + '</td><td></td></tr>');
      tr.data('laptime', time);
      tr.find('td').last().append(removeBtn);
      addRowClick(tr); // row click event
      removeBtn.click(function (event) { // remove button event
        tr.remove();
      });
      tr.insertBefore(addVehicle());
      addVehicleName.focus();
    }
  });

  // TODO copied from server
  function parseTime(time) {
    const m = time.match(/(?:(\d\d?):)?(\d+)(?:.(\d*))?/);
    if (!m) {
      return null;
    } else {
      var min = m[1] || 0;
      var sec = m[2] || 0;
      var mil = m[3] || 0;
      mil = (mil + '000').substr(0, 3); // pad to 3 digits
      return (Number(min) * 60 + Number(sec)) * 1000 + Number(mil);
    }
  }

  function computeStartingTimes(vehicles, offset, numlaps, tracklength, overtakedeficit) {
    vehicles.sort(function (a, b) { return b.time - a.time; });
    const ccgpLength = 1.61; // miles
    if (vehicles.length == 0) {
      console.log('nothing selected');
      return [];
    } else {
      function raceTime(laptime) {
        return Math.round(laptime * numlaps * tracklength / ccgpLength);
      };
      function overtakeTime(v1, v2) {
        // magic formula; just doing some scaling to account for extreme lap time differences
        // i.e. if cars are similarly fast: full deficit,
        // if cars are extremely different: deficit closer to zero (as overtaking will be easier and take less time).
        const delta = Math.abs(v2.time - v1.time) / 1000;
        return Math.round(1000 * overtakedeficit / (1 + 0.03 * delta * delta));
      }
      function clamp(time) { // round to seconds; TODO could be done smarter
        return Math.round(time / 1000) * 1000;
      };
      const raceEnd = offset * 1000 + raceTime(vehicles[0].time); // slowest vehicle
      console.log('estimated finish time:', formattedTime(raceEnd, 3));
      var startTimePrev = 0;
      return vehicles.map(function (v, i) {
        // TODO account for number of players
        var rTime = raceTime(v.time);
        for (j = 0; j < i; j++) {
          rTime += overtakeTime(v, vehicles[j]);
        }
        const startTime = Math.max(raceEnd - rTime, startTimePrev); // don't start in front of slower car
        startTimePrev = startTime;
        return { name: v.name, start: clamp(startTime) };
      });
    }
  }

  function formattedTime(millis, digits) {
    const min = Math.floor(millis / 60000);
    const sec = Math.floor((millis % 60000) / 1000);
    const mil = millis % 1000;
    return min + ':' + ('0' + sec).substr(-2) + (digits ? '.' + ('00' + mil).substr(-digits) : ''); // no rounding done here
  }

  function updateVehicleList(vehicles) {
    const list = $('.container table#vehicles > tbody');
    list.contents().filter(function () { // remove all children but addVehicle
      return !$(this).is('#addVehicle');
    }).remove();
    const addVehicle = list.find('#addVehicle');
    vehicles.forEach(function (v) {
      const tr = $('<tr><td><input type="checkbox"></td><td>' +
        v.name + '</td><td>' + formattedTime(v.time, 3) + '</td></tr>');
      tr.data('laptime', v.time);
      tr.insertBefore(addVehicle);
      addRowClick(tr);
    });
    list.parent().prop('hidden', false);
    submitBtn().prop('disabled', false); // enable button
  }

  // allow clicking anywhere in table row
  function addRowClick(tr) {
    tr.click(function (event) {
      const input = $(this).find('input[type=checkbox]');
      if (event.target != input[0]) { // abort if checkbox was clicked
        //console.log('row clicked');
        input.prop('checked', function(_, b) { return !b; });
      } else {
        //console.log('checkbox clicked');
      }
    });
  }

});
