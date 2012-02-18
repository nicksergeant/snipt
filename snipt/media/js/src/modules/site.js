
(function(Site) {

    var Snipt = snipt.module('snipt');

    SiteView = Backbone.View.extend({
        el: 'body',

        initialize: function(opts) {

            this.$el = $(this.el);
            this.$search_form = $('form.search', this.$el);
            this.$search_query = $('input#search-query', this.$el);
            this.$snipts = $('section#snipts article.snipt', this.$el);
            this.$copyModals = $('div.copy-modal', this.$snipts);

            this.keyboardShortcuts();
            this.inFieldLabels();

            if (this.$snipts.length) {
                SniptListView = Snipt.Views.SniptListView;
                SniptList = new SniptListView({ 'snipts': this.$snipts });

                $('body').click(function() {
                    if (window.$selected) {
                        window.$selected.trigger('deselect');
                    }
                });
            }

            $search_query = this.$search_query;
            $search_query.focus(function() {
                if (window.$selected) {
                    $selected.trigger('deselect');
                }
            });
            this.$search_form.submit(function() {
                window.location = 'https://www.google.com/search?q=' + $search_query.val() + ' site:snipt.net%20';
                return false;
            });

            $('div.modal a.close').click(function() {
                $(this).parent().parent().modal('hide');
                return false;
            });
        },
        events: {
            'showKeyboardShortcuts': 'showKeyboardShortcuts'
        },

        keyboardShortcuts: function() {
            var $el = this.$el;

            $search_query = this.$search_query;
            $document = $(document);

            $document.bind('keydown', '/', function(e) {
                e.preventDefault();
                $search_query.focus();
            });
            $document.bind('keydown', 'h', function(e) {
                $el.trigger('showKeyboardShortcuts');
            });
            $document.bind('keydown', 't', function(e) {
                window.open('', '_blank');
            });
            $document.bind('keydown', 'r', function(e) {
                location.reload(true);
            });
            $document.bind('keydown', 'Ctrl+h', function(e) {
                history.go(-1);
            });
            $document.bind('keydown', 'Ctrl+l', function(e) {
                history.go(1);
            });
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
