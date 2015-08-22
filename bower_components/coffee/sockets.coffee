ready = ->

    socket = io.connect 'http://' + document.domain + ':' + location.port

    socket.on 'connect', ->
        socket.emit 'my event', data: "I'm connected!"

    socket.on 'message', (msg) ->
        console.log 'got it'


$(document).ready(ready)
$(document).on('page:load', ready)
