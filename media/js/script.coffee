$ =>
    $(document).bind('keyup', '/', -> $('input#search-query').focus() )

    $('div.infield label').inFieldLabels()

    $('section.code a.expand').click ->
        el = $(this).parent()
        el.toggleClass('expanded')

        if el.hasClass('expanded')
            el.css('height', 'auto')
            $(this).text('Collapse')
        else
            el.css('height', '200px')
            $(this).text('Expand')

        false

    false
