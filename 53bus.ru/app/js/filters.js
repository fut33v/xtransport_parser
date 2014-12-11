(function() {
  var transportFilters;

  transportFilters = angular.module('transportFilters', []);

  transportFilters.filter('ordertransport', function() {
    return function(input) {
      var inputTransport, output, outputTransport, _i, _j, _len, _len1;
      if (input != null) {
        output = [];
        for (_i = 0, _len = input.length; _i < _len; _i++) {
          inputTransport = input[_i];
          output.push(inputTransport);
        }
        for (_j = 0, _len1 = output.length; _j < _len1; _j++) {
          outputTransport = output[_j];
          outputTransport.number = parseInt(outputTransport.name);
        }
        output.sort(function(a, b) {
          if (a.number > b.number) {
            return 1;
          }
          if (a.number < b.number) {
            return -1;
          }
          return 0;
        });
        return output;
      }
    };
  });

  transportFilters.filter('filtertime', function() {
    return function(input, hour, minute) {
      var output, row, scheduleHour, scheduleMinute, time, timeHourMinute, _i, _j, _len, _len1;
      if (hour === 0 && minute === 0) {
        return input;
      }
      output = [];
      for (_i = 0, _len = input.length; _i < _len; _i++) {
        row = input[_i];
        for (_j = 0, _len1 = row.length; _j < _len1; _j++) {
          time = row[_j];
          timeHourMinute = time.split(':');
          scheduleHour = parseInt(timeHourMinute[0]);
          scheduleMinute = parseInt(timeHourMinute[1]);
          if (scheduleHour > hour) {
            output.push(row);
            break;
          } else if (scheduleHour === hour) {
            if (scheduleMinute >= minute) {
              output.push(row);
              break;
            }
          }
        }
      }
      return output;
    };
  });

  transportFilters.filter('filterTimeSuburban', function() {
    return function(input) {
      var l;
      if (input != null) {
        l = function(i) {
          var hour, minute, obj, time;
          time = i.split(':');
          hour = parseInt(time[0]);
          minute = parseInt(time[1]);
          return obj = {
            hour: hour,
            minute: minute
          };
        };
        input.sort(function(a, b) {
          var t1, t2;
          t1 = l(a);
          t2 = l(b);
          if (t1.hour === t2.hour) {
            if (t1.minute > t2.minute) {
              return 1;
            } else {
              return -1;
            }
          } else if (t1.hour > t2.hour) {
            return 1;
          } else {
            return -1;
          }
        });
        return input;
      }
    };
  });

}).call(this);