const fs = require("fs")
const puppeteer = require("puppeteer")
const { options } = require("./launch-options")


const leaguesToScape = [
  "NA LCS",
  "EU LCS"
]

const markets = [
  'team to draw first blood',
  //  'team to draw first blood - map 1',
  // 'team to draw first blood - map 2',
  // 'team to draw first blood - map 3',
  'team to destroy the first tower',
  'team to slay the first dragon',
]

function getTeamNamesAndOddsFromContainer(marketGroupContainer) {
  const results = []
  const groups = marketGroupContainer.querySelectorAll(".cm-MarketSubGroup ")
  for (let group of groups) {
    const matchup = group.querySelector(".cm-MarketSubGroup_Label").innerText
    const teamsAndOdds = 
      matchup.substr(0, matchup.indexOf("-"))
      .split("vs")
      .map(x => x.trim())
      .map(x => x.toLowerCase())

    const odds = group.nextElementSibling.querySelectorAll(".gl-Participant_Odds")
    odds.forEach(odd => teamsAndOdds.push(odd.innerText))
    results.push(teamsAndOdds)
  }

  return results
}

function clickMarket(market, table) {
  table.querySelectorAll(".sm-CouponLink_Label ").forEach(x => {
    if (x.innerText.toLowerCase().includes(market)) {
      x.click()
    }
  })
}

function attachToWindow(page, propName, propVal) {
  return page.evaluate(`
      if (typeof ${propName} === 'undefined') {
        Object.defineProperty(window, '${propName}', {
          get() { return ${propVal} }
        })
      } else if (typeof ${propName} === 'string') {
        ${propName} = ${propVal}
      } else {
      }
    `)
}

function attachMarketToWindow(page, market) {
  return page.evaluate(`
      if (typeof market === 'undefined') {
        Object.defineProperty(window, 'market', {
          get() {
            return '${market}'
          }
        }) 
      } else {
        market = '${market}'
      }
    `)
}

function clearPreviouslyScrapedData() {
  try {
    fs.unlinkSync("results.txt")
  } catch(e) {
    fs.writeFileSync("results.txt")
  }
}

async function getPic() {
  clearPreviouslyScrapedData()
  const browser = await puppeteer.launch(options)
  const page = await browser.newPage()

  await page.goto("https://www.bet365.com.au/")
  await page.waitForSelector(".wc-HomePageHeader")
  await page.waitForSelector(".wn-Classification ")
  await page.mainFrame().waitForSelector(".wn-Classification ")

  const divsCounts = await page.$$eval(".wn-Classification ", (divs) => {
    for (let div of divs) {
      if (div.innerText.includes("Esports")) {
        div.click()
      }
    }
  })

  const marketOdds = {}

  for (let market of markets) {
    await attachMarketToWindow(page, market)
    await attachToWindow(page, 'clickMarket', clickMarket)
    await attachToWindow(page, 'leaguesToScape', JSON.stringify(leaguesToScape))
    await page.waitForSelector(".sm-MarketGroup_HeaderOpen ")

    const leagues = await page.$$eval(".sm-MarketGroup_GroupName ", (divs) => {
      console.log("Getting odds for " + market)
      // TODO: loop each league
      // league -> market -> back -> another league
      // makes more sense to put all markets in a single place 
      // or does it??
      leagues = []
      let id = 0
      for (let div of divs) {
        if (leaguesToScape.some(x => div.innerText.includes(x))) {
          id += 1
          div.parentElement.parentElement.setAttribute("id", "league-" + id)
          leagues.push("league-" + id)
        }
      }

      return leagues
    })

    for (let id of [leagues[0]]) {
      const theId = "#" + id
      await page.$eval(theId, (table) => {
        // const table = // theLeague.parentElement.parentElement
        clickMarket(market, table)
      })
    }

    await page.waitForSelector(".cm-CouponMarketGroupButton_Title")
    await attachToWindow(page, 'getTeamNamesAndOddsFromContainer', getTeamNamesAndOddsFromContainer)

    const [ theMarket, theResults ] = await page.$eval(".gl-MarketGroupContainer ", (marketGroupContainer) => {
      const results = getTeamNamesAndOddsFromContainer(marketGroupContainer)

      return [ market, results ]
    })

    fs.appendFileSync("results.txt", theMarket + "\n")
    for (let data of theResults) {
      fs.appendFileSync("results.txt", data.join(",").toString() + "\n")
    }

    await page.goBack()
  }

  await page.waitForSelector(".sm-MarketGroup_HeaderOpen")
  await browser.close()
}

getPic()
