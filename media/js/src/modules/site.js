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
            this.$aside_nav = $('aside.nav', this.$body);
            this.$aside_nav_ul = $('ul', this.$aside_nav);
            this.$search_form = $('form.search', this.$body);
            this.$search_query = $('input#search-query', this.$body);
            this.$search_page_query = $('input.search-query', this.$body);
            this.$search_queries = this.$search_query.add(this.$search_page_query);
            this.$snipts = $('section#snipts article.snipt', this.$body);
            this.$modals = $('div.modal', this.$snipts);
            this.$main_edit = $('section#main-edit');
            this.$main = $('section#main');
            this.$keyboard_shortcuts = $('#keyboard-shortcuts', this.$body);
            this.$amazon_ads = $('section.amazon', this.$main);

            this.keyboardShortcuts();
            this.inFieldLabels();

            if (this.$amazon_ads.length) {
                this.initAmazonAds();
            }

            var SniptListView = Snipt.SniptListView;
            this.snipt_list = new SniptListView({ 'snipts': this.$snipts });

            var that = this;

            this.$body.click(function() {
                if (!window.ui_halted && !window.from_modal && window.$selected) {
                    window.$selected.trigger('deselect');
                }
                if (window.from_modal) {
                    window.from_modal = false;
                }
                that.$aside_nav.removeClass('open');
            });

            this.$aside_nav_ul.click(function(e) {
                e.stopPropagation();
            });

            $search_queries = this.$search_queries;
            $search_queries.focus(function() {
                if (window.$selected) {
                    $selected.trigger('deselect');
                }
            });

            this.$body.on('click', 'a.close', function() {
                $(this).parent().parent().modal('hide');
                window.ui_halted = false;
                return false;
            });

            this.$keyboard_shortcuts.on('hidden', function() {
                window.ui_halted = false;
            });

            window.ui_halted = false;
        },
        events: {
            'showKeyboardShortcuts': 'showKeyboardShortcuts',
            'click a.mini-profile':  'toggleMiniProfile'
        },

        keyboardShortcuts: function() {
            var $body = this.$body;

            var that = this;

            $search_queries = this.$search_queries;
            $search_page_query = this.$search_page_query;
            $search_query = this.$search_query;
            $document = $(document);

            $document.bind('keydown', '/', function(e) {
                if (!window.ui_halted) {
                    e.preventDefault();
                    if ($body.hasClass('search')) {
                        $search_page_query.focus();
                    } else {
                        $search_query.focus();
                    }
                }
            });
            $document.bind('keydown', 'h', function(e) {
                if (!window.ui_halted) {
                    window.ui_halted = true;
                    $body.trigger('showKeyboardShortcuts');
                } else {
                    if (that.$keyboard_shortcuts.is(':visible')) {
                        that.$keyboard_shortcuts.modal('hide');
                    }
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
            this.$search_queries.bind('keydown', 'esc', function(e) {
                if (!window.ui_halted) {
                    e.preventDefault();
                    this.blur();
                }
            });
        },
        showKeyboardShortcuts: function() {
            this.$keyboard_shortcuts.modal('toggle');
        },
        toggleMiniProfile: function(e) {
            this.$aside_nav.toggleClass('open');
            return false;
        },
        inFieldLabels: function () {
            $('div.infield label', this.$body).inFieldLabels({
                fadeDuration: 200
            });
        },
        initAmazonAds: function() {
            var $more = $('div.more', this.$amazon_ads);
            var that = this;
            var adTemplate = $('script#amazon-ad').html();

            $('a', $more).on('click', function() {
                var $current = $('li:visible', that.$amazon_ads);
                $('li', that.$amazon_ads).hide();

                if ($(this).hasClass('see-previous')) {
                    var $prev = $current.prev();
                    if ($prev.length) {
                        $prev = $prev;
                    } else {
                        $prev = $('li', that.$amazon_ads).eq(-1);
                    }
                    $prev.show();
                } else {
                    var $next = $current.next();
                    if ($next.length) {
                        $next = $next;
                    } else {
                        $next = $('li', that.$amazon_ads).eq(0);
                    }
                    $next.show();
                }
            });

            $.getJSON('/api/public/a/', {'q': window.tag}, function(resp) {
                if (resp.result.length === 0) {
                    $('section.amazon').hide();
                
                } else {
                    var html = '';
                    for (var i = 0; i < resp.result.length; i++) {
                        if (resp.result[i].image) {
                            html += _.template(adTemplate, {
                                url: resp.result[i].url,
                                title: resp.result[i].title,
                                review: resp.result[i].review,
                                image: resp.result[i].image
                            });
                        }
                    }
                    $ul = $('ul', that.$amazon_ads);

                    $ul.hide().html(html);
                    $lis = $('li', $ul);
                    $lis.hide();
                    $lis.eq(0).show();
                    $ul.show();

                    $('div.more span', that.$amazon_ads).text('Books');
                }
            });
        }
    });

})(snipt.module('site'));
