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

transportControllers.controller('BusScheduleController', ['$scope', '$http', '$routeParams', '$filter',
    function($scope, $http, $routeParams, $filter) {
        $scope.busId = $routeParams.busId;
        $http.get('transport/schedules/' + $scope.busId + ".json").
            success(function(data) {
             // console.log(data); 
             $scope.busSchedule = data; 
        });
        $http.get('transport/buses.json').
            success(function(data) {
                // console.log(data); 
            $scope.buses = data; 
            $scope.stationsSchedule = []; 
            for (var i=0; i < data.length; i++) { 
                if (data[i].id === $scope.busId) {
                    $scope.currentBus = data[i];
                }
                // loop through the current bus schedule  
                for (var j=0; j < data[i].schedule.length; j++) {
                    // loop through the bus instance
                    for(var x=0; x < data[i].schedule[j].length; x++) {
                        $scope.stationsSchedule[x][j] = data[i].schedule[j][x]; 
                    }     
                }
            }
            console.log($scope.stationsSchedule);
        });
        this.isStationSearched = function(station) {
            var fitsQuery = [];
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
            return false;
             //return $filter('filter')($scope.currentBus.stations, $scope.query).length;
        }
}]);
