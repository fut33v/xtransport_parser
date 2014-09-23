'use strict';

/* Filters */
var transportFilters = angular.module('transportFilters', []);

transportFilters.filter('filtertime', function() {
    return function(input, hour, minute) {
        if (hour == 0 && minute == 0) {
            return input;
        } 
        var output = [];
        for (var i=0; i < input.length; i++) {
            for (var j=0; j < input[i].length; j++) {            
                var time = input[i][j].split(":");
                // console.log(time); 
                var scheduleHour = parseInt(time[0]); 
                var scheduleMinute = parseInt(time[1]); 
                // console.log(scheduleHour, ":", scheduleMinute, "--", hour, ":", minute); 
                if (scheduleHour > hour) {
                    output.push(input[i]);         
                    break;
                } else if (scheduleHour == hour) {
                    if (scheduleMinute >= minute) {
                        output.push(input[i]);         
                        break;
                    }
                }
                // console.log(input[i][j]);
            }
        } 
        console.log(output);
        return output;
    }
});
