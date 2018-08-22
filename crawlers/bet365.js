const fs = require("fs")
const puppeteer = require("puppeteer")
const { options } = require("./launch-options")


const markets = [
  'team to draw first blood',
  //  'team to draw first blood - map 1',
  // 'team to draw first blood - map 2',
  // 'team to draw first blood - map 3',
  'team to destroy the first tower',
  'team to slay the first dragon',
]

function attachMarketToWindow(page, market) {
  return page.evaluate(`
      if (typeof market !== 'undefined') {
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

    /* TODO: delete?
  const windowSet = (page, name, value) => {
    page.evaluateOnNewDocument(`
      Object.defineProperty(window, 'markets', {
        get() {
          return [
            'team to draw first blood',
            'team to destroy the first tower',
            'team to slay the first dragon',
          ]
        }
      })
    `)
  }
  await windowSet(page)*/

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
    await page.waitForSelector(".sm-MarketGroup_HeaderOpen ")

    await page.$$eval(".sm-MarketGroup_GroupName ", (divs) => {
      console.log("Getting odds for " + market)
      // TODO: loop each league
      // league -> market -> back -> another league
      // makes more sense to put all markets in a single place 
      leagues = []
        /*
      for (let div of divs) {
        if (div.innerText.includes("LOL")) {
          leagues.push(div)
        }
      }*/
      console.log("leagues", leagues)
      for (let div of divs) {
        if (div.innerText.includes("LOL")) {
          const table = div.parentElement.parentElement
          table.querySelectorAll(".sm-CouponLink_Label ").forEach(x => {
            if (x.innerText.toLowerCase().includes(market)) {
              x.click()
            }
          })
        }
      }
    })

    await page.waitForSelector(".cm-CouponMarketGroupButton_Title")

    const [ theMarket, theResults ] = await page.$eval(".gl-MarketGroupContainer ", (el) => {
      const groups = el.querySelectorAll(".cm-MarketSubGroup ")
      const results = []
      for (let g of groups) {
        const matchup = g.querySelector(".cm-MarketSubGroup_Label").innerText
        const teamsAndOdds = 
          matchup.substr(0, matchup.indexOf("-"))
          .split("vs")
          .map(x => x.trim())
          .map(x => x.toLowerCase())

        const odds = g.nextElementSibling.querySelectorAll(".gl-Participant_Odds")
        odds.forEach(odd => teamsAndOdds.push(odd.innerText))
        results.push(teamsAndOdds)
      }
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
