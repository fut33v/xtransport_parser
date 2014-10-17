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

}).call(this);
