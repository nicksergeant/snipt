
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
            'click .container': 'selectFromClick',
            'copy':             'copy',
            'detail':           'detail',
            'deselect':         'deselect',
            'expand':           'expand',
            'next':             'next',
            'prev':             'prev',
            'select':           'select'
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
        deselect: function() {
            this.$el.removeClass('selected');
            window.$selected = false;
        },
        detail: function() {
            window.location = this.model.get('url');
        },
        expand: function() {
            this.$container.toggleClass('expanded', 100);
            this.$tags.toggleClass('expanded');
            this.select();
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
                    window.scrollTo(0, 0);
                } else {
                    $('html, body').animate({
                        scrollTop: this.$el.offset().top - 50
                    }, 0);
                }
            }

            window.$selected = this.$el;
        },
        selectFromClick: function(e) {
            this.select(true);
            e.stopPropagation();
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
            $document = $(document);

            $document.bind('keydown', 'c', function() {
                if ($selected) {
                    $selected.trigger('copy');
                }
            });
            $document.bind('keydown', 'e', function() {
                if ($selected) {
                    if ($selected.hasClass('expandable')) {
                        $selected.trigger('expand');
                    }
                }
            });
            $document.bind('keydown', 'esc', function() {
                if ($selected) {
                    $selected.trigger('deselect');
                }
            });
            $document.bind('keydown', 'g', function() {
                if (window.$selected) {
                    window.$selected.trigger('deselect');
                }
                window.scrollTo(0, 0);
            });
            $document.bind('keydown', 'Shift+g', function() {
                if (window.$selected) {
                    window.$selected.trigger('deselect');
                }
                window.scrollTo(0, document.body.scrollHeight);
            });
            $document.bind('keydown', 'h', function() {
                window.location = '/';
            });
            $document.bind('keydown', 'j', function() {
                if (!$selected) {
                    SniptList.$snipts.eq(0).trigger('select');
                } else {
                    $selected.trigger('next');
                }
            });
            $document.bind('keydown', 'k', function() {
                if (!$selected) {
                    SniptList.$snipts.eq(0).trigger('select');
                } else {
                    $selected.trigger('prev');
                }
            });
            $document.bind('keydown', 'n', function() {
                var $anc = $('li.next a');
                if ($anc.length) {
                    if ($anc.attr('href') !== '#') {
                        window.location = $anc.attr('href');
                    }
                }
            });
            $document.bind('keydown', 'o', function() {
                if ($selected) {
                    $selected.trigger('detail');
                }
            });
            $document.bind('keydown', 'p', function() {
                var $anc = $('li.prev a');
                if ($anc.length) {
                    if ($anc.attr('href') !== '#') {
                        window.location = $anc.attr('href');
                    }
                }
            });
            $document.bind('keydown', 'return', function() {
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
