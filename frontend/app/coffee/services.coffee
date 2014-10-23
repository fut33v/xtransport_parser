transportServices = angular.module 'transportServices', []

transportServices.factory 'TransportManager', [
  '$http',
  ($http) ->
    new class TransportManager
      constructor: () ->
        true
      
      getTransportList: () ->
        $http.get('json/transport.json').success (data) ->
      
      getTransport: (transportId) ->
        $http.get('json/transport/' + transportId + '.json').success (data) ->
          if data.type == 'bus'
            data.icon = 'img/bus.png'
            data.typeName = 'автобусы'
            data.typeNameSingle = 'автобус'
          if data.type == 'trolley'
            data.icon = 'img/trolley.png'
            data.typeName = 'троллейбусы'
            data.typeNameSingle = 'троллейбус'
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