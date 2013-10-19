(function() {

  'use strict';

  if (typeof angular !== 'undefined') {

    var root = this;
    var $ = root.jQuery;
    var controllers = {};
    var app = root.app;

    // Controllers.
    controllers.SniptListController = function($scope, AccountStorage) {

      $scope.$root.account = {
        list_view: 'N'
      };

      AccountStorage.getAccount().then(function(response) {
        $scope.$root.account = response.data;
      });

      $scope.$root.$watch('account.list_view', function(oldView, newView) {
        if (oldView !== newView) {
          AccountStorage.saveAccount($scope.$root.account, ['list_view']).then(function(response) {
            $scope.$root.account = response.data;
          });
        }
      });
    };

    // Assign the controllers.
    app.controller(controllers);

  }

}).call(this);
