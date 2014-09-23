'use strict';

/* App Module */
var transportApp = angular.module('transportApp', [
    'ngRoute',
    'transportControllers',
    'oci.fixedHeader'
]);

transportApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: 'html/main_view.html',
            controller: 'MainViewController'
        }).
        when('/buses/', {
            templateUrl: 'html/buses_view.html',
            controller: 'BusesController'
        }).
        when('/buses/:busId', {
            templateUrl: 'html/bus_view.html',
            controller: 'BusScheduleController'
        }).otherwise({
            redirectTo: '/'
        });
    }]);
