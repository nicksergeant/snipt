(function(Site) {

    var Snipt = snipt.module('snipt');

    Backbone.oldSync = Backbone.sync;
    Backbone.Model.prototype.idAttribute = 'resource_uri';
    var addSlash = function(str) {
        return str + ((str.length > 0 && str.charAt(str.length - 1) === '/') ? '' : '/');
    };
    Backbone.sync = function(method, model, options) {
        options.headers = _.extend({
            'Authorization': 'ApiKey ' + window.user + ':' + window.api_key
        }, options.headers);
        return Backbone.oldSync(method, model, options);
    };
    Backbone.Model.prototype.url = function() {
        var url = this.id;
        if (!url) {
            url = this.urlRoot;
            url = url || this.collection && (_.isFunction(this.collection.url) ? this.collection.url() : this.collection.url);

            if (url && this.has('id')) {
                url = addSlash(url) + this.get('id');
            }
        }
        url = url && addSlash(url);

        if (typeof url === 'undefined') {
            url = '/api/private/snipt/';
            this.unset('id', {'silent': true});
            this.unset('user', {'silent': true});
        }
        return url || null;
    };

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

            this.$body.on('click', 'a.close', function() {
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
            this.$search_query.bind('keydown', 'esc', function(e) {
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
