(function() {
  var BusesTrolleysController, MainViewController, TestController, transportControllers;

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
      console.log("Hello, I'm MainViewController");
    }

    return MainViewController;

  })();

  BusesTrolleysController = (function() {
    function BusesTrolleysController($scope, TransportManager) {
      var ctrlBusesTrolleysController;
      this.$scope = $scope;
      this.TransportManager = TransportManager;
      ctrlBusesTrolleysController = this;
      TransportManager.getTransportList().success(function(data) {
        var transportList;
        $scope.transportList = data;
        transportList = data;
        $scope.busesList = transportList['buses'];
        return $scope.trolleysList = transportList['trolleys'];
      });
      console.log("Hello, I'm BusesTrolleysController");
    }

    BusesTrolleysController.prototype.showFullName = function(bus) {
      console.log("hi");
      this.$scope.showFullName = true;
      return this.$scope.currentBus = bus;
    };

    BusesTrolleysController.prototype.hideFullName = function(bus) {
      return this.$scope.currentBus = "";
    };

    return BusesTrolleysController;

  })();

  transportControllers.controller('MainViewController', ['$scope', MainViewController]);

  transportControllers.controller('BusesTrolleysController', ['$scope', 'TransportManager', BusesTrolleysController]);

  transportControllers.controller('TestController', ['$scope', 'TransportManager', TestController]);

}).call(this);
