transportDirectives = angular.module 'transportDirectives', []

transportDirectives.directive 'currentTime', [
  '$interval',
  'dateFilter',
  ($interval, dateFilter) ->
    link = (scope, element, attrs) ->
      format = "H:mm"
      updateTime = () ->
        element.text dateFilter(new Date(), format)

      element.on '$destroy', () ->
        $interval.cancel(timeoutId)

      #start the UI update process; save the timeoutId for canceling
      timeoutId = $interval(
        () ->
          updateTime() # update DOM
        , 1000
      )

    return obj=
      link: link
]
