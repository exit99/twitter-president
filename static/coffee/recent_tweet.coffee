ready = ->
    window.render_recent_tweet = (msg) ->
        for field in ['name', 'sentiment', 'state', 'msg']
            val = msg[field]
            if field == "name"
                val = _.startCase(val)
            if field == "sentiment"
                val = _.round(val).toString() + "/100"
            $(".recent-tweet .tweet-" + field).html(val)


$(document).ready(ready)
$(document).on('page:load', ready)
