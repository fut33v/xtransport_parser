transportServices = angular.module 'transportServices', []

transportServices.factory 'TransportManager', [
  '$http',
  ($http) ->
    new class TransportManager
      constructor: () ->
        true
      
      getTransportList: () ->
        $http.get('json/transport.json').success (data) ->
      
      getBus: (bus_id) ->
        $http.get('json/buses/' + bus_id + '.json').success (data) ->
      
      getTrolley: (bus_id) ->
        $http.get('json/trolleys/' + bus_id + '.json').success (data) ->
      
      getTransport: (transportId) ->
        $http.get('json/transport/' + transportId + '.json').success (data) ->
          if data.type == 'bus'
            data.typeName = 'автобусы'
            data.icon = 'img/bus.png'
          if data.type == 'trolley'
            data.icon = 'img/trolley.png'
            data.typeName = 'троллейбусы'
]


transportServices.factory 'TimeManager', [
  '$http',
  ($http) ->
    new class TimeManager
      constructor: () ->
        @daysOfWeek = [
          "воскресенье",
          "понедельник",
          "вторник",
          "среда",
          "четверг",
          "пятница",
          "суббота"
        ]
        @workday = "рабочий"
        @weekend = "выходной"

      getToday:() ->
        currentDate = new Date()
        currentDay = currentDate.getDay()
        if currentDay == 0 or currentDay == 6
          dayType = @weekend
          weekend = true
        else
          dayType = @workday
          weekend = false
        obj =
          dayName: @daysOfWeek[currentDay]
          dayType: dayType
          weekend: weekend
]
