'use strict';

/* Directives */

var transportDirectives = angular.module('transportDirectives', []);

transportDirectives.directive('currentTime', [
    '$interval', 
    'dateFilter', 
    function($interval, dateFilter) {
        function link(scope, element, attrs) {
            var format,
            timeoutId;

            format = "H:mm"
            function updateTime() {
                element.text(dateFilter(new Date(), format));
            }

            element.on('$destroy', function() {
                $interval.cancel(timeoutId);
            });

            // start the UI update process; save the timeoutId for canceling
            timeoutId = $interval(function() {
                updateTime(); // update DOM
            }, 1000);
            }

        return {
          link: link
        };
}]);
