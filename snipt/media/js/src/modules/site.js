(function(Site) {

    var Snipt = snipt.module('snipt');

    SiteView = Backbone.View.extend({
        el: 'body',

        initialize: function(opts) {

            this.$search_query = $('input#search-query', this.el);
            this.$snipts = $('section#snipts article.snipt', this.el);

            this.keyboardShortcuts();
            this.inFieldLabels();

            // Init snipts
            if (this.$snipts.length) {
                SniptListView = Snipt.Views.SniptListView;
                SniptList = new SniptListView({ 'snipts': this.$snipts });
            }

            // Search
            this.$search_query.focus(function() {
                if (window.$selected) {
                    $selected.trigger('deselect');
                }
            });

        },
        keyboardShortcuts: function() {

            $search_query = this.$search_query;

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
            $('div.infield label', this.el).inFieldLabels({
                fadeDuration: 200
            });
        }
    });

    Site.Views = {
        'SiteView': SiteView
    };

})(snipt.module('site'));
