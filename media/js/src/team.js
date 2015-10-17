(function() { 'use strict';

if (typeof angular !== 'undefined') {

  var root = this;
  var $ = root.jQuery;
  var controllers = {};
  var app = root.app;

  // Services.
  app.factory('TeamStorage', function($http, $q) {
    return {
      searchMembers: function(query) {
        var promise = $http({
          method: 'GET',
          url: '/api/public/user/?format=json&username__contains=' + query
        });
        return promise;
      }
    };
  });

  // Controllers.
  controllers.TeamController = function($scope, $timeout, TeamStorage) {
    $scope.members = [];
    $scope.$watch('search', function(val) {
      $timeout.cancel($scope.timeout);

      if (!val) return $scope.members = [];

      $scope.timeout = $timeout(function() {
        TeamStorage.searchMembers(val).then(function(response) {
          $scope.members = response.data.objects;
        });
      }, 250);
    });
  };

  // Assign the controllers.
  app.controller(controllers);

}

}).call(this);
