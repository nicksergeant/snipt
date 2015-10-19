(function() { 'use strict';

if (typeof angular !== 'undefined') {

  var root = this;
  var $ = root.jQuery;
  var controllers = {};
  var app = root.app;

  // App definition.
  app.config(function($routeProvider) {

    // Routes.
    $routeProvider.when('/account/', {
      templateUrl: '/static/js/src/modules/partials/profile.html',
      controller: controllers.ProfileController
    });
    $routeProvider.when('/account/billing/', {
      templateUrl: '/static/js/src/modules/partials/billing.html',
      controller: controllers.BillingController
    });
    $routeProvider.when('/account/blogging/', {
      templateUrl: '/static/js/src/modules/partials/blogging.html',
      controller: controllers.BloggingController
    });
    $routeProvider.when('/account/editor/', {
      templateUrl: '/static/js/src/modules/partials/editor.html',
      controller: controllers.EditorController
    });

    $routeProvider.otherwise({
      'redirectTo': function(routeParams, locationPath) {
        window.location = locationPath;
      }
    });

  });

  // Services.
  app.factory('AccountStorage', function($http) {
    return {
      cancelSubscription: function() {

        var promise = $http({
          method: 'GET',
          url: '/account/cancel-subscription/',
          headers: {
            'Authorization': 'ApiKey ' + window.user + ':' + window.api_key
          }
        });

        return promise;
      },
      getAccount: function() {

        var promise = $http({
          method: 'GET',
          url: '/api/private/profile/' + window.user_profile_id + '/',
          headers: {
            'Authorization': 'ApiKey ' + window.user + ':' + window.api_key
          }
        });

        return promise;
      },
      getStripeAccount: function() {

        var promise = $http({
          method: 'GET',
          url: '/account/stripe-account-details/'
        });

        return promise;
      },
      saveAccount: function(user, fields) {

        var promise = $http({
          method: 'PUT',
          url: '/api/private/profile/' + window.user_profile_id + '/',
          headers: {
            'Authorization': 'ApiKey ' + window.user + ':' + window.api_key
          },
          data: function() {
            var userData = {};

            for (var i = 0; i < fields.length; i++) {
              userData[fields[i]] = user[fields[i]];
            }

            return userData;
          }()
        });

        return promise;
      }
    };
  });

  // Controllers.
  controllers.BillingController = function($scope, AccountStorage) {
    $scope.section = 'Billing';

    $scope.cancelSubscription = function() {
      if (confirm('Are you sure you want to cancel your subscription?\n\nYou will no longer be able to create new Snipts. Your existing snipts will still be accessible. This action is effective immediately and we unfortunately cannot issue any refunds.')) {
        $scope.cancelled = true;
        $scope.cancelling = true;
        AccountStorage.cancelSubscription().then(function(response) {
          if (response.data.deleted) {
            $scope.cancelling = false;
          } else {
            $scope.cancelling = false;
            $scope.cancelled = false;
          }
        });
      }
    };
  };
  controllers.BloggingController = function($scope) {
    $scope.fields = [
      'blog_title',
      'blog_theme',
      'blog_domain',
      'gittip_username',
      'disqus_shortname',
      'google_analytics_tracking_id',
      'gauges_site_id',
      'google_ad_client',
      'google_ad_slot',
      'google_ad_width',
      'google_ad_height'
    ];
    $scope.section = 'Blogging';

    $scope.blogThemeOptions = [
      { id: 'D', label: 'Default' },
      { id: 'A', label: 'Pro Adams' }
    ];

  };
  controllers.EditorController = function($scope) {
    $scope.fields = ['default_editor', 'editor_theme'];
    $scope.section = 'Editor';

    $scope.editorOptions = [
      { id: 'C', label: 'CodeMirror' },
      { id: 'T', label: 'Textarea' }
    ];
    $scope.editorThemeOptions = [
      { id: 'default', label: 'Default' },
      { id: 'ambiance', label: 'Ambiance' },
      { id: 'blackboard', label: 'Blackboard' },
      { id: 'cobalt', label: 'Cobalt' },
      { id: 'eclipse', label: 'Eclipse' },
      { id: 'elegant', label: 'Elegant' },
      { id: 'erlang-dark', label: 'Erlang Dark' },
      { id: 'lesser-dark', label: 'Lesser Dark' },
      { id: 'monokai', label: 'Monokai' },
      { id: 'neat', label: 'Neat' },
      { id: 'night', label: 'Night' },
      { id: 'rubyblue', label: 'Ruby Blue' },
      { id: 'solarized dark', label: 'Solarized Dark' },
      { id: 'solarized light', label: 'Solarized Light' },
      { id: 'twilight', label: 'Twilight' },
      { id: 'vibrant-ink', label: 'Vibrant Ink' },
      { id: 'xq-dark', label: 'XQ Dark' }
    ];

  };
  controllers.AccountController = function($scope, $route, AccountStorage) {
    $scope.errors = [];
    $scope.saveButtonText = 'Save';
    $scope.route = $route;

    AccountStorage.getAccount().then(function(response) {
      $scope.user = response.data;

      if ($scope.user.has_pro && $scope.user.stripe_id && $scope.user.stripe_id !== 'COMP') {
        AccountStorage.getStripeAccount().then(function(response) {
          $scope.user.stripeAccount = response.data;
        });
      }
    });

    $scope.saveFields = function(fields) {
      $scope.saveButtonText = 'Saving…';

      AccountStorage.saveAccount($scope.user, fields).then(function onSuccess(response) {

        // Save the new user object.
        $scope.user = response.data;

        // Signal that we have a successful response.
        $scope.success = true;

        // Success message.
        $scope.message = $scope.route.current.scope.section + ' settings saved.';

        // Reset the save button text.
        $scope.saveButtonText = 'Save';

        // Clear out any marked errors.
        $scope.errors = [];

        // Remove the success message after a while.
        setTimeout(function() {
          $scope.success = null;
          $scope.message = '';

          // We have to apply since we're outside of the scope context.
          $scope.$apply();

        }, 3000);

      }, function onError(response) {

        // Signal that we have an error.
        $scope.success = false;

        // Reset the save button text.
        $scope.saveButtonText = 'Save';

        // If we have a response, then it's probably a validation error.
        if (response) {

          // Set the errors on the scope.
          $scope.errors = response.data.profile;
          $scope.message = 'Only spaces, letters, numbers, underscores, dashes, periods, forward slashes, and "at sign" are valid.';

        } else {
          $scope.message = 'There was an error saving your settings.';
        }

      });
    };
  };
  controllers.ProfileController = function($scope) {
    $scope.section = 'Profile';
  };

  // Assign the controllers.
  app.controller(controllers);

}

}).call(this);
