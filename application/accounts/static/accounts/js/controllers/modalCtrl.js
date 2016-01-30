angular
    .module('AccountsMod')
    .controller('ModalCtrl', function($scope, $modalInstance, user_name) {
        var vm = this;

        vm.activate = function () {
          $scope.user_name = user_name;
        }

        vm.delete = function() {
          $modalInstance.close(true);
        };
        
        vm.cancel = function () {
          $modalInstance.dismiss("cancel");
        };

        vm.activate();
    });