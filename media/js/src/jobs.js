'use strict';

(function(window) {

  if (typeof angular !== 'undefined') {

    var root = window;
    var $ = root.jQuery;
    var controllers = {};
    var app = root.app;

    app.filter('startFrom', function() {
      return function(input, start) {
        start = +start;
        return input ? input.slice(start) : input;
      };
    });

    // Controllers.
    controllers.JobSearchController = function($http, $scope, filterFilter, $timeout) {
      $scope.currentPage = 0;
      $scope.pageSize = 10;

      $http.get('/jobs-json/').then(function(response) {
        $scope.jobs = response.data;
        $scope.filterJobs();
        $timeout(function() {
          window.mixpanel.track_links('.job-link', 'Job link clicked');
        });
      });

      $scope.filterJobs = function() {
        $scope.filteredJobs = filterFilter($scope.jobs, $scope.query);
        $scope.currentPage = 0;
      };
      $scope.numberOfPages = function() {
        if ($scope.filteredJobs) {
          return Math.ceil($scope.filteredJobs.length / $scope.pageSize);                
        }
      };

      $scope.$watch('query', function (val) {
        $scope.filterJobs();
      });
      
    };

    // Assign the controllers.
    app.controller(controllers);

  }

})(window);
