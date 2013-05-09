var snipt = {
    module: function() {
        var modules = {};

        return function(name) {
            if (modules[name]) {
                return modules[name];
            }

            return modules[name] = {};
        };
    }()
};

jQuery(function($) {

    var SiteView = snipt.module('site').SiteView;
    window.site = new SiteView();

});

// Angular app init.
(function() {

    var root = this;

    // App definition.
    var app = angular.module('Snipt', [], function($locationProvider) {
        $locationProvider.html5Mode(true);
    });

    // Use non-Django-style interpolation.
    app.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
    });

    root.app = app;

}).call(this);
