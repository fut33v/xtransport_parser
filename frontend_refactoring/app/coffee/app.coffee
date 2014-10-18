transportApp = angular.module 'transportApp', [
  'ngRoute',
  'transportControllers',
  'transportServices',
  'transportFilters'
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
      .when('/schedule/:transportId', obj=
        templateUrl: 'html/schedule_view.html',
        controller: 'ScheduleController')
      .when('/stops/', obj=
        templateUrl: 'html/stops_view.html',
        controller: 'BusesController')
      .otherwise(obj=
        redirectTo: '/'
      )
]
