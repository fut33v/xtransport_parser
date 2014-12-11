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

        TransportManager.prototype.getTransport = function(transportId) {
          return $http.get('json/transport/' + transportId + '.json').success(function(data) {
            if (data.type === 'bus') {
              data.icon = 'img/bus.png';
              data.typeName = 'автобусы';
              data.typeNameSingle = 'автобус';
            }
            if (data.type === 'trolley') {
              data.icon = 'img/trolley.png';
              data.typeName = 'троллейбусы';
              return data.typeNameSingle = 'троллейбус';
            }
          });
        };

        TransportManager.prototype.getSuburbanTransport = function() {
          return $http.get('json/suburban_transport.json').success(function(data) {
            return console.log(data);
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
          this.daysOfWeekOutput = [
            {
              name: "Понедельник",
              key: "monday"
            }, {
              name: "Вторник",
              key: "tuesday"
            }, {
              name: "Среда",
              key: "wednesday"
            }, {
              name: "Четверг",
              key: "thursday"
            }, {
              name: "Пятница",
              key: "friday"
            }, {
              name: "Суббота",
              key: "saturday"
            }, {
              name: "Воскресенье",
              key: "sunday"
            }
          ];
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