ready = ->
    window.render_map = (candidate) ->
        window.current_candidate = candidate

        # Remove old map from DOM.
        $('#map-container').replaceWith('<div id="map-container"></div>')

        $('#candidate-name').text(candidate)

        minValue = 40
        maxValue = 60
        paletteScale = d3.scale.linear().domain([minValue,maxValue]).range(["#FFEFEF","#6F0202"])

        for c, c_data of MAP_DATA
            for state, state_data of c_data
                state_data['fillColor'] = paletteScale(state_data['sentiment'])

        map = new Datamap
            element: document.getElementById 'map-container'
            scope: 'usa'
            fills:
                defaultFill: '#F7F7F7'
            data:
                MAP_DATA[candidate]
            geographyConfig:
                borderColor: '#F5F5F5'
                highlightBorderWidth: 2
                highlightFillColor: (geo) ->
                    return geo['fillColor'] || '#F5F5F5'
                highlightBorderColor: '#B7B7B7'
                popupTemplate: (geo, data) ->
                    data = MAP_DATA[candidate][geo.id]
                    if not data
                        sentiment = "N/A"
                        total_tweets = 0
                    else
                        sentiment = _.round(data['sentiment']) + "/100"
                        total_tweets = data['total_tweets']
                    element = [
                        '<div class="hoverinfo">',
                        '<h6>' + geo.properties.name + '</h6>',
                        '<span>Sentiment: <strong>' + sentiment + '</strong></span><br>',
                        '<span>Total Tweets: <strong>' + total_tweets + '</strong></span><br>',
                        '</div>'].join ''
                    return element

        $('.candidates').removeClass('selected')
        $('#' + candidate.replace(' ', '-')).addClass('selected')

    window.render_map(_.keys(MAP_DATA)[0])

    # The render allows the new css sizes to apply to the element.
    $(window).resize ->
        console.log ("RESIZE")
        window.render_map(window.current_candidate)
    
    

$(document).ready(ready)
$(document).on('page:load', ready)
