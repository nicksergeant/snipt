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
        $scope.$root.$watch('account.list_view', function(newView, oldView) {
          if (oldView !== newView) {
            if (newView === 'N') {
              window.ll('tagEvent', 'Switched to normal view');
            } else {
              window.ll('tagEvent', 'Switched to compact view');
            }
            AccountStorage.saveAccount($scope.$root.account, ['list_view']).then(function(response) {
              $scope.$root.account = response.data;
            });
          }
        });
      });
    };

    // Assign the controllers.
    app.controller(controllers);

  }

}).call(this);
