transportApp = angular.module 'transportApp', [
  'ngRoute',
  'transportControllers',
  'transportServices',
  'transportDirectives',
  'transportFilters',
  'oci.fixedHeader'
]

transportApp.config [
  '$routeProvider',
  ($routeProvider) ->
    $routeProvider
      .when('/', obj=
        templateUrl: 'html/main_view.html',
        controller: 'MainViewController')
      .when('/buses_trolleys/', obj=
        templateUrl: 'html/buses_trolleys_view.html',
        controller: 'BusesTrolleysController')
      .when('/suburban_transport/', obj=
        templateUrl: 'html/suburban_transport_view.html',
        controller: 'BusesTrolleysController')
      .when('/suburban_transport/:transportId', obj=
        templateUrl: 'html/suburban_schedule_view.html',
        controller: 'SuburbanScheduleController')
      .when('/schedule/:transportId', obj=
        templateUrl: 'html/schedule_view.html',
        controller: 'ScheduleController')
      .when('/stops/', obj=
        templateUrl: 'html/stops_view.html',
        controller: 'BusesController')
      .when('/service/', obj=
        templateUrl: 'html/service_view.html',
        controller: 'ServiceController')
      .otherwise(obj=
        redirectTo: '/'
      )
]
