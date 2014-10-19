transportControllers = angular.module 'transportControllers', []

class TestController
  constructor: (@$scope, @TransportManager) ->
    TransportManager.getBus('bus_20')
    TransportManager.getTrolley('trolley_2')
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

transportControllers.controller 'TestController', [
  '$scope',
  'TransportManager',
  TestController
]
