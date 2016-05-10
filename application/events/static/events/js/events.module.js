(function() {
	'use strict';

	angular.module('EventsMod',['ngCookies','ngAnimate','ngResource','ui.bootstrap','ui.calendar'])
        .config(['$httpProvider','$resourceProvider', function($httpProvider, $resourceProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $resourceProvider.defaults.stripTrailingSlashes = false;
        }]);
})();