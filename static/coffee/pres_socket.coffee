ready = ->
    socket = io.connect('http://' + document.domain + ':' + location.port + NAMESPACE)

    # This function does nothing but is needed to make socketio work.
    socket.on('connect', -> return)

    socket.on(MSG_NAME, (msg) ->
        MAP_DATA[msg.name][msg.state]["sentiment"] = msg.sentiment
        MAP_DATA[msg.name][msg.state]["total_tweets"] = msg.total_tweets
        if window.current_candidate == msg.name
            window.render_map(msg.name)

        $('#log').append('<br>Received #' + msg.sentiment + ': ' + msg.name)
        console.log "HERE"
    )


$(document).ready(ready)
$(document).on('page:load', ready)
