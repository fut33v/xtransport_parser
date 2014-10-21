transportFilters = angular.module 'transportFilters', []

transportFilters.filter 'ordertransport', () ->
  (input) ->
    if input?
      output = []
      output.push inputTransport for inputTransport in input
      outputTransport.number = parseInt(outputTransport.name) for outputTransport in output
      output.sort (a,b) ->
        if (a.number > b.number)
            return 1
        if (a.number < b.number)
            return -1
        return 0
      return output

transportFilters.filter 'filtertime', () ->
  (input, hour, minute) ->
    if (hour == 0 && minute == 0)
      return input
    output = []
    for row in input
      for time in row
        timeHourMinute = time.split ':'
        scheduleHour = parseInt timeHourMinute[0]
        scheduleMinute = parseInt timeHourMinute[1]
        if scheduleHour > hour
          output.push row
          break
        else if scheduleHour == hour
          if scheduleMinute >= minute
            output.push row
            break
    output
