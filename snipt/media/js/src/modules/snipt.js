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
            'click a.expand': 'expand',
            'click a.copy': 'copy'
        },
        expand: function() {
            this.$container.toggleClass('expanded', 100);
            this.$tags.toggleClass('expanded');
            return false;
        },
        copy: function() {
            window.prompt('Text is selected. To copy: press Ctrl+C then <Enter>', this.$raw.text());
            return false;
        }
    });

    SniptListView = Backbone.View.extend({
        el: 'section#snipts',

        initialize: function(opts) {
            opts.snipts.each(this.addSnipt);
        },
        addSnipt: function() {
            model = new SniptView({ el: this });
        }
    });

    Snipt.Views = {
        'SniptListView': SniptListView
    };

})(snipt.module('snipt'));
