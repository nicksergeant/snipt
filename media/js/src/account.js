(function() {

    if (typeof angular !== 'undefined') {

        // Globals.
        var root = this;
        var $ = root.jQuery;

        // App definition.
        var app = angular.module('Account', [], function($routeProvider, $locationProvider) {

            $locationProvider.html5Mode(true);

            // Routes.
            $routeProvider.when('/account/', {
                templateUrl: '/media/js/src/modules/partials/profile.html',
                controller: controllers.ProfileController
            });
            $routeProvider.when('/account/billing/', {
                templateUrl: '/media/js/src/modules/partials/billing.html',
                controller: controllers.BillingController
            });
            $routeProvider.when('/account/blogging/', {
                templateUrl: '/media/js/src/modules/partials/blogging.html',
                controller: controllers.BloggingController
            });
            $routeProvider.when('/account/editor/', {
                templateUrl: '/media/js/src/modules/partials/editor.html',
                controller: controllers.EditorController
            });

            // I have absolutely no idea why I need to do this. Angular shouldn't touch URLs
            // that don't match above. But for some reason, it does. So if you have a non-routed
            // URL inside of your controller, your browser won't redirect.
            //
            // -10 points, Angular.
            $routeProvider.otherwise({
                'redirectTo': function(routeParams, locationPath) {
                    window.location = locationPath;
                }
            });

        });

        // Use non-Django-style interpolation.
        app.config(function($interpolateProvider) {
            $interpolateProvider.startSymbol('[[');
            $interpolateProvider.endSymbol(']]');
        });

        // Services.
        app.factory('AccountStorage', function($http) {
            return {
                getAccount: function() {

                    var promise = $http({
                        method: 'GET',
                        url: '/api/private/profile/' + window.user_profile_id + '/',
                        headers: {
                            'Authorization': 'ApiKey ' + window.user + ':' + window.api_key
                        }
                    });

                    return promise;
                }
            };
        });

        // Controllers.
        var controllers = {};

        controllers.MainController = function($scope, $route, AccountStorage) {
            $scope.route = $route;

            AccountStorage.getAccount().then(function(response) {
                $scope.user = response.data;
            });
        };

        controllers.BillingController = function($scope) {
            $scope.section = 'Billing';
        };
        controllers.BloggingController = function($scope) {
            $scope.section = 'Blogging';
        };
        controllers.EditorController = function($scope) {
            $scope.section = 'Editor';
        };
        controllers.ProfileController = function($scope) {
            $scope.section = 'Profile';
        };

        // Assign the controllers.
        app.controller(controllers);

    }

}).call(this);
