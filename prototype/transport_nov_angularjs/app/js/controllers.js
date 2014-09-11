'use strict';

/* Controllers */

var transportApp = angular.module('transportApp', []);

transportApp.controller('BusController', function($http) {
    var busController = this;
    $http({method: 'GET', url: 'transport/buses.json'}).
        success(function(data) {
            busController.buses = data;
        });    
});
