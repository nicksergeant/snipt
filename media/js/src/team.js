(function() { 'use strict';

if (typeof angular !== 'undefined') {

  var root = this;
  var $ = root.jQuery;
  var controllers = {};
  var app = root.app;

  // Services.
  app.factory('TeamStorage', function($http) {
    return {

    };
  });

  // Controllers.
  controllers.TeamController = function($scope, TeamStorage) {

  };

  // Assign the controllers.
  app.controller(controllers);

}

}).call(this);
