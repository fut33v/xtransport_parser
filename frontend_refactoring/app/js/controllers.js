(function() {
  var BusesTrolleysController, MainViewController, ScheduleController, TestController, transportControllers;

  transportControllers = angular.module('transportControllers', []);

  TestController = (function() {
    function TestController($scope, TransportManager) {
      this.$scope = $scope;
      this.TransportManager = TransportManager;
      TransportManager.getBus('bus_20');
      TransportManager.getTrolley('trolley_2');
      TransportManager.getTransportList();
      $scope.helloWorld = "Hello world";
    }

    return TestController;

  })();

  MainViewController = (function() {
    function MainViewController($scope) {
      this.$scope = $scope;
      true;
    }

    return MainViewController;

  })();

  BusesTrolleysController = (function() {
    function BusesTrolleysController($scope, TransportManager) {
      this.$scope = $scope;
      this.TransportManager = TransportManager;
      TransportManager.getTransportList().success(function(data) {
        var transportList;
        $scope.transportList = data;
        transportList = data;
        $scope.busesList = transportList['buses'];
        return $scope.trolleysList = transportList['trolleys'];
      });
    }

    BusesTrolleysController.prototype.showFullName = function(bus) {
      this.$scope.showFullName = true;
      return this.$scope.currentBus = bus;
    };

    BusesTrolleysController.prototype.hideFullName = function(bus) {
      return this.$scope.currentBus = "";
    };

    return BusesTrolleysController;

  })();

  ScheduleController = (function() {
    function ScheduleController($scope, $routeParams, $filter, TransportManager, TimeManager) {
      var ctrl, i, _i, _j;
      this.$scope = $scope;
      this.$routeParams = $routeParams;
      this.$filter = $filter;
      this.TransportManager = TransportManager;
      this.TimeManager = TimeManager;
      ctrl = this;
      TransportManager.getTransport($routeParams.transportId).success(function(data) {
        var currentSchedule, currentStations, currentTransport, station, today, _i, _j, _k, _l, _len, _len1, _len2, _len3, _ref, _ref1;
        console.log(data);
        ctrl.currentTransport = data;
        currentTransport = data;
        if (currentTransport.weekend) {
          console.log('Weekend!');
        }
        if (currentTransport.everyday) {
          $scope.everydayIsTheSame = true;
          currentSchedule = currentTransport['schedule_everyday'];
          currentStations = currentTransport['stations_everyday'];
          for (_i = 0, _len = currentStations.length; _i < _len; _i++) {
            station = currentStations[_i];
            station.selected = true;
          }
        } else if (currentTransport.workdays && currentTransport.weekend) {
          today = TimeManager.getToday();
          if (today.weekend) {
            currentSchedule = currentTransport['schedule_weekend'];
            currentStations = currentTransport['stations_weekend'];
            ctrl.selectedDay = 'weekend';
          } else {
            currentSchedule = currentTransport['schedule_workdays'];
            currentStations = currentTransport['stations_workdays'];
            ctrl.selectedDay = 'workdays';
          }
          _ref = currentTransport['stations_workdays'];
          for (_j = 0, _len1 = _ref.length; _j < _len1; _j++) {
            station = _ref[_j];
            station.selected = true;
          }
          _ref1 = currentTransport['stations_weekend'];
          for (_k = 0, _len2 = _ref1.length; _k < _len2; _k++) {
            station = _ref1[_k];
            station.selected = true;
          }
        } else if (currentTransport.workdays && !currentTransport.weekend) {
          $scope.workdaysOnly = true;
          currentSchedule = currentTransport['schedule_workdays'];
          currentStations = currentTransport['stations_workdays'];
          for (_l = 0, _len3 = currentStations.length; _l < _len3; _l++) {
            station = currentStations[_l];
            station.selected = true;
          }
        }
        $scope.currentTransport = currentTransport;
        $scope.currentSchedule = currentSchedule;
        return $scope.currentStations = currentStations;
      });
      this.today = TimeManager.getToday();
      this.initialCheckedStations = true;
      $scope.currentDayType = this.today.dayType;
      $scope.currentDayName = this.today.dayName;
      $scope.selectedHour = 0;
      $scope.selectedMinute = 0;
      $scope.highlightOn = true;
      $scope.hours = [];
      $scope.minutes = [];
      for (i = _i = 0; _i <= 23; i = ++_i) {
        $scope.hours.push(i);
      }
      for (i = _j = 0; _j <= 59; i = ++_j) {
        $scope.minutes.push(i);
      }
      $scope.hideMenu = false;
    }

    ScheduleController.prototype.isSelectedWorkdays = function() {
      if (this.selectedDay === 'workdays') {
        return true;
      }
      return false;
    };

    ScheduleController.prototype.isSelectedWeekend = function() {
      if (this.selectedDay === 'weekend') {
        return true;
      }
      return false;
    };

    ScheduleController.prototype.setCurrentWorkdays = function() {
      this.selectedDay = 'workdays';
      this.$scope.currentSchedule = this.currentTransport.schedule_workdays;
      return this.$scope.currentStations = this.currentTransport.stations_workdays;
    };

    ScheduleController.prototype.setCurrentWeekend = function() {
      this.selectedDay = 'weekend';
      this.$scope.currentSchedule = this.currentTransport.schedule_weekend;
      return this.$scope.currentStations = this.currentTransport.stations_weekend;
    };

    ScheduleController.prototype.setCurrentTime = function() {
      var d, h, m;
      d = new Date();
      h = d.getHours();
      m = d.getMinutes();
      this.$scope.selectedHour = h;
      return this.$scope.selectedMinute = m;
    };

    ScheduleController.prototype.setNullTime = function() {
      this.$scope.selectedHour = 0;
      return this.$scope.selectedMinute = 0;
    };

    ScheduleController.prototype.setAllStationsChecked = function() {
      var station, _i, _len, _ref;
      _ref = this.$scope.currentStations;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        station = _ref[_i];
        station.selected = true;
      }
      return this.initialCheckedStations = true;
    };

    ScheduleController.prototype.stationClicked = function(selectedStation) {
      var station, _i, _len, _ref;
      if (this.initialCheckedStations) {
        _ref = this.$scope.currentStations;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          station = _ref[_i];
          station.selected = false;
        }
        return this.initialCheckedStations = false;
      }
    };

    ScheduleController.prototype.isTimeExpired = function(time) {
      var currentHour, currentMinute, d, hour, minute, timeSplited;
      d = new Date();
      currentHour = d.getHours();
      currentMinute = d.getMinutes();
      timeSplited = time.split(':');
      hour = timeSplited[0];
      minute = timeSplited[1];
      if (hour === 0 || hour === 1) {
        return false;
      }
      if (currentHour > hour) {
        return true;
      } else {
        if (currentHour === hour && currentMinute > minute) {
          return true;
        }
      }
      return false;
    };

    ScheduleController.prototype.hideButton = function() {
      if (this.$scope.hideMenu) {
        return this.$scope.hideMenu = false;
      } else {
        return this.$scope.hideMenu = true;
      }
    };

    return ScheduleController;

  })();

  transportControllers.controller('MainViewController', ['$scope', MainViewController]);

  transportControllers.controller('BusesTrolleysController', ['$scope', 'TransportManager', BusesTrolleysController]);

  transportControllers.controller('ScheduleController', ['$scope', '$routeParams', '$filter', 'TransportManager', 'TimeManager', ScheduleController]);

  transportControllers.controller('TestController', ['$scope', 'TransportManager', TestController]);

}).call(this);
