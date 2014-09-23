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
            console.log($scope.buses);
        });
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
                        console.log("Хуёк");
                    } 
                }
                // Add if checked
                if (elem[0].checked) {
                    for (var x=0; x < scope.checkedStations.length; x++) {
                        if (scope.checkedStations[x].id === scope.station.id) { 
                            scope.checkedStations[x].selected = true;
                            console.log(scope.checkedStations)
                        }
                    } 
                    // scope.checkedStations.push(scope.station.id);
                }
                // Remove if unchecked
                else {
                    for (var x=0; x < scope.checkedStations.length; x++) {
                        if (scope.checkedStations[x].id === scope.station.id) { 
                            scope.checkedStations[x].selected = false;
                            console.log(scope.checkedStations)
                        }
                    } 
                    // var index = scope.checkedStations.indexOf(scope.station.id);
                    // scope.checkedStations.splice(index, 1);
                }
                // console.log(scope.checkedStations);
            });
        }
    }
});
