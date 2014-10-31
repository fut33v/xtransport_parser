(function() {
  var transportApp;

  transportApp = angular.module('transportApp', ['ngRoute', 'transportControllers', 'transportServices', 'transportDirectives', 'transportFilters', 'oci.fixedHeader']);

  transportApp.config([
    '$routeProvider', function($routeProvider) {
      var obj;
      return $routeProvider.when('/', obj = {
        templateUrl: 'html/main_view.html'
      }).when('/urban_transport/', obj = {
        templateUrl: 'html/urban_transport_view.html',
        controller: 'UrbanTransportController'
      }).when('/suburban_transport/', obj = {
        templateUrl: 'html/suburban_transport_view.html',
        controller: 'SuburbanTransportController'
      }).when('/suburban_transport/:transportId', obj = {
        templateUrl: 'html/suburban_schedule_view.html',
        controller: 'SuburbanScheduleController'
      }).when('/urban_transport/:transportId', obj = {
        templateUrl: 'html/urban_schedule_view.html',
        controller: 'UrbanScheduleController'
      }).when('/stops/', obj = {
        templateUrl: 'html/stops_view.html',
        controller: 'BusesController'
      }).when('/service/', obj = {
        templateUrl: 'html/service_view.html',
        controller: 'ServiceController'
      }).otherwise(obj = {
        redirectTo: '/'
      });
    }
  ]);

}).call(this);
