ready = ->

    Candidate = React.createClass
        displayName: "Candidate"

        renderMap: ->
            window.render_map(@props.candidate)

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
                        @props.totalTweets
                    )
                )
            )


    CandidateList = React.createClass
        displayName: "Candidate List"

        getInitialState: ->
            sort_by: "totalTweets"

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
            for candidate, data of @props.mapData
                active_states = 0
                total_tweets = 0
                sentiment = 0
                for state, state_data of data
                    active_states++
                    total_tweets += state_data.total_tweets
                    sentiment += state_data.sentiment
                props = {
                    candidate: candidate
                    sentiment: _.round sentiment / active_states
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

    render_candidates = ->
        container = document.getElementById 'candidate-container'
        React.render React.createElement(CandidateList, { mapData: MAP_DATA }), container

    render_candidates()
    window.render_map(window.initial_candidate)

$(document).ready(ready)
$(document).on('page:load', ready)
