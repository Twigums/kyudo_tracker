# get all arrow elements
arrows = document.querySelectorAll('.arrow')

# new var for x and y
offsetX = undefined
offsetY = undefined

i = 0
while i < arrows.length
    arrow = arrows[i]

    # Event listener for when dragging starts
    arrow.addEventListener 'dragstart', (event) ->
        offsetX = event.clientX - (arrow.getBoundingClientRect().left)
        offsetY = event.clientY - (arrow.getBoundingClientRect().top)
        event.dataTransfer.setData 'text/plain', arrow.id

        return

    # Event listener for when dragging ends
    arrow.addEventListener 'dragend', ->

        # reset
        offsetX = offsetY = 0

        return

    i++

# prevents default behavior during dragover
reset_pos = ->
    `var arrows`
    arrows = [
        'arrow1'
        'arrow2'
        'arrow3'
        'arrow4'
    ]

    i = 0
    while i < arrows.length
        document.getElementById(arrows[i]).style.top = '50px'
        document.getElementById(arrows[i]).style.left = 50 * (i + 1) + 'px'
        i++

    return

document.addEventListener 'dragover', (event) ->
    event.preventDefault()

    return

# get id and move arrow to new coordinates
document.addEventListener 'drop', (event) ->
    event.preventDefault()
    id = event.dataTransfer.getData('text/plain')

    arrow = document.getElementById(id)
    newX = event.clientX - offsetX
    newY = event.clientY - offsetY

    imageContainer = document.getElementById('clickArea')
    containerX = imageContainer.getBoundingClientRect().left
    containerY = imageContainer.getBoundingClientRect().top

    arrow.style.left = newX - containerX + 'px'
    arrow.style.top = newY - containerY + 'px'

    return

$(document).ready ->
    setNumber = 1

    # Add click event listener to the Clear Markers button
    $('#clearMarkers').click ->
        $('.currentSet').remove()
        reset_pos()

        return

    $('#endSet').click ->
        `var i`
        `var arrow`
        coords = []
        i = 0
        while i < arrows.length
            arrow = document.getElementById(i)
            arrow_rect = arrow.getBoundingClientRect()
            x = arrow_rect.left + arrow_rect.width / 2
            y = arrow_rect.top + arrow_rect.height / 2
            coords.push
                x: x
                y: y
                i: i

            i++

        $.ajax
            url: '/saveCoordinates'
            type: 'POST'
            data:
                coordinates: coords
                setNumber: setNumber

            success: ->
                console.log 'Coordinates sent to server.'

                return

        reset_pos()
        setNumber++

        return

    # show all button shows all markers (with marker div)
    $('#showAll').click ->
        $('.arrow').show()

        return

    # hide all button hides all markers (with marker div)
    $('#hideAll').click ->
        $('.arrow').hide()

        return

    # downloads plot on client side
    $('#downloadPlot').click ->

        # call server to download plot
        window.open '/generate_marker_plot', '_blank'

        return

    # downloads MA plot on client side
    $('#downloadMA').click ->

        # call server to download plot
        window.open '/generate_ma_plot', '_blank'

        return

    # downloads KMeans plot on client side
    $('#downloadKMeans').click ->
        # call server to download plot
        window.open '/generate_kmeans_plot', '_blank'

        return

    return
