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
    }
]);

transportControllers.controller('BusScheduleController', ['$scope', '$http', '$routeParams', '$filter',
    function($scope, $http, $routeParams, $filter) {
        
        $scope.busId = $routeParams.busId;
        $http.get('transport/schedules/' + $scope.busId + ".json").
            success(function(data) {
             $scope.busSchedule = data; 
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
            console.log(h, m);
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

        this.stationClicked = function() {
            console.log('kydax');
            if ($scope.initialCheckedStations) {
                for (var x=0; x < $scope.checkedStations.length; x++) {
                    $scope.checkedStations[x].selected = false;
                }
                $scope.initialCheckedStations = false;
            }
        }
        
        $scope.initialCheckedStations = true; 
        $scope.hideMenu = false;
        $scope.hours = [];
        $scope.minutes = [];
        $scope.selectedHour = 0;
        $scope.selectedMinute = 0;
        $scope.highlightOn = true;
        for (var i=0; i < 24; i++) {
            $scope.hours.push(i);
        }
        for (var i=0; i < 60; i++) {
            $scope.minutes.push(i);
        }

}])
    .directive("checkboxGroup", function() {
    return {
        restrict: "A",
        link: function (scope, elem, attrs) {
            // Update array on click
            elem.bind('click', function () {
                if (scope.checkedStationsInit.length) { 
                    while(scope.checkedStationsInit.length > 0) {
                        scope.checkedStationsInit.pop(); 
                    }
                    for (var x=0; x < scope.checkedStations.length; x++) {
                        scope.checkedStations[x].selected = false;
                    } 
                }
                // Add if checked
                if (elem[0].checked) {
                    for (var x=0; x < scope.checkedStations.length; x++) {
                        if (scope.checkedStations[x].id === scope.station.id) { 
                            scope.checkedStations[x].selected = true;
                        }
                    } 
                    // scope.checkedStations.push(scope.station.id);
                }
                // Remove if unchecked
                else {
                    for (var x=0; x < scope.checkedStations.length; x++) {
                        if (scope.checkedStations[x].id === scope.station.id) { 
                            scope.checkedStations[x].selected = false;
                        }
                    } 
                    // var index = scope.checkedStations.indexOf(scope.station.id);
                    // scope.checkedStations.splice(index, 1);
                }
            });
        }
    }
});
