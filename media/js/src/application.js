'use strict';

var snipt = {
  module: function() {
    var modules = {};

    return function(name) {
      if (modules[name]) {
        return modules[name];
      }

      return modules[name] = {};
    };
  }()
};

jQuery(function($) {
  var SiteView = snipt.module('site').SiteView;
  window.site = new SiteView();

  var $pres = $('td.code pre');
  $pres.each(function(i) {
    var pre = $pres.eq(i);
    pre.width(pre.parents('section.code').width() - 30);
  });
});

// Angular app init.
(function() {

  var root = this;

  // App definition.
  var app = angular.module('Snipt', ['ngRoute'], function($locationProvider) {
    $locationProvider.html5Mode(true);
  });

  // Use non-Django-style interpolation.
  app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
  });

  root.app = app;

  if (root.ll) {
    if (root.location.pathname === '/account/stats/') {
      root.ll('tagEvent', 'Viewed stats page');
    }
    if (root.location.pathname === '/pro/') {
      root.ll('tagEvent', 'Viewed Pro page');
    }
    if (root.location.pathname === '/pro/signup/') {
      root.ll('tagEvent', 'Viewed Pro signup page');
    }
  }

  app.controller('AppController', function($scope) {
    $scope.ads = [
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://showroom.is/?from=snipt',
        image: 'https://snipt.s3.amazonaws.com/img/logo-showroom.png',
        company: 'Showroom.is',
        title: 'New-car research for the modern web.'
      },
      {
        url: 'http://bruce-springsteen-the-e-street-band.gigs.is/?from=snipt',
        image: 'http://cdn.chairnerd.com/images/performers-landscape/bruce-springsteen-bf99a8/4275/huge.jpg',
        company: 'Gigs.is',
        title: 'Bruce Springsteen & The E Street Band on tour.'
      },
      {
        url: 'http://beyonce.gigs.is/?from=snipt',
        image: 'http://cdn.chairnerd.com/images/performers-landscape/beyonce-b28ec9/37/huge.jpg',
        company: 'Gigs.is',
        title: 'Beyonce on tour. View current tour dates on:'
      },
      {
        url: 'http://paul-mccartney.gigs.is/?from=snipt',
        image: 'http://cdn.chairnerd.com/images/performers-landscape/paul-mccartney-0ab8df/1408/huge.jpg',
        company: 'Gigs.is',
        title: 'Paul McCartney on tour. View current tour dates on:'
      },
      {
        url: 'http://rolling-stones.gigs.is/?from=snipt',
        image: 'http://cdn.chairnerd.com/images/performers-landscape/rolling-stones-73ab94/2597/huge.jpg',
        company: 'Gigs.is',
        title: 'Rolling Stones on tour. View current tour dates on:'
      },
      {
        url: 'http://justin-timberlake.gigs.is/?from=snipt',
        image: 'http://cdn.chairnerd.com/images/performers-landscape/justin-timberlake-c30b82/1019/huge.jpg',
        company: 'Gigs.is',
        title: 'Justin Timberlake on tour. View current tour dates on:'
      },
      {
        url: 'http://billy-joel.gigs.is/?from=snipt',
        image: 'http://cdn.chairnerd.com/images/performers-landscape/billy-joel-254023/303/huge.jpg',
        company: 'Gigs.is',
        title: 'Billy Joel on tour. View current tour dates on:'
      },
      {
        url: 'http://taylor-swift.gigs.is/?from=snipt',
        image: 'http://cdn.chairnerd.com/images/performers-landscape/taylor-swift-1cdf83/35/huge.jpg',
        company: 'Gigs.is',
        title: 'Taylor Swift on tour. View current tour dates on:'
      },
      {
        url: 'http://one-direction.gigs.is/?from=snipt',
        image: 'http://cdn.chairnerd.com/images/performers-landscape/one-direction-a22937/12586/huge.jpg',
        company: 'Gigs.is',
        title: 'One Direction on tour. View current tour dates on:'
      },
      {
        url: 'http://george-strait.gigs.is/?from=snipt',
        image: 'http://cdn.chairnerd.com/images/performers-landscape/george-strait-92a4b8/780/huge.jpg',
        company: 'Gigs.is',
        title: 'George Strait on tour. View current tour dates on:'
      },
      {
        url: 'http://pearl-jam.gigs.is/?from=snipt',
        image: 'http://cdn.chairnerd.com/images/performers-landscape/pearl-jam-fb4480/1416/huge.jpg',
        company: 'Gigs.is',
        title: 'Pearl Jam on tour. View current tour dates on:'
      }
    ];

    var randomIndex = Math.floor(Math.random() * (($scope.ads.length - 1) - 0 + 1)) + 0;
    $scope.randomAd = $scope.ads[randomIndex];
  });

}).call(this);
