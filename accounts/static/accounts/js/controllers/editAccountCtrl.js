'use strict';

angular
    .module('AccountsMod')
    .controller('EditAccountCtrl', EditAccountCtrl)

    EditAccountCtrl.$inject = ['Accounts', 'PermissionsSets', '$window']

    function EditAccountCtrl(Accounts, PermissionsSets, $window) {
        var vm = this;
        window.vm = vm;
            
        if(window.account_id) {
            vm.editing = true;
            var accountId = window.account_id;
            vm.account = Accounts.get({id: accountId});
        } else {
            vm.editing = false;
            vm.account = {
                email: '',
                first_name: '',
                last_name: '',
                user_designation: '',
                permission_irf_view: false,
                permission_irf_add: false,
                permission_irf_edit: false,
                permission_irf_delete: false,
                permission_vif_view: false,
                permission_vif_add: false,
                permission_vif_edit: false,
                permission_vif_delete: false,
                permission_border_stations_view: false,
                permission_border_stations_add: false,                
                permission_border_stations_edit: false,                
                permission_border_stations_delete: false,                
                permission_accounts_manage: false,
                permission_receive_email: false,
                permission_vdc_manage: false,
                permission_budget_manage: false,
            }
        }
        
        vm.permissionsSets = PermissionsSets.all();
        
        vm.update = function() {
            var call;
            if(vm.editing) {
                call = Accounts.update(vm.account).$promise;
            }else {
                call= Accounts.create(vm.account).$promise;                
            }
            call.then(function() {
                $window.location.href = "/accounts";
            });
        }
        
        vm.getTitle = function() {
            if(vm.editing) {
                return 'Edit ' +vm.account.first_name + ' ' + vm.account.last_name + "'s Account";
            }
            return 'Create Account';
        }
        
        vm.onUserDesignationChanged = function(value) {
            PermissionsSets.get({id: value}).$promise.then(function (permissions) {
                console.log(permissions);
                vm.account.permission_irf_view = permissions.permission_irf_view;
                vm.account.permission_irf_add = permissions.permission_irf_add;
                vm.account.permission_irf_edit = permissions.permission_irf_edit;
                vm.account.permission_irf_delete = permissions.permission_irf_delete;
                vm.account.permission_vif_view = permissions.permission_vif_view;
                vm.account.permission_vif_add = permissions.permission_vif_add;
                vm.account.permission_vif_edit = permissions.permission_vif_edit;
                vm.account.permission_vif_delete = permissions.permission_vif_delete;
                vm.account.permission_border_stations_view = permissions.permission_border_stations_view;
                vm.account.permission_border_stations_add = permissions.permission_border_stations_add;
                vm.account.permission_border_stations_edit = permissions.permission_border_stations_edit;
                vm.account.permission_border_stations_delete = permissions.permission_border_stations_delete;
                vm.account.permission_accounts_manage = permissions.permission_accounts_manage;
                vm.account.permission_receive_email = permissions.permission_receive_email;
                vm.account.permission_vdc_manage = permissions.permission_vdc_manage;
                vm.account.permission_budget_manage = permissions.permission_budget_manage;
            });
        }
        
        vm.getButtonText = function(has_permission) {
            if(has_permission) {
                return "Yes";
            }
            return "No";
        }
        
        vm.getUpdateButtonText = function() {
            if(vm.editing) {
                return "Update";
            }
            return "Create";
        }
               
    }
