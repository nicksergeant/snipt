(function(Snipt) {

    Snipt.SniptModel = Backbone.Model.extend({
    });
    SniptView = Backbone.View.extend({
        initialize: function() {
            this.model = new Snipt.SniptModel();
            this.model.view = this;

            this.$el = $(this.el);
            this.$aside = $('aside', this.$el);
            this.$container = $('div.container', this.$el);
            this.$raw = $('div.raw', this.$container);
            this.$tags = $('section.tags ul', this.$aside);
        },
        events: {
            'click a.copy':   'copy',
            'click a.expand': 'expand',
            'detail':         'detail',
            'next':           'next',
            'prev':           'prev',
            'select':         'select'
        },
        expand: function() {
            this.$container.toggleClass('expanded', 100);
            this.$tags.toggleClass('expanded');
            return false;
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
        select: function() {

            $('article.selected', SniptList.$el).removeClass('selected');
            this.$el.addClass('selected');

            if (SniptList.$snipts.index(this.$el) === 0) {
                $('html, body').animate({
                    scrollTop: 0
                }, 0);
            } else {
                $('html, body').animate({
                    scrollTop: this.$el.offset().top - 50
                }, 0);
            }

            window.$selected = this.$el;
        },
        detail: function() {
            console.log('Going to detail view for ' + this.$el.find('h1').text());
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

            $(document).bind('keydown', 'j', function(e) {
                if (!$selected) {
                    $snipts.eq(0).trigger('select');
                } else {
                    $selected.trigger('next');
                }
            });
            $(document).bind('keydown', 'k', function(e) {
                if (!$selected) {
                    $snipts.eq(0).trigger('select');
                } else {
                    $selected.trigger('prev');
                }
            });
            $(document).bind('keydown', 'return', function(e) {
                if (!$selected) {
                    return false;
                }
                $selected.trigger('detail');
                return false;
            });
            $(document).bind('keydown', 'esc', function(e) {
                if ($selected) {
                    $selected.removeClass('selected');
                    $selected = false;
                }
            });
        }
    });
    Snipt.Views = {
        'SniptListView': SniptListView
    };

})(snipt.module('snipt'));
