ready = ->
    window.render_map = (candidate) ->
        window.current_candidate = candidate

        # Remove old map from DOM.
        $('#map-container').replaceWith('<div id="map-container"></div>')

        minValue = 0
        maxValue = 100
        paletteScale = d3.scale.linear().domain([minValue,maxValue]).range(["#EFEFFF","#02386F"])

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
                    return ['<div class="hoverinfo"><strong>',
                            geo.properties.name + " sentiment",
                            ': ' + _.round(data['sentiment']) + "/100",
                            '</strong><br>',
                            "<i>Total Tweets: " + data['total_tweets'],
                            '</div>'].join ''

        return
    

$(document).ready(ready)
$(document).on('page:load', ready)
