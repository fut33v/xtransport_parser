transportControllers = angular.module 'transportControllers', []

class TestController
  constructor: (@$scope, @TransportManager) ->
    TransportManager.getBus('bus_20')
    TransportManager.getTrolley('trolley_2')
    TransportManager.getTransportList()
    $scope.helloWorld = "Hello world"

class MainViewController
  constructor: (@$scope) ->
    console.log "Hello, I'm MainViewController"

class BusesTrolleysController
  constructor: (@$scope, @TransportManager) ->
    ctrlBusesTrolleysController = @
    TransportManager.getTransportList().success (data) ->
      $scope.transportList = data
      transportList = data
      $scope.busesList = transportList['buses']
      $scope.trolleysList = transportList['trolleys']
      # ctrlBusesTrolleysController.

    console.log "Hello, I'm BusesTrolleysController"

  showFullName: (bus) ->
    console.log "hi"
    @$scope.showFullName = true
    @$scope.currentBus = bus

  hideFullName: (bus) ->
    @$scope.currentBus = ""

class ScheduleController
  constructor: (@$scope, @$routeParams, @$filter,  @TransportManager) ->
    TransportManager.getTransport($routeParams.transportId).success (data) ->
      $scope.transportObject = data

###############################################################################
transportControllers.controller 'MainViewController', [
  '$scope',
  MainViewController
]

transportControllers.controller 'BusesTrolleysController', [
  '$scope',
  'TransportManager',
  BusesTrolleysController
]

transportControllers.controller 'ScheduleController', [
  '$scope',
  '$routeParams',
  '$filter',
  'TransportManager',
  ScheduleController
]

transportControllers.controller 'TestController', [
  '$scope',
  'TransportManager',
  TestController
]
