(function(Site) {

    var Snipt = snipt.module('snipt');

    SiteView = Backbone.View.extend({
        el: 'body',

        initialize: function(opts) {

            // Site variables
            $search_query = $('input#search-query', this.el);
            $snipts = $('section#snipts article.snipt', this.el);

            // Init functions
            this.keyboardShortcuts();
            this.inFieldLabels();

            // Init snipts
            if ($snipts.length) {
                SniptListView = Snipt.Views.SniptListView;
                Snipts = new SniptListView({ 'snipts': $snipts });
            }

        },
        keyboardShortcuts: function() {

            // Search
            $(document).bind('keydown', '/', function(e) {
                e.preventDefault();
                $search_query.focus();
            });

            // Escape
            $('input').bind('keydown', 'esc', function(e) {
                e.preventDefault();
                this.blur();
            });
        },
        inFieldLabels: function () {
            $('div.infield label', this.el).inFieldLabels();
        }
    });

    Site.Views = {
        'SiteView': SiteView
    };

})(snipt.module('site'));
