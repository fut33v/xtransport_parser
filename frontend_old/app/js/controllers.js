'use strict';

/* Controllers */

var transportControllers = angular.module('transportControllers', []);

transportControllers.controller('MainViewController', ['$scope', '$http', 
    function($scope, $http) {
        $http.get('transport/buses.json').
            success(function(data) {
                $scope.buses = data;
        });    
    
        $http.get('transport/stations.json').
            success(function(data) {
                $scope.stations = data;
        });    
}]);

transportControllers.controller('BusesController', ['$scope', '$http', 
    function($scope, $http) { 
        $http.get('transport/buses.json').
            success(function(data) {
            $scope.buses = data; 
        });
        $scope.nameInInt = function(name) {
            return parseInt(name);
        }
        this.showFullName = function(bus) {
            console.log ("testing", bus);
            $scope.showFullName = true;
            $scope.currentBus = bus;
        }
        this.hideFullName = function(bus) {
            $scope.currentBus = "";
        }
    }
]);

transportControllers.controller('BusScheduleController', ['$scope', '$http', '$routeParams', '$filter',
    function($scope, $http, $routeParams, $filter) {
        
        $scope.busId = $routeParams.busId;

        $http.get('transport/schedules/' + $scope.busId + ".json").
            success(function(data) {
            $scope.busSchedule = data; 
            
            $scope.daysOfWeek = [
                "воскресенье", 
                "понедельник",
                "вторник",
                "среда",
                "четверг",
                "пятница",
                "суббота"
            ]; 
            var currentDate = new Date();
            $scope.currentDay = currentDate.getDay();
            console.log($scope.currentDay);

            if ($scope.currentDay == 0 || $scope.currentDay == 6) {
                $scope.isCurrentDayWeekend = true;
                $scope.dayEndString = "выходной";
            } else {
                $scope.dayEndString = "рабочий";
                $scope.isCurrentDayWeekend = false;
            }

            $scope.isSelectedWorkdays = !$scope.isCurrentDayWeekend;
            if ($scope.isSelectedWorkdays) { 
                $scope.currentSchedule = $scope.busSchedule.schedule;
            } else {
                $scope.currentSchedule = $scope.busSchedule.scheduleWeekend;
            }
        });
        
        $http.get('transport/buses.json').
            success(function(data) {
            $scope.buses = data; 
            for (var i=0; i < $scope.buses.length; i++) {
                if ($scope.busId === $scope.buses[i].id) { 
                    $scope.currentBus = $scope.buses[i];
                }
            }
            $scope.checkedStations = $scope.currentBus.stations;
            for (var x=0; x < $scope.checkedStations.length; x++) {
                $scope.checkedStations[x].selected = true;
            } 
            $scope.checkedStationsInit = [0];
        });
       

        this.hideButton = function() {
            if($scope.hideMenu) {
                $scope.hideMenu = false;
            } else {
                $scope.hideMenu = true;
            }    
        }

        this.setCurrentTime = function() {
            var d = new Date();
            var h = d.getHours();
            var m = d.getMinutes();
            // console.log(h, m);
            $scope.selectedHour = h;
            $scope.selectedMinute = m;
        }
        
        this.setNullTime = function(time) {
            $scope.selectedHour = 0;
            $scope.selectedMinute = 0;
        }
       
        this.isTimeExpired = function(time) {
            var d = new Date();
            var currentHour = d.getHours();
            var currentMinute = d.getMinutes();
            var timeSplited = time.split(':');
            var hour = timeSplited[0];
            var minute = timeSplited[1];
            // @comment: night hours of the next day 
            if (hour == 0 || hour == 1) {
                return false;
            }  
            if (currentHour > hour) {
                return true;
            } else {
                if (currentHour == hour && currentMinute > minute) {
                    return true;
                }
            }
            return false;
        }

        this.setAllStationsChecked = function() {
            for (var x=0; x < $scope.checkedStations.length; x++) {
                $scope.checkedStations[x].selected = true;
            } 
            $scope.initialCheckedStations = true;
        }

        this.stationClicked = function(selectedStation) {
            if ($scope.initialCheckedStations) {
                for (var x=0; x < $scope.checkedStations.length; x++) {
                    $scope.currentBus.stations[x].selected = false;
                }
                $scope.initialCheckedStations = false;
            }
        }

        this.setCurrentWorkdays = function() {
            $scope.isSelectedWorkdays = true; 
            $scope.currentSchedule = $scope.busSchedule.schedule;
        }

        this.setCurrentWeekend = function() {
            $scope.isSelectedWorkdays = false; 
            $scope.currentSchedule = $scope.busSchedule.scheduleWeekend;
        }
      
        $scope.initialCheckedStations = true; 
        $scope.hideMenu = false;
        $scope.hours = [];
        $scope.minutes = [];
        $scope.selectedHour = 0;
        $scope.selectedMinute = 0;
        this.highlightOn = true;
        for (var i=0; i < 24; i++) {
            $scope.hours.push(i);
        }
        for (var i=0; i < 60; i++) {
            $scope.minutes.push(i);
        }
}]);