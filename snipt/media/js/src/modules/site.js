(function(Site) {

    var Snipt = snipt.module('snipt');

    SiteView = Backbone.View.extend({
        el: 'body',

        initialize: function(opts) {

            this.$el = $(this.el);
            this.$search_query = $('input#search-query', this.$el);
            this.$snipts = $('section#snipts article.snipt', this.$el);

            this.keyboardShortcuts();
            this.inFieldLabels();

            // Init snipts
            if (this.$snipts.length) {
                SniptListView = Snipt.Views.SniptListView;
                SniptList = new SniptListView({ 'snipts': this.$snipts });

                $('body').click(function() {
                    if (window.$selected) {
                        window.$selected.trigger('deselect');
                    }
                });
            }

            // Search
            this.$search_query.focus(function() {
                if (window.$selected) {
                    $selected.trigger('deselect');
                }
            });

        },
        events: {
            'showKeyboardShortcuts': 'showKeyboardShortcuts'
        },

        keyboardShortcuts: function() {
            var $el = this.$el;

            $search_query = this.$search_query;
            $document = $(document);

            // Search
            $document.bind('keydown', '/', function(e) {
                e.preventDefault();
                $search_query.focus();
            });

            $document.bind('keydown', 'Shift+/', function(e) {
                $el.trigger('showKeyboardShortcuts');
            });

            // Escape
            $('input').bind('keydown', 'esc', function(e) {
                e.preventDefault();
                this.blur();
            });
        },
        showKeyboardShortcuts: function() {
            $('#keyboard-shortcuts').modal('toggle');
        },
        inFieldLabels: function () {
            $('div.infield label', this.$el).inFieldLabels({
                fadeDuration: 200
            });
        }
    });
    Site.Views = {
        'SiteView': SiteView
    };

})(snipt.module('site'));
