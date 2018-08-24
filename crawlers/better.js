"use strict";
var _this = this;
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var puppeteer = require("puppeteer");
var launch_options_1 = require("./launch-options");
var theEvent = "NA LCS";
var theMarket = "Team to Draw First Blood";
function attachToWindow(page, propName, propVal) {
    return page.evaluate("\n      if (typeof " + propName + " === 'undefined') {\n        Object.defineProperty(window, '" + propName + "', {\n          get() { return " + propVal + " }\n        })\n      } else if (typeof " + propName + " === 'string') {\n        " + propName + " = " + propVal + "\n      } else {\n      }\n    ");
}
/**
 * @param {HTMLElement}
 * Contains <span class="gl-Participant_Name">{teamNAme}</span>
 */
var getTeams = (function getTeams(el) {
    return Array.from(el.querySelectorAll(".gl-Participant_Name"))
        .map(function (x) { return x.innerHTML; });
});
/**
 * @param {HTMLElement}
 * Contains <span class="gl-Participant_Odds">{odds}</span>
 */
var getOdds = (function (el) {
    return Array.from(el.querySelectorAll(".gl-Participant_Odds"))
        .map(function (x) { return x.innerHTML; });
});
var visitEsportsPage = (function (page) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
    return tslib_1.__generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, page.goto("https://www.bet365.com.au/")];
            case 1:
                _a.sent();
                return [4 /*yield*/, page.mainFrame().waitForSelector(".wn-Classification ")];
            case 2:
                _a.sent();
                return [4 /*yield*/, page.$$eval(".wn-Classification ", function (divs) {
                        return Array.from(divs)
                            .find(function (x) { return x.innerText.includes("Esports"); })
                            .click();
                    })];
            case 3:
                _a.sent();
                return [2 /*return*/];
        }
    });
}); });
var main = (function main() {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var browser, page;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    console.log("Executing");
                    return [4 /*yield*/, puppeteer.launch(launch_options_1.options)];
                case 1:
                    browser = _a.sent();
                    return [4 /*yield*/, browser.newPage()];
                case 2:
                    page = _a.sent();
                    return [4 /*yield*/, visitEsportsPage(page)];
                case 3:
                    _a.sent();
                    return [4 /*yield*/, page.mainFrame().waitForSelector(".sm-MarketGroup_GroupName ")];
                case 4:
                    _a.sent();
                    return [4 /*yield*/, page.$$eval(".sm-MarketGroup_GroupName ", function (divs) {
                            var theLeague = Array.from(divs)
                                .find(function (x) { return x.innerText.toLowerCase().includes('na lcs'); });
                            // the table containing all the markets
                            //
                            var table = theLeague.parentElement.parentElement;
                            var market = Array.from(table.querySelectorAll(".sm-CouponLink_Label "))
                                .find(function (x) { return x.innerText.toLowerCase().includes("draw first blood"); })
                                .click();
                        })];
                case 5:
                    _a.sent();
                    return [4 /*yield*/, page.waitForSelector(".cm-CouponMarketGroupButton_Title")];
                case 6:
                    _a.sent();
                    console.log("Here");
                    return [4 /*yield*/, attachToWindow(page, 'getTeams', getTeams)];
                case 7:
                    _a.sent();
                    return [4 /*yield*/, attachToWindow(page, 'getOdds', getOdds)];
                case 8:
                    _a.sent();
                    return [4 /*yield*/, page.$eval(".gl-MarketGroup", function (marketGroup) {
                            var tableRows = Array.from(marketGroup.querySelectorAll(".gl-Market_General"));
                            for (var _i = 0, tableRows_1 = tableRows; _i < tableRows_1.length; _i++) {
                                var tableRow = tableRows_1[_i];
                                Promise.all([
                                    getTeams(tableRow),
                                    getOdds(tableRow)
                                ]).then(function (_a) {
                                    var teams = _a[0], odds = _a[1];
                                    console.log(teams);
                                    console.log(odds);
                                });
                            }
                        })];
                case 9:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
})();
// main()
