'use strict';

var constants = require('../testConstants.json');
var methods = require('../commonMethods.js');

var moneyDistributionForm = function () {

    this.navigateToMoneyDistributionPage = function () {
        browser.get(constants.webAddress + '/budget/budget_calculations/');
        //element(by.linkText("Resend MDF")).click();
        methods.click(element(by.linkText("Resend MDF")));
    };

    this.toggleEmailAddress = function () {
        //element.all(by.repeater('staff in main.staff')).then(function(staff) {
            //var titleElement = staff[0].element(by.tagName('input'));
            //var titleElement = staff.element(by.xpath("/td/input"));
        var titleElement = element(by.xpath("/html/body/div[2]/div//table/tbody/tr/td[1]/input"));
        methods.click(titleElement);
            //titleElement.click();
        //});
    };

    this.toggleAllEmailAddresses = function () {
        element.all(by.repeater('staff in main.staff')).then(function(staff) {
            for(var i = 0; i < staff.length; i++) {
                var titleElement = staff[i].element(by.tagName('input'));
                methods.click(titleElement);
                //titleElement.click();
            }
        });
    };

    this.sendEmails = function () {
        browser.sleep(800);
        methods.click(element(by.partialLinkText("Send to")));
        browser.sleep(800);
    };

    this.updateBudgetForm = function () {
        //element(by.linkText("Update Budget")).click();
        browser.sleep(800);
        methods.click(element(by.linkText("Update Budget")));
        browser.sleep(800);
    };

};

module.exports = new moneyDistributionForm();