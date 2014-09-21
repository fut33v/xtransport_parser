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
            $scope.checkedStations = [];
            $scope.checkedStationsInit = [0];
            console.log("Хуёк!");
            for (var i=0; i < $scope.currentBus.stations.length; i++) {
                $scope.checkedStations.push($scope.currentBus.stations[i].id);
            }
            console.log($scope.checkedStations);
        });
        
        
        this.isStationChecked = function(station) {
            /* var fitsQuery = [];
            fitsQuery = $filter('filter')($scope.currentBus.stations, $scope.query);
            if (fitsQuery.length) {             
                for (var i=0; i < fitsQuery.length; i++){
                    console.log(station);
                    console.log(fitsQuery[i]);
                    if (fitsQuery[i] === station) {
                        this.currentStation = i; 
                        return true; 
                    }
                }
            }
            return false; */
            for (var i=0; i < $scope.checkedStations.length; i++) {
                if (station.id === $scope.checkedStations[i]) {
                    return true;
                }
                console.log(station.id);
            }
            return false;
        }
}])
    .directive("checkboxGroup", function() {
    return {
        restrict: "A",
        link: function (scope, elem, attrs) {
            // Update array on click
            elem.bind('click', function () {
                if (scope.checkedStationsInit.length) { 
                    console.log("1", scope.checkedStationsInit);
                    while(scope.checkedStations.length > 0) {
                        scope.checkedStations.pop(); 
                    }
                    while(scope.checkedStationsInit.length > 0) {
                        scope.checkedStationsInit.pop(); 
                    }
                }
                // Add if checked
                if (elem[0].checked) {
                    scope.checkedStations.push(scope.station.id);
                }
                // Remove if unchecked
                else {
                    var index = scope.checkedStations.indexOf(scope.station.id);
                    scope.checkedStations.splice(index, 1);
                }
                console.log(scope.checkedStations);
            });
        }
    }
});
