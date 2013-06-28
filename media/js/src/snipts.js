(function() {

  if (typeof angular !== 'undefined') {

    var root = this;
    var $ = root.jQuery;
    var controllers = {};
    var app = root.app;

    // Controllers.
    controllers.SniptListController = function($scope) {
      $scope.section = 'Billing';
    };

    // Assign the controllers.
    app.controller(controllers);

  }

}).call(this);
