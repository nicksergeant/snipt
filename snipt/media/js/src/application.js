
var snipt = {
    module: function() {
        var modules = {};

        return function(name) {
            if (modules[name]) {
                return modules[name];
            }

            return modules[name] = { Views: {} };
        };
    }()
};

jQuery(function($) {

    var SiteView = snipt.module('site').Views.SiteView;
    window.site = new SiteView();

});
