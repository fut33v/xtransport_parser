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
                var scheduleHour = parseInt(time[0]); 
                var scheduleMinute = parseInt(time[1]); 
                if (scheduleHour > hour) {
                    output.push(input[i]);         
                    break;
                } else if (scheduleHour == hour) {
                    if (scheduleMinute >= minute) {
                        output.push(input[i]);         
                        break;
                    }
                }
            }
        } 
        return output;
    }
});



transportFilters.filter('orderbuses', function() {
    return function(input) {
        if (input) { 
            var output = [];
            for (var i=0; i < input.length; i++) {
                output.push(input[i]);
            }
            for (var i=0; i < output.length; i++) {
                output[i].number = parseInt(output[i].name);
            }
            output.sort(function(a,b) {
                if (a.number > b.number) {
                    return 1;
                }    
                if (a.number < b.number) {
                    return -1;
                }    
                return 0;
            });
        }
        return output;
    }
});
