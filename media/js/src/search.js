(function() {

    if (typeof angular !== 'undefined') {

        var root = this;
        var $ = root.jQuery;
        var controllers = {};
        var app = root.app;

        // Services.
        app.factory('SearchService', function() {
            return {
              mineOnly: false,
              query: ''
            };
        });

        // Controllers.
        controllers.HeaderSearchController = function($scope, SearchService) {

          $scope.search = SearchService;

        };
        controllers.SearchController = function($scope, SearchService) {

          $scope.search = SearchService;

          $scope.$watch('search.query', function(query) {
            if (query.indexOf('--mine') !== -1) {
              $scope.search.mineOnly = true;
            } else {
              $scope.search.mineOnly = false;
            }
          });

          $scope.toggleMineOnly = function() {
            if ($scope.search.mineOnly) {

              // Make sure '--mine' exists somewhere in the query.
              if ($scope.search.query.indexOf('--mine') === -1) {
                $scope.search.query = $scope.search.query.trim() + ' --mine';
              }

            }
            else {
              $scope.search.query = $scope.search.query.replace('--mine', '').trim();
            }
          };

        };

        // Assign the controllers.
        app.controller(controllers);

    }

}).call(this);
