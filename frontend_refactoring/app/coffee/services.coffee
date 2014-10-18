transportServices = angular.module 'transportServices', []

transportServices.factory 'TransportManager', [
  '$http',
  ($http) ->
    new class TransportManager
      constructor: (@$scope) ->
        console.log "TransportManager constructor invoked"
      
      getTransportList: () ->
        $http.get('json/transport.json').success (data) ->
          console.log data
      
      getBus: (bus_id) ->
        $http.get('json/buses/' + bus_id + '.json').success (data) ->
          console.log data
      
      getTrolley: (bus_id) ->
        $http.get('json/trolleys/' + bus_id + '.json').success (data) ->
          console.log data
      
      getTransport: (transportId) ->
        $http.get('json/transport/' + transportId + '.json').success (data) ->
          console.log data
]
