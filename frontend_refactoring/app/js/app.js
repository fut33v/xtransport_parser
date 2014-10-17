(function() {
  var transportApp;

  transportApp = angular.module('transportApp', ['ngRoute', 'transportControllers', 'transportServices', 'transportFilters']);

  transportApp.config([
    '$routeProvider', function($routeProvider) {
      var obj;
      return $routeProvider.when('/', obj = {
        templateUrl: 'html/main_view.html',
        controller: 'MainViewController'
      }).when('/buses_trolleys/', obj = {
        templateUrl: 'html/buses_trolleys_view.html',
        controller: 'BusesTrolleysController'
      }).when('/schedule/:busId', obj = {
        templateUrl: 'html/schedule_view.html',
        controller: 'ScheduleController'
      }).when('/stops/', obj = {
        templateUrl: 'html/stops_view.html',
        controller: 'BusesController'
      }).otherwise(obj = {
        redirectTo: '/'
      });
    }
  ]);

}).call(this);
