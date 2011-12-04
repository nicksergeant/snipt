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
            this.$copy_button = $('a.copy', this.$aside);
            this.$copy_do = $('span.do', this.$copy_button);
            this.$copy_done = $('span.done', this.$copy_button);
            this.$expand_button = $('a.expand', this.$aside);
            this.$raw = $('div.raw', this.$container);
            this.$tags = $('section.tags ul', this.$aside);

            this.setupCopy();
        },
        events: {
            'click a.expand': 'expand'
        },
        expand: function() {
            this.$container.toggleClass('expanded', 100);
            this.$tags.toggleClass('expanded');
            return false;
        },
        setupCopy: function() {

            var copy_do = this.$copy_do;
            var copy_done = this.$copy_done;

            //this.$copy_button.zclip({
                //afterCopy: function() {
                    //copy_do.hide();
                    //copy_done.fadeIn(500);
                    //setTimeout(function() {
                        //copy_done.hide();
                        //copy_do.fadeIn(500);
                    //}, 1500);
                //},
                //copy: this.$raw.text()
            //});
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
