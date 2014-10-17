transportControllers = angular.module 'transportControllers', []

class TestController
  constructor: (@$scope) ->
    $scope.helloWorld = "Hello world"


transportControllers.controller 'TestController', [
  '$scope',
  TestController
]
