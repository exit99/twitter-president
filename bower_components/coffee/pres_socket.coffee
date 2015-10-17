ready = ->
    socket = io.connect('http://' + document.domain + ':' + location.port + NAMESPACE)

    # This function does nothing but is needed to make socketio work.
    socket.on('connect', -> return)

    socket.on(MSG_NAME, (msg) ->
        $('#log').append('<br>Received #' + msg.count + ': ' + msg.data)
    )
 

$(document).ready(ready)
$(document).on('page:load', ready)
