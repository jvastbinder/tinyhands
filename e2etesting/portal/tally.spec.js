var tallyHelper = require('./tally');
var loginPage = require('../accounts/loginPage');
var irfCrud = require('../irf/irfCRUD');

describe('Tally UI', function(){
    var origHeight = 0;
    var origWidth = 0;
    
    beforeEach(function () {
        return browser.ignoreSynchronization = true;
    });
    
    it('should have 7 days on screen', function(){
        browser.driver.manage().window().maximize();
        
        browser.sleep(1000);
        loginPage.loginAsAdmin();
        tallyHelper.navigateHome();
        var days = element.all(by.css('.day-of-week')).filter(function(elem, index) {
            return elem.isDisplayed();
        });
        expect(days.count()).toEqual(7);
        
    });
    
    it('should have no interceptions for the 7 days', function(){
        var daysText = element.all(by.css('h4.animated.tallyFade'));
        daysText.each(function(element, index){
            element.getInnerHtml().then(function(text){
                expect(text).toEqual('No Interceptions');
            });
        });
    });
    
    it('should list interceptions when there are some and show what days have changed', function() {
        irfCrud.getToIRF().then(function(){
            expect(browser.driver.getCurrentUrl()).toContain('data-entry/irfs/create/');
            var date = new Date();
            irfCrud.fillOutIRF(new Date().toString());
            return tallyHelper.navigateHome();
            
        }).then(function(){
            var days = element.all(by.css('.day-of-week')).filter(function(elem, index) {
                return elem.isDisplayed();
            });
            expect(days.count()).toEqual(7);
            
            var interceptions = tallyHelper.getInterceptions();
            
            expect(interceptions.count()).toEqual(1);
            expect(interceptions.first().getInnerHtml()).toEqual('1 INT in BHD');
            
            //test that tab is red based on changes since locally stored version
            var tab = interceptions.first().element(by.xpath('..')).element(by.xpath('..'));
            expect(tab.getCssValue('color')).toEqual('rgba(255, 255, 255, 1)');
            /*
            Make sure the background is red when updated.
            We check for .498039 rather than .5 because of the reason stated here: 
                http://stackoverflow.com/questions/13754483/how-to-get-the-exact-rgba-value-set-through-css-via-javascript
            */
            expect(tab.getCssValue('background-color')).toEqual('rgba(255, 0, 0, 0.498039)');
        });
    });
    
    it('should change back to white after viewing a day when screen is large', function(){
        var interceptions = tallyHelper.getInterceptions();
        var tab = interceptions.first().element(by.xpath('..')).element(by.xpath('..'));
        browser.actions().mouseMove(tab).mouseMove({x: 300, y: 300}).perform().then(function(){ 
            expect(tab.getCssValue('background-color')).toEqual('rgba(255, 255, 255, 0.85098)');
        });
    });
    
    it('should auto update every minute', function() {
        tallyHelper.openNewTab() //open new tab
        .then(function () { // switch to the newly created tab
           tallyHelper.switchToTab(1);
        }).then(function() { // complete new irf
            return irfCrud.getToIRF().then(function(){
                expect(browser.driver.getCurrentUrl()).toContain('data-entry/irfs/create/');
                return irfCrud.fillOutIRF(new Date().toString());
            });
        }).then(function() { //close second tab and return back to first tab
            return browser.driver.close().then(function () {
                return tallyHelper.switchToTab(0);
            });
        }).then(function() { //wait one minute for update to occur
            return browser.sleep(60000);
        }).then(function () {
            var interceptions = tallyHelper.getInterceptions();
            
            expect(interceptions.count()).toEqual(1);
            expect(interceptions.first().getInnerHtml()).toEqual('2 INT in BHD');
            var tab = interceptions.first().element(by.xpath('..')).element(by.xpath('..'));
            expect(tab.getCssValue('color')).toEqual('rgba(255, 255, 255, 1)');
            expect(tab.getCssValue('background-color')).toEqual('rgba(255, 0, 0, 0.498039)');
        });
    }, 90000); //gives it a minute and a half until it timeouts
    
    it('should show number of interceptions for that day when screen is small', function () {
        browser.driver.manage().window().setSize(768, 768).then(function(){
            return tallyHelper.openNewTab(); 
        }).then(function () { // switch to the newly created tab
            return browser.getAllWindowHandles().then(function (handles) {
                newWindowHandle = handles[1];
                return browser.switchTo().window(newWindowHandle);
            });
        }).then(function() { // complete new irf
            return irfCrud.getToIRF().then(function(){
                expect(browser.driver.getCurrentUrl()).toContain('data-entry/irfs/create/');
                var date = new Date();
                irfCrud.fillOutIRF(new Date().toString());
                return tallyHelper.navigateHome();
            });
        }).then(function() { //close second tab and return back to first tab
            return browser.driver.close().then(function () {
                return browser.getAllWindowHandles().then(function (handles) {
                    newWindowHandle = handles[0];
                    return browser.switchTo().window(newWindowHandle);
                });
            });
        }).then(function() { //wait one minute for update to occur
            return browser.sleep(60000);
        }).then(function () {
            var interceptions = tallyHelper.getInterceptionsSmall();
            
            expect(interceptions.count()).toEqual(1);
            expect(interceptions.first().getInnerHtml()).toEqual('3');
            
            var tab = interceptions.first().element(by.xpath('..'));
            expect(tab.getCssValue('color')).toEqual('rgba(255, 255, 255, 1)');
            expect(tab.getCssValue('background-color')).toEqual('rgba(255, 0, 0, 0.498039)');
        });
    }, 90000); //gives it a minute and a half until it timeouts
    
    it('should change back to white after viewing a day when screen is small', function(){
        var interceptions = tallyHelper.getInterceptionsSmall();
        var tab = interceptions.first().element(by.xpath('..'));
        browser.actions().mouseMove(tab).mouseMove({x: 300, y: 300}).perform().then(function(){ 
            expect(tab.getCssValue('background-color')).toEqual('rgba(0, 0, 0, 0)');
        });
    });
    
    it('should disappear when unchecked from hamburger map menu and reappear when checked', function(){
        browser.driver.manage().window().maximize(); // return browser back to full size
        var EC = protractor.ExpectedConditions;
        tallyHelper.navigateHome()
        .then(function () {
            var tallyDiv = element(by.id('tally')).element(by.tagName('div')).isDisplayed();
            return expect(tallyDiv).toBe(true);
        }).then(function (){
            return element(by.id('layer-dropdown')).click().then(function(){
                return element(by.id('layer-dropdown')).click() //not sure why I need the second click but it makes the dropdown popup
            });
        }).then(function(){
            var tallyToggle = element(by.id('tallyToggle'));
            return tallyToggle.click();
        }).then(function () {
            var tallyDiv = element(by.id('tally')).element(by.tagName('div')).isDisplayed();
            return expect(tallyDiv).toBe(false);
        }).then(function (){
            return element(by.id('layer-dropdown')).click();
        }).then(function(){
            var tallyToggle = element(by.id('tallyToggle'));
            return tallyToggle.click();
        }).then(function () {
            var tallyDiv = element(by.id('tally')).element(by.tagName('div')).isDisplayed();
            return expect(tallyDiv).toBe(true);
        })
    });
});