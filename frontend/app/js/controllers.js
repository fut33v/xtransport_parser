(function() {
  var BusesTrolleysController, MainViewController, ScheduleController, ServiceController, TestController, transportControllers;

  transportControllers = angular.module('transportControllers', []);

  TestController = (function() {
    function TestController($scope, TransportManager) {
      this.$scope = $scope;
      this.TransportManager = TransportManager;
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
        $scope.mixedList = transportList['mixed'];
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
    function ScheduleController($scope, $routeParams, $filter, TransportManager, TimeManager, filtertimeFilter) {
      var ctrl, i, _i, _j;
      this.$scope = $scope;
      this.$routeParams = $routeParams;
      this.$filter = $filter;
      this.TransportManager = TransportManager;
      this.TimeManager = TimeManager;
      this.filtertimeFilter = filtertimeFilter;
      ctrl = this;
      TransportManager.getTransport($routeParams.transportId).success(function(data) {
        var currentSchedule, currentStations, currentTransport, station, today, _i, _j, _k, _l, _len, _len1, _len2, _len3, _len4, _len5, _m, _n, _ref, _ref1, _ref2;
        console.log(data);
        ctrl.currentTransport = data;
        currentTransport = data;
        if (currentTransport.schedule_everyday != null) {
          $scope.everydayIsTheSame = true;
          currentSchedule = currentTransport['schedule_everyday'];
          currentStations = currentTransport['stations_everyday'];
          for (_i = 0, _len = currentStations.length; _i < _len; _i++) {
            station = currentStations[_i];
            station.selected = true;
          }
        } else if ((currentTransport.schedule_workdays != null) && (currentTransport.schedule_weekend != null)) {
          today = TimeManager.getToday();
          if (today.weekend) {
            currentSchedule = currentTransport['schedule_weekend'];
            if (currentTransport.stations != null) {
              currentStations = currentTransport.stations;
            } else {
              currentStations = currentTransport.stations_weekend;
            }
            ctrl.selectedDay = 'weekend';
          } else {
            currentSchedule = currentTransport['schedule_workdays'];
            if (currentTransport.stations != null) {
              currentStations = currentTransport.stations;
            } else {
              currentStations = currentTransport['stations_workdays'];
            }
            ctrl.selectedDay = 'workdays';
          }
          if (currentTransport.stations != null) {
            _ref = currentTransport.stations;
            for (_j = 0, _len1 = _ref.length; _j < _len1; _j++) {
              station = _ref[_j];
              station.selected = true;
            }
          } else {
            _ref1 = currentTransport.stations_workdays;
            for (_k = 0, _len2 = _ref1.length; _k < _len2; _k++) {
              station = _ref1[_k];
              station.selected = true;
            }
            _ref2 = currentTransport.stations_weekend;
            for (_l = 0, _len3 = _ref2.length; _l < _len3; _l++) {
              station = _ref2[_l];
              station.selected = true;
            }
          }
        } else if ((currentTransport.schedule_workdays != null) && (currentTransport.schedule_weekend == null)) {
          $scope.workdaysOnly = true;
          currentSchedule = currentTransport.schedule_workdays;
          currentStations = currentTransport.stations_workdays;
          for (_m = 0, _len4 = currentStations.length; _m < _len4; _m++) {
            station = currentStations[_m];
            station.selected = true;
          }
        } else if (!currentTransport.workdays && currentTransport.weekend) {
          $scope.weekendOnly = true;
          currentSchedule = currentTransport.schedule_weekend;
          currentStations = currentTransport.stations_weekend;
          for (_n = 0, _len5 = currentStations.length; _n < _len5; _n++) {
            station = currentStations[_n];
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
      if (this.currentTransport.stations == null) {
        return this.$scope.currentStations = this.currentTransport.stations_workdays;
      }
    };

    ScheduleController.prototype.setCurrentWeekend = function() {
      this.selectedDay = 'weekend';
      this.$scope.currentSchedule = this.currentTransport.schedule_weekend;
      if (this.currentTransport.stations == null) {
        return this.$scope.currentStations = this.currentTransport.stations_weekend;
      }
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
      if (timeSplited.length !== 2) {
        return false;
      }
      hour = parseInt(timeSplited[0]);
      minute = parseInt(timeSplited[1]);
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

    ScheduleController.prototype.showShortDescription = function() {
      if (this.currentTransport != null) {
        if (this.currentTransport.name.length <= 4) {
          return true;
        } else {
          return false;
        }
      }
    };

    ScheduleController.prototype.isStationShown = function(index) {
      var column, filteredSchedule, isEmpty, row, _i, _len;
      filteredSchedule = this.filtertimeFilter(this.$scope.currentSchedule, this.$scope.selectedHour, this.$scope.selectedMinute);
      column = [];
      for (_i = 0, _len = filteredSchedule.length; _i < _len; _i++) {
        row = filteredSchedule[_i];
        column.push(row[index]);
      }
      isEmpty = _.every(column, function(elem) {
        return elem === '-';
      });
      if (isEmpty) {
        return false;
      } else {
        return this.$scope.currentStations[index].selected;
      }
    };

    ScheduleController.prototype.isNoMenu = function() {
      if (this.currentTransport != null) {
        if (this.currentTransport.type === 'mixed') {
          return true;
        } else {
          return false;
        }
      }
    };

    return ScheduleController;

  })();

  ServiceController = (function() {
    function ServiceController($scope, TransportManager) {
      var ctrl;
      this.$scope = $scope;
      this.TransportManager = TransportManager;
      console.log("Hello, Petuh");
      ctrl = this;
      TransportManager.getTransportList().success(function(data) {
        var bus, transportList, trolley, _i, _j, _len, _len1, _ref, _ref1, _results;
        transportList = data;
        $scope.transportList = transportList;
        $scope.allTransport = [];
        _ref = transportList['buses'];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          bus = _ref[_i];
          TransportManager.getTransport(bus.id).success(function(data) {
            $scope.allTransport.push(data);
            return $scope.allTransport = _.reject($scope.allTransport, ctrl.toReject);
          });
        }
        _ref1 = transportList['trolleys'];
        _results = [];
        for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
          trolley = _ref1[_j];
          _results.push(TransportManager.getTransport(trolley.id).success(function(data) {
            $scope.allTransport.push(data);
            return $scope.allTransport = _.reject($scope.allTransport, ctrl.toReject);
          }));
        }
        return _results;
      });
    }

    ServiceController.prototype.isTransportOk = function(transport) {
      return this.isStationsSame(transport) && this.isLengthOk(transport);
    };

    ServiceController.prototype.isStationOk = function(stations_wrkd, stations_wknd, index) {
      if ((stations_wrkd != null) && (stations_wknd != null) && (index != null)) {
        if ((stations_wrkd[index] != null) && stations_wknd[index]) {
          if (stations_wrkd[index].name === stations_wknd[index].name) {
            return true;
          } else {
            return false;
          }
        }
      }
    };

    ServiceController.prototype.isStationsSame = function(transport) {
      var stations_weekend, stations_workdays;
      if ((transport != null) && (transport.stations_workdays != null) && (transport.stations_weekend != null)) {
        stations_workdays = _.pluck(transport.stations_workdays, 'name');
        stations_weekend = _.pluck(transport.stations_weekend, 'name');
        return _.isEqual(stations_workdays, stations_weekend);
      }
    };

    ServiceController.prototype.isLengthOk = function(transport) {
      if ((transport != null) && (transport.stations_workdays != null) && (transport.stations_weekend != null)) {
        if (transport.stations_workdays.length !== transport.stations_weekend.length) {
          return false;
        }
        return true;
      }
    };

    ServiceController.prototype.withDifferentCountOfStations = function() {
      var count, transport, _i, _len, _ref;
      if (this.$scope.allTransport != null) {
        count = 0;
        _ref = this.$scope.allTransport;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          transport = _ref[_i];
          if (!this.isLengthOk(transport)) {
            count += 1;
          }
        }
        return count;
      }
    };

    ServiceController.prototype.withSameStations = function() {
      var count, transport, _i, _len, _ref;
      if (this.$scope.allTransport != null) {
        count = 0;
        _ref = this.$scope.allTransport;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          transport = _ref[_i];
          if (this.isStationsSame(transport)) {
            count += 1;
          }
        }
        return count;
      }
    };

    ServiceController.prototype.isTransportShown = function(transport) {
      if (transport != null) {
        if (this.isStationsSame(transport)) {
          return false;
        }
        if (!this.isLengthOk(transport)) {
          return false;
        }
        return true;
      }
    };

    ServiceController.prototype.toReject = function(transport) {
      if (transport.everyday) {
        return true;
      }
      if (transport.weekend && !transport.workdays) {
        return true;
      }
      if (!transport.weekend && transport.workdays) {
        return true;
      }
      return false;
    };

    return ServiceController;

  })();

  transportControllers.controller('MainViewController', ['$scope', MainViewController]);

  transportControllers.controller('BusesTrolleysController', ['$scope', 'TransportManager', BusesTrolleysController]);

  transportControllers.controller('ScheduleController', ['$scope', '$routeParams', '$filter', 'TransportManager', 'TimeManager', 'filtertimeFilter', ScheduleController]);

  transportControllers.controller('ServiceController', ['$scope', 'TransportManager', ServiceController]);

  transportControllers.controller('TestController', ['$scope', 'TransportManager', TestController]);

}).call(this);
