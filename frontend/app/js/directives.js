(function() {
  var transportDirectives;

  transportDirectives = angular.module('transportDirectives', []);

  transportDirectives.directive('currentTime', [
    '$interval', 'dateFilter', function($interval, dateFilter) {
      var link, obj;
      link = function(scope, element, attrs) {
        var format, timeoutId, updateTime;
        format = "H:mm";
        updateTime = function() {
          return element.text(dateFilter(new Date(), format));
        };
        element.on('$destroy', function() {
          return $interval.cancel(timeoutId);
        });
        return timeoutId = $interval(function() {
          return updateTime();
        }, 1000);
      };
      return obj = {
        link: link
      };
    }
  ]);

}).call(this);
