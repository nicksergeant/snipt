(function(Snipt) {

    Snipt.SniptModel = Backbone.Model.extend({
        url: '',
        title: ''
    });
    SniptView = Backbone.View.extend({

        initialize: function() {
            this.$el = $(this.el);
            this.$h1 = $('header h1 a', this.$el);

            this.model = new Snipt.SniptModel({
                title: this.$h1.text(),
                url: this.$h1.attr('href')
            });
            this.model.view = this;

            this.$aside = $('aside', this.$el);
            this.$container = $('div.container', this.$el);
            this.$raw = $('div.raw', this.$container);
            this.$tags = $('section.tags ul', this.$aside);
        },
        events: {
            'click a.copy':     'copy',
            'click a.expand':   'expand',
            'click .container': 'clickSelect',
            'copy':             'copy',
            'detail':           'detail',
            'expand':           'expand',
            'next':             'next',
            'prev':             'prev',
            'select':           'select'
        },

        clickSelect: function() {
            this.select(true);
        },
        copy: function() {
            var cmd;
            if (navigator.platform == 'MacPPC' ||
                navigator.platform == 'MacIntel') {
                cmd = 'Cmd';
            }
            else {
                cmd = 'Ctrl';
            }
            window.prompt('Text is selected. To copy: press ' + cmd + '+C then <Enter>', this.$raw.text());
            return false;
        },
        detail: function() {
            window.location = this.model.get('url');
        },
        expand: function() {
            this.$container.toggleClass('expanded', 100);
            this.$tags.toggleClass('expanded');
            return false;
        },
        next: function() {
            nextSnipt = this.$el.next('article.snipt');
            if (nextSnipt.length) {
                return nextSnipt.trigger('select');
            }
        },
        prev: function() {
            prevSnipt = this.$el.prev('article.snipt');
            if (prevSnipt.length) {
                return prevSnipt.trigger('select');
            }
        },
        select: function(fromClick) {

            $('article.selected', SniptList.$el).removeClass('selected');
            this.$el.addClass('selected');

            if (fromClick !== true) {
                if (SniptList.$snipts.index(this.$el) === 0) {
                    $('html, body').animate({
                        scrollTop: 0
                    }, 0);
                } else {
                    $('html, body').animate({
                        scrollTop: this.$el.offset().top - 50
                    }, 0);
                }
            }

            window.$selected = this.$el;
        }
    });
    SniptListView = Backbone.View.extend({
        el: 'section#snipts',

        initialize: function(opts) {

            this.$snipts = opts.snipts;
            this.$snipts.each(this.addSnipt);
            this.$el = $(this.el);

            this.keyboardShortcuts();
        },
        addSnipt: function() {
            model = new SniptView({ el: this });
        },
        keyboardShortcuts: function() {

            $selected = window.selected;
            $snipts = this.$snipts;
            $el = this.$el;

            $(document).bind('keydown', 'c', function() {
                if ($selected) {
                    $selected.trigger('copy');
                }
            });
            $(document).bind('keydown', 'e', function() {
                if ($selected) {
                    if ($selected.hasClass('expandable')) {
                        $selected.trigger('expand');
                    }
                }
            });
            $(document).bind('keydown', 'esc', function() {
                if ($selected) {
                    $selected.removeClass('selected');
                    $selected = false;
                }
            });
            $(document).bind('keydown', 'j', function() {
                if (!$selected) {
                    $snipts.eq(0).trigger('select');
                } else {
                    $selected.trigger('next');
                }
            });
            $(document).bind('keydown', 'k', function() {
                if (!$selected) {
                    $snipts.eq(0).trigger('select');
                } else {
                    $selected.trigger('prev');
                }
            });
            $(document).bind('keydown', 'o', function(e) {
                if ($selected) {
                    $selected.trigger('detail');
                }
            });
            $(document).bind('keydown', 'return', function(e) {
                if ($selected) {
                    $selected.trigger('detail');
                }
            });
        }
    });
    Snipt.Views = {
        'SniptListView': SniptListView
    };

})(snipt.module('snipt'));
