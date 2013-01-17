$(function() {

    var $aside = $('aside');

    // Convert "View more" links into nicer links.
    $('a:contains("View more")', $aside).addClass('more');

    // Populate any GitTip widgets.
    if (window.gittip_username) {
        $aside.html($aside.html().replace(
           '[[gittip]]',
           '<iframe style="border: 0; margin: 0; padding: 0;" src="https://www.gittip.com/' + window.gittip_username + '/widget.html" width="48pt" height="22pt"></iframe>')
        );
        $('iframe', $aside).parent('p').prev('p').css('margin-bottom', '10px');
    }

});
