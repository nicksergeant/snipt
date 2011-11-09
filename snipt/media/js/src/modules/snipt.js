(function(Snipt) {

    Snipt.SniptModel = Backbone.Model.extend({
    });

    SniptView = Backbone.View.extend({
        initialize: function() {
            this.model = new Snipt.SniptModel();
            this.model.view = this;
            this.$el = $(this.el);
            this.$container = $('div.container', this.$el);
            this.$expand_button = $('a.expand', this.$el);
        },
        events: {
            'click a.expand': 'expand'
        },
        expand: function() {
            this.$container.toggleClass('expanded', 100);
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
