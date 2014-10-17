(function() {
  var transportServices;

  transportServices = angular.module('transportServices', []);

  transportServices.factory('TransportManager', [
    '$http', function($http) {
      var TransportManager;
      return new (TransportManager = (function() {
        function TransportManager($scope) {
          this.$scope = $scope;
          console.log("TransportManager constructor invoked");
        }

        TransportManager.prototype.getTransportList = function() {
          return $http.get('json/transport.json').success(function(data) {
            return console.log(data);
          });
        };

        TransportManager.prototype.getBus = function(bus_id) {
          return $http.get('json/buses/' + bus_id + '.json').success(function(data) {
            return console.log(data);
          });
        };

        TransportManager.prototype.getTrolley = function(bus_id) {
          return $http.get('json/trolleys/' + bus_id + '.json').success(function(data) {
            return console.log(data);
          });
        };

        return TransportManager;

      })());
    }
  ]);

}).call(this);
