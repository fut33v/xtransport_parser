transportControllers = angular.module 'transportControllers', []

class TestController
  constructor: (@$scope, @TransportManager) ->
    TransportManager.getTransportList()
    $scope.helloWorld = "Hello world"


class MainViewController
  constructor: (@$scope) ->
    true


class BusesTrolleysController
  constructor: (@$scope, @TransportManager) ->
    TransportManager.getTransportList().success (data) ->
      $scope.transportList = data
      transportList = data
      $scope.busesList = transportList['buses']
      $scope.mixedList = transportList['mixed']
      $scope.trolleysList = transportList['trolleys']

  showFullName: (bus) ->
    @$scope.showFullName = true
    @$scope.currentBus = bus

  hideFullName: (bus) ->
    @$scope.currentBus = ""


class ScheduleController
  constructor: (
      @$scope,
      @$routeParams,
      @$filter,
      @TransportManager,
      @TimeManager) ->

    ctrl = @

    TransportManager.getTransport($routeParams.transportId).success (data) ->
      console.log data
      ctrl.currentTransport = data
      currentTransport = data

      if currentTransport.weekend
        console.log 'Weekend!'

      if currentTransport.everyday
        $scope.everydayIsTheSame = true
        currentSchedule = currentTransport['schedule_everyday']
        currentStations = currentTransport['stations_everyday']
        station.selected = true for station in currentStations
      else if currentTransport.workdays and currentTransport.weekend
        today = TimeManager.getToday()
        if today.weekend
          currentSchedule = currentTransport['schedule_weekend']
          currentStations = currentTransport['stations_weekend']
          ctrl.selectedDay = 'weekend'
        else
          currentSchedule = currentTransport['schedule_workdays']
          currentStations = currentTransport['stations_workdays']
          ctrl.selectedDay = 'workdays'
        station.selected = true for station in currentTransport['stations_workdays']
        station.selected = true for station in currentTransport['stations_weekend']
      else if currentTransport.workdays and not currentTransport.weekend
        $scope.workdaysOnly = true
        currentSchedule = currentTransport['schedule_workdays']
        currentStations = currentTransport['stations_workdays']
        station.selected = true for station in currentStations
      else if not currentTransport.workdays and currentTransport.weekend
        console.log "hi"
        $scope.weekendOnly = true
        currentSchedule = currentTransport['schedule_weekend']
        currentStations = currentTransport['stations_weekend']
        station.selected = true for station in currentStations

      # ctrl.currentSchedule = currentSchedule
      # ctrl.currentStations = currentStations

      #$scope.currentTransport.typeName
      $scope.currentTransport = currentTransport
      $scope.currentSchedule = currentSchedule
      $scope.currentStations = currentStations

    @today = TimeManager.getToday()
    @initialCheckedStations = true
    $scope.currentDayType = @today.dayType
    $scope.currentDayName = @today.dayName
    $scope.selectedHour = 0
    $scope.selectedMinute = 0
    $scope.highlightOn = true
    $scope.hours = []
    $scope.minutes = []
    $scope.hours.push(i) for i in [0..23]
    $scope.minutes.push(i) for i in [0..59]
    $scope.hideMenu = false

  isSelectedWorkdays: () ->
    if @selectedDay == 'workdays'
      return true
    false

  isSelectedWeekend: () ->
    if @selectedDay == 'weekend'
      return true
    false

  setCurrentWorkdays: () ->
    @selectedDay = 'workdays'
    @$scope.currentSchedule = @currentTransport.schedule_workdays
    @$scope.currentStations = @currentTransport.stations_workdays
    # station.selected = true for station in @$scope.currentStations

  setCurrentWeekend: () ->
    @selectedDay = 'weekend'
    @$scope.currentSchedule = @currentTransport.schedule_weekend
    @$scope.currentStations = @currentTransport.stations_weekend
    # station.selected = true for station in @$scope.currentStations

  setCurrentTime: () ->
    d = new Date()
    h = d.getHours()
    m = d.getMinutes()
    @$scope.selectedHour = h
    @$scope.selectedMinute = m

  setNullTime: () ->
    @$scope.selectedHour = 0
    @$scope.selectedMinute = 0

  setAllStationsChecked: () ->
    for station in @$scope.currentStations
        station.selected = true
    @initialCheckedStations = true

  stationClicked: (selectedStation) ->
    if (@initialCheckedStations)
      for station in @$scope.currentStations
        station.selected = false
      @initialCheckedStations = false

  isTimeExpired: (time) ->
    d = new Date()
    currentHour = d.getHours()
    currentMinute = d.getMinutes()
    timeSplited = time.split(':')
    if timeSplited.length != 2
      return false
    hour = timeSplited[0]
    minute = timeSplited[1]
    # night hours of the next day
    if (hour == 0 || hour == 1)
        return false
    if currentHour > hour
        return true
    else
      if (currentHour == hour && currentMinute > minute)
          return true
    return false

  hideButton: () ->
    if @$scope.hideMenu
      @$scope.hideMenu = false
    else
      @$scope.hideMenu = true

  showShortDescription: () ->
    console.log 'kydax', @currentTransport
    if  @currentTransport.name.length <= 4
      return true
    else
      false

  isNoMenu: () ->
    if @currentTransport.type == 'mixed'
      return true
    else
      false


