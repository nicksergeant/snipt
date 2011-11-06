(function(Apply) {

    Apply.FieldModel = Backbone.Model.extend({
        group: null
    });
    FieldView = Backbone.View.extend({
        initialize: function() {
            this.model = new Apply.FieldModel({
                group: $(this.el).parents('div.group').attr('id')
            });
            this.model.view = this;

            this.$tooltip = $('div.tooltip', $('#' + this.model.get('group')));
        },
        events: {
            'focus': 'focused',
            'blur' : 'blurred',
            'keyup': 'updateTooltip'
        },
        focused: function() {
            App.$tooltips.hide();
            this.$tooltip.show();
        },
        blurred: function() {
            App.$tooltips.hide();
        },
        updateTooltip: function() {
            if (this.model.get('group') == 'name') {
                short_name = $.trim(App.$first_name.val() + ' ' + App.$last_name.val().charAt(0));
                if (short_name !== '') {
                    short_name = ': ' + short_name;
                }
                App.$name_preview.text($.trim(short_name));
            }
        }
    });

    AppView = Backbone.View.extend({
        el: '#app',

        initialize: function(opts) {
            $('input, select, textarea', this.el).each(this.addField);

            this.$first_name   = $('input#id_first_name', this.el);
            this.$last_name    = $('input#id_last_name', this.el);
            this.$name_preview = $('strong#name-preview', this.el);
            this.$tooltips     = $('div.tooltip', this.el);
        },
        addField: function() {
            model = new FieldView({ el: this });
        }
    });

    Apply.Views = {
        'AppView': AppView,
        'FieldView': FieldView
    };

})(sidepros.module('apply'));
