ready = ->

    Candidate = React.createClass
        displayName: "Candidate"

        renderMap: ->
            window.render_map(@props.candidate)

        abbrNum: (number, decPlaces) ->
            Math.pow(10, decPlaces)
            abbrev = [
              'k'
              'm'
              'b'
              't'
            ]
            i = abbrev.length - 1
            while i >= 0
              # Convert array index to "1000", "1000000", etc
              size = Math.pow(10, (i + 1) * 3)
              # If the number is bigger or equal do the abbreviation
              if size <= number
                # Here, we multiply by decPlaces, round, and then divide by decPlaces.
                # This gives us nice rounding to a particular decimal place.
                number = Math.round(number * decPlaces / size) / decPlaces
                # Handle special case where we round up to the next abbreviation
                if number == 1000 and i < abbrev.length - 1
                  number = 1
                  i++
                # Add the letter for the abbreviation
                number += abbrev[i]
                # We are done... stop
                break
              i--
            number

        render: ->
            React.createElement(
                "div",
                {
                    className: "row candidates",
                    onClick: @renderMap,
                    href: "#",
                    id: @props.candidate.replace(' ', '-')
                },
                React.createElement(
                    "div",
                    {className: "col-lg-6 name"},
                    React.createElement(
                        "p",
                        null,
                        _.startCase(@props.candidate)
                    )
                ),
                React.createElement(
                    "div",
                    {className: "col-lg-3 stats"},
                    React.createElement(
                        "p",
                        null,
                        @props.sentiment + "/100"
                    )
                ),
                React.createElement(
                    "div",
                    {className: "col-lg-3 stats"},
                    React.createElement(
                        "p",
                        null,
                        @abbrNum(@props.totalTweets, 2)
                    )
                )
            )


    CandidateList = React.createClass
        displayName: "Candidate List"

        getInitialState: ->
            sort_by: "totalTweets"
            map_data: @props.mapData

        componentDidMount: ->
            @props.socket.on(@props.msgName, @update)

        update: (msg) ->
            @setState map_data: @props.updateMapData(msg)

        sortBy: (e) ->
            @setState sort_by: e.target.id

        makeHeader: ->
            React.createElement(
                "div",
                { "className": "row candidates-header" },
                React.createElement(
                    "div",
                    { "className": "col-lg-6 name" },
                    React.createElement(
                        "p",
                        { id: "candidate", onClick: @sortBy },
                        "Candidate"
                    )
                ),
                React.createElement(
                    "div",
                    { "className": "col-lg-3 stats" },
                    React.createElement(
                        "p",
                        { id: "sentiment", onClick: @sortBy },
                        "National"
                    )
                ),
                React.createElement(
                    "div",
                    { "className": "col-lg-3 stats" },
                    React.createElement(
                        "p",
                        { id: "totalTweets", onClick: @sortBy },
                        "Tweets"
                    )
                )
            )

        makeCandidates: ->
            candidates = []
            for candidate, data of @state.map_data
                total_tweets = 0
                sentiment = 0
                for state, state_data of data
                    total_tweets += state_data.total_tweets
                    sentiment += (state_data.sentiment * state_data.total_tweets)
                props = {
                    candidate: candidate
                    sentiment: _.round sentiment / total_tweets
                    totalTweets: total_tweets
                }
                candidates.push React.createElement(Candidate, props)
            candidates = _.sortBy(candidates, (candidate) =>
                candidate.props[@state.sort_by]
            )
            if @state.sort_by != "candidate"
                candidates.reverse()
            window.initial_candidate = candidates[0].props.candidate
            return candidates
    
        render: ->
            React.createElement(
                "div",
                null,
                @makeHeader(),
                @makeCandidates()
            )

    window.render_candidates = ->
        container = document.getElementById 'candidate-container'
        React.render(React.createElement(CandidateList, {
            mapData: MAP_DATA
            socket: window.socket
            msgName: MSG_NAME
            updateMapData: window.updateMapData
        }), container)

    window.render_candidates()
    window.render_map(window.initial_candidate)

$(document).ready(ready)
$(document).on('page:load', ready)
