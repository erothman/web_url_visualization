(function () {
  'use strict';
  var app = angular.module('VulnerabilityTableApp', []);

  app.controller('TableCtrl', ['$scope', '$log', '$http', function($scope, $log, $http) {
        
        $http.get('/getData')
        .then(function (response) {
            $scope.vulnerabilities = response.data;
        });
        $scope.reverse = false;
        $scope.alphField = "test";
        $scope.queryTerm = "";
        $scope.getOrganizedData = function(field) {
            $log.log(field)
            if ($scope.alphField == field) {
                $scope.reverse = !$scope.reverse;
            } else {$scope.reverse = false; $scope.alphField = field;}
            $log.log($scope.alphField)
            $http.get('/getDataOrdered/'+field+'/'+$scope.reverse)
            .then(function (response) {
                $scope.vulnerabilities = response.data;
            });
        }
        $scope.getQueriedData = function() {
            $http.get('/getDataQuery/'+$scope.queryTerm)
            .then(function (response) {
                $scope.vulnerabilities = response.data;
            });
        }
}]);
}());
