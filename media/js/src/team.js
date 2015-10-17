(function() { 'use strict';

if (typeof angular !== 'undefined') {

  var root = this;
  var $ = root.jQuery;
  var controllers = {};
  var app = root.app;

  // Services.
  app.factory('TeamStorage', function($http, $q) {
    return {
      searchUsers: function(query) {
        var promise = $http({
          method: 'GET',
          url: '/api/public/user/?format=json&limit=100&username__contains=' + query
        });
        return promise;
      }
    };
  });

  // Controllers.
  controllers.TeamController = function($scope, $timeout, TeamStorage) {
    $scope.users = [];
    $scope.$watch('search', function(val) {
      $timeout.cancel($scope.timeout);

      if (!val) return $scope.users = [];

      $scope.timeout = $timeout(function() {
        TeamStorage.searchUsers(val).then(function(response) {
          $scope.users = response.data.objects;
        });
      }, 350);
    });
  };

  // Assign the controllers.
  app.controller(controllers);

}

}).call(this);
