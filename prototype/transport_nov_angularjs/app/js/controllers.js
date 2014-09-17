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
        }
}]);
