
(function(Site) {

    var Snipt = snipt.module('snipt');

    Site.SiteView = Backbone.View.extend({
        el: 'body',

        initialize: function(opts) {

            this.$body = $(this.el);
            this.$html = $('html');
            this.$html_body = this.$body.add(this.$html);
            this.$search_form = $('form.search', this.$body);
            this.$search_query = $('input#search-query', this.$body);
            this.$snipts = $('section#snipts article.snipt', this.$body);
            this.$modals = $('div.modal', this.$snipts);
            this.$main_edit = $('section#main-edit');
            this.$main = $('section#main');

            this.keyboardShortcuts();
            this.inFieldLabels();

            if (this.$snipts.length) {
                var SniptListView = Snipt.SniptListView;
                this.snipt_list = new SniptListView({ 'snipts': this.$snipts });

                this.$body.click(function() {
                    if (!window.ui_halted && !window.from_modal && window.$selected) {
                        window.$selected.trigger('deselect');
                    }
                    if (window.from_modal) {
                        window.from_modal = false;
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
                window.ui_halted = false;
                return false;
            });

            window.ui_halted = false;
        },
        events: {
            'showKeyboardShortcuts': 'showKeyboardShortcuts'
        },

        keyboardShortcuts: function() {
            var $body = this.$body;

            $search_query = this.$search_query;
            $document = $(document);

            $document.bind('keydown', '/', function(e) {
                if (!window.ui_halted) {
                    e.preventDefault();
                    $search_query.focus();
                }
            });
            $document.bind('keydown', 'h', function(e) {
                if (!window.ui_halted) {
                    $body.trigger('showKeyboardShortcuts');
                }
            });
            $document.bind('keydown', 't', function(e) {
                if (!window.ui_halted) {
                    window.open('', '_blank');
                }
            });
            $document.bind('keydown', 'r', function(e) {
                if (!window.ui_halted) {
                    location.reload(true);
                }
            });
            $document.bind('keydown', 'Ctrl+h', function(e) {
                if (!window.ui_halted) {
                    history.go(-1);
                }
            });
            $document.bind('keydown', 'Ctrl+l', function(e) {
                if (!window.ui_halted) {
                    history.go(1);
                }
            });
            $('input').bind('keydown', 'esc', function(e) {
                if (!window.ui_halted) {
                    e.preventDefault();
                    this.blur();
                }
            });
        },
        showKeyboardShortcuts: function() {
            $('#keyboard-shortcuts').modal('toggle');
        },
        inFieldLabels: function () {
            $('div.infield label', this.$body).inFieldLabels({
                fadeDuration: 200
            });
        }
    });

})(snipt.module('site'));
