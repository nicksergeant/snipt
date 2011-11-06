// Memoizing technique from http://weblog.bocoup.com/organizing-your-backbone-js-application-with-modules
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

// Init application
jQuery(function($) {

    //if ($('body').hasClass('apply')) {
        //AppView = sidepros.module('apply').Views.AppView;
        //App = new AppView();
    //}

});
