ready = ->
    map = new Datamap

        element: document.getElementById 'container'

        scope: 'usa'

        fills:
            1: "#FF0000"
            2: "#FF3C3C"
            3: "#FF7777"
            4: "#FFBBBB"
            5: "#FFDFDF"
            6: "#DFEBFF"
            7: "#A9C9FF"
            8: "#74A8FF"
            9: "#3380FF"
            10: "#0060FF"
            defaultFill: 'green'

        data:
            FL:
                fillKey: 1
                numberOfThings: 10381
            TX:
                fillKey: 7,
                numberOfThings: 3000

        geographyConfig:
            popupTemplate: (geo, data) ->
                return ['<div class="hoverinfo"><strong>',
                        'Number of things in ' + geo.properties.name,
                        ': ' + data.numberOfThings,
                        '</strong></div>'].join ''

    map.legend()
    return

$(document).ready(ready)
$(document).on('page:load', ready)
