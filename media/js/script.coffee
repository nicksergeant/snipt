$ =>
    $(document).bind('keyup', '/', -> $('input#search-query').focus() )

    $('div.infield label').inFieldLabels()

    false
