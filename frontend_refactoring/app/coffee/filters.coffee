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