class ServiceController
  constructor: (
    @$scope,
    @TransportManager
  ) ->
    console.log "Hello, Petuh"
    ctrl = @
    TransportManager.getTransportList().success (data) ->
      transportList = data
      $scope.transportList = transportList
      $scope.allTransport = []
      for bus in transportList['buses']
        TransportManager.getTransport(bus.id).success (data) ->
          $scope.allTransport.push data
          $scope.allTransport = _.reject($scope.allTransport, ctrl.toReject)
      for trolley in transportList['trolleys']
        TransportManager.getTransport(trolley.id).success (data) ->
          $scope.allTransport.push data
          $scope.allTransport = _.reject($scope.allTransport, ctrl.toReject)
 
  isTransportOk: (transport) ->
    return @isStationsSame(transport) and @isLengthOk(transport)

  isStationOk: (stations_wrkd, stations_wknd, index) ->
    if stations_wrkd? and stations_wknd? and index?
      if stations_wrkd[index]? and stations_wknd[index]
        if stations_wrkd[index].name == stations_wknd[index].name
          return true
        else
          false

  isStationsSame: (transport) ->
    if transport? and transport.stations_workdays? and transport.stations_weekend?
      stations_workdays = _.pluck(transport.stations_workdays, 'name')
      stations_weekend = _.pluck(transport.stations_weekend, 'name')
      _.isEqual(stations_workdays, stations_weekend)

  isLengthOk: (transport) ->
    if transport? and transport.stations_workdays? and transport.stations_weekend?
      if transport.stations_workdays.length != transport.stations_weekend.length
        return false
      true
 
  withDifferentCountOfStations: () ->
    if @$scope.allTransport?
      count = 0
      for transport in @$scope.allTransport
        if not @isLengthOk transport
          count += 1
      count

  withSameStations: () ->
    if @$scope.allTransport?
      count = 0
      for transport in @$scope.allTransport
        if @isStationsSame transport
          count += 1
      count

  isTransportShown: (transport) ->
    if transport?
      if @isStationsSame transport
        return false
      if not @isLengthOk transport
        return false
      true

    
  # transport to reject (workdays only, weekend only, same for everyday)
  toReject: (transport) ->
    if transport.everyday
      return true
    if transport.weekend and not transport.workdays
      return true
    if not transport.weekend and transport.workdays
      return true
    false
      

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
  'TimeManager',
  ScheduleController
]

transportControllers.controller 'ServiceController', [
  '$scope',
  'TransportManager',
  ServiceController
]

transportControllers.controller 'TestController', [
  '$scope',
  'TransportManager',
  TestController
]
