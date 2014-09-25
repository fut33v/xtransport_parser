class @Spacer
  print = (text) ->
    console.log(text)

  replaceAll = (text, search, replacement) ->
    text.split(search).join(replacement)

  spacer = (textForSpacer) ->
    upperText = textForSpacer.toUpperCase()
    resultString = []
    resultString.push letter for letter in upperText
    resultString = resultString.toString()
    replaceAll(resultString, ",", " ")

  spaceInputContent = () ->
    inputElement = document.getElementById("not-spaced")
    spacedText = spacer inputElement.value
    outputDiv = document.getElementById("spaced")
    outputDiv.innerHTML = spacer spacedText

  onWindowLoad = () ->
    inputElement = document.getElementById("not-spaced")
    spacedText = spacer inputElement.value
    outputDiv = document.getElementById("spaced")
    outputDiv.innerHTML = spacedText

  window.spaceInputContent = spaceInputContent
  window.onload = onWindowLoad
  # window.onload = spacer("Text")

