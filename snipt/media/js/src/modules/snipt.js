(function(Snipt) {

    SniptListView = Backbone.View.extend({
        el: 'section#snipts',

        initialize: function(opts) {

            $snipts = opts.snipts;

            //$('input, select, textarea', this.el).each(this.addField);

            //$('section.code a.expand').click ->
                //el = $(this).parent()
                //el.toggleClass('expanded')

                //if el.hasClass('expanded')
                    //el.css('height', 'auto')
                    //$(this).text('Collapse')
                //else
                    //el.css('height', '200px')
                    //$(this).text('Expand')
                //false
            //false
            //
        }
    });

    Snipt.Views = {
        'SniptListView': SniptListView
    };

})(snipt.module('snipt'));
