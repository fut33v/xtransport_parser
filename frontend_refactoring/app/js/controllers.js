(function() {
  var TestController, transportControllers;

  transportControllers = angular.module('transportControllers', []);

  TestController = (function() {
    function TestController($scope) {
      this.$scope = $scope;
      $scope.helloWorld = "Hello world";
    }

    return TestController;

  })();

  transportControllers.controller('TestController', ['$scope', TestController]);

}).call(this);
