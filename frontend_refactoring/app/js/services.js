(function() {
  var transportServices;

  transportServices = angular.module('transportServices', []);

  transportServices.factory('TransportManager', [
    '$http', function($http) {
      var TransportManager;
      return new (TransportManager = (function() {
        function TransportManager() {
          true;
        }

        TransportManager.prototype.getTransportList = function() {
          return $http.get('json/transport.json').success(function(data) {});
        };

        TransportManager.prototype.getBus = function(bus_id) {
          return $http.get('json/buses/' + bus_id + '.json').success(function(data) {});
        };

        TransportManager.prototype.getTrolley = function(bus_id) {
          return $http.get('json/trolleys/' + bus_id + '.json').success(function(data) {});
        };

        TransportManager.prototype.getTransport = function(transportId) {
          return $http.get('json/transport/' + transportId + '.json').success(function(data) {
            if (data.type === 'bus') {
              data.typeName = 'автобусы';
              data.icon = 'img/bus.png';
            }
            if (data.type === 'trolley') {
              data.icon = 'img/trolley.png';
              return data.typeName = 'троллейбусы';
            }
          });
        };

        return TransportManager;

      })());
    }
  ]);

  transportServices.factory('TimeManager', [
    '$http', function($http) {
      var TimeManager;
      return new (TimeManager = (function() {
        function TimeManager() {
          this.daysOfWeek = ["воскресенье", "понедельник", "вторник", "среда", "четверг", "пятница", "суббота"];
          this.workday = "рабочий";
          this.weekend = "выходной";
        }

        TimeManager.prototype.getToday = function() {
          var currentDate, currentDay, dayType, obj, weekend;
          currentDate = new Date();
          currentDay = currentDate.getDay();
          if (currentDay === 0 || currentDay === 6) {
            dayType = this.weekend;
            weekend = true;
          } else {
            dayType = this.workday;
            weekend = false;
          }
          return obj = {
            dayName: this.daysOfWeek[currentDay],
            dayType: dayType,
            weekend: weekend
          };
        };

        return TimeManager;

      })());
    }
  ]);

}).call(this);
