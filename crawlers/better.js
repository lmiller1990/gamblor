"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var _this = this;
exports.__esModule = true;
var fs = require("fs");
var launch_options_1 = require("./launch-options");
var puppeteer = require("puppeteer");
var path = require("path");
var minimist = require("minimist");
var utils_1 = require("./utils");
var args = minimist(process.argv.slice(2));
var theEvent = args.event;
var theMarket = args.market;
var outputFile = args.outputFile;
var outputDirectory = args.outputDirectory;
function attachToWindow(page, propName, propVal) {
    return page.evaluate("\n      if (typeof " + propName + " === 'undefined') {\n        Object.defineProperty(window, '" + propName + "', {\n          get() { return " + propVal + " }\n        })\n      } else if (typeof " + propName + " === 'string') {\n        " + propName + " = " + propVal + "\n      } else {\n      }\n    ");
}
function clearPreviouslyScrapedData() {
    try {
        fs.unlinkSync(path.join(__dirname, "..", "odds", outputDirectory, outputFile));
    }
    catch (e) {
        // doesn't exist
    }
    fs.appendFileSync(path.join(__dirname, "..", "odds", outputDirectory, outputFile), "team_1,team_2,team_1_odds,team_2_odds");
}
function getTeams(el) {
    return Array.from(el.querySelectorAll(".gl-Participant_Name"))
        .map(function (x) { return x.innerHTML; });
}
/**
 * @param el {HTMLElement} HTMLElement that looks like this:
 *
 * <div class="cm-MarketSubGroup_Label ">Gambit Esports vs G-Rex - LOL - World Champs Play-In - Map 1</div>
 * <div>........</div> <- this is the el param
 *
 * So we want to get the team names from the previous element
 *
 * @returns teams {Array<string} array containing the two teams
 */
function getTeamsForOverUnder(el) {
    var tableHeader = el.previousElementSibling;
    var child = tableHeader.children[0];
    var teams = child.innerText.split('- LOL')[0].split('vs');
    return teams.map(function (x) { return x.toLowerCase().trim(); });
}
function getOdds(el) {
    return Array.from(el.querySelectorAll(".gl-Participant_Odds"))
        .map(function (x) { return x.innerHTML; });
}
var visitEsportsPage = (function (page) { return __awaiter(_this, void 0, void 0, function () {
    return __generator(this, function (_a) {
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
    return __awaiter(this, void 0, void 0, function () {
        var browser, page, matches, _i, _a, match;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    clearPreviouslyScrapedData();
                    return [4 /*yield*/, puppeteer.launch(launch_options_1.options)];
                case 1:
                    browser = _b.sent();
                    return [4 /*yield*/, browser.newPage()];
                case 2:
                    page = _b.sent();
                    return [4 /*yield*/, visitEsportsPage(page)];
                case 3:
                    _b.sent();
                    return [4 /*yield*/, page.mainFrame().waitForSelector(".sm-MarketGroup_GroupName ")];
                case 4:
                    _b.sent();
                    return [4 /*yield*/, attachToWindow(page, 'theMarket', JSON.stringify(theMarket))];
                case 5:
                    _b.sent();
                    return [4 /*yield*/, attachToWindow(page, 'theEvent', JSON.stringify(theEvent))
                        // console.log(theEvent, theMarket)
                    ];
                case 6:
                    _b.sent();
                    // console.log(theEvent, theMarket)
                    return [4 /*yield*/, page.$$eval(".sm-MarketGroup_GroupName ", function (divs) {
                            console.log(divs.length);
                            var theLeague = Array.from(divs)
                                .filter(function (x) {
                                console.log('innertext', x.innerText, 'theEvent', theEvent);
                                if (x.innerText.toLowerCase().includes(theEvent)) {
                                    console.log('found it', x);
                                    return x;
                                }
                            })[0];
                            // console.log("Finding for ", theEvent, theMarket) 
                            // the table containing all the markets
                            //
                            console.log(theLeague);
                            var table = theLeague.parentElement.parentElement;
                            var market = Array.from(table.querySelectorAll(".sm-CouponLink_Label "))
                                .find(function (x) {
                                console.log(x.innerText);
                                return x.innerText.toLowerCase().includes(theMarket);
                            });
                            market.click();
                        })];
                case 7:
                    // console.log(theEvent, theMarket)
                    _b.sent();
                    return [4 /*yield*/, page.waitForSelector(".cm-CouponMarketGroupButton_Title")];
                case 8:
                    _b.sent();
                    return [4 /*yield*/, attachToWindow(page, 'getTeams', getTeams)];
                case 9:
                    _b.sent();
                    return [4 /*yield*/, attachToWindow(page, 'getOdds', getOdds)];
                case 10:
                    _b.sent();
                    return [4 /*yield*/, attachToWindow(page, 'getTeamsForOverUnder', getTeamsForOverUnder)];
                case 11:
                    _b.sent();
                    return [4 /*yield*/, page.$eval(".gl-MarketGroup", function (marketGroup) {
                            var results = [];
                            var tableRows = Array.from(marketGroup.querySelectorAll(".gl-Market_General"));
                            var teamGetter = theMarket.includes("total") ? getTeamsForOverUnder : getTeams;
                            for (var _i = 0, tableRows_1 = tableRows; _i < tableRows_1.length; _i++) {
                                var tableRow = tableRows_1[_i];
                                Promise.all([
                                    teamGetter(tableRow),
                                    getOdds(tableRow)
                                ]).then(function (_a) {
                                    var teams = _a[0], odds = _a[1];
                                    var match = {
                                        firstTeamName: teams[0].toLowerCase(),
                                        secondTeamName: teams[1].toLowerCase(),
                                        firstTeamOdds: parseFloat(odds[0].toLowerCase()),
                                        secondTeamOdds: parseFloat(odds[1].toLowerCase())
                                    };
                                    results.push(match);
                                });
                            }
                            return results;
                        })];
                case 12:
                    matches = _b.sent();
                    for (_i = 0, _a = utils_1.removeDupMatches(matches); _i < _a.length; _i++) {
                        match = _a[_i];
                        fs.appendFileSync(path.join(__dirname, "..", "odds", outputDirectory, outputFile), "\n" + match.firstTeamName + "," + match.secondTeamName + "," + match.firstTeamOdds + "," + match.secondTeamOdds);
                    }
                    return [4 /*yield*/, browser.close()];
                case 13:
                    _b.sent();
                    return [2 /*return*/];
            }
        });
    });
})();
