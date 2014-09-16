'use strict';

/* App Module */
var transportApp = angular.module('transportApp', [
    'ngRoute',
    'transportControllers'
]);

transportApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: 'html/main_view.html',
            controller: 'MainViewController'
        }).
        when('/buses/:busId', {
            templateUrl: 'html/bus_view.html',
            controller: 'BusScheduleController'
        }).otherwise({
            redirectTo: '/'
        });
    }]);
