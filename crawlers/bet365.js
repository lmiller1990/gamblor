const puppeteer = require("puppeteer")
const fs = require("fs")


const markets = [
  'team to draw first blood',
  //  'team to draw first blood - map 1',
  // 'team to draw first blood - map 2',
  // 'team to draw first blood - map 3',
  'team to destroy the first tower',
  'team to slay the first dragon',
]

async function getPic() {
  const args = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-infobars',
    '--window-position=0,0',
    '--ignore-certifcate-errors',
    '--ignore-certifcate-errors-spki-list',
    '--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3312.0 Safari/532.36"',
    '--auto-open-devtools-for-tabs'
  ];

  const options = {
    args,
    headless: false,
    ignoreHTTPSErrors: true,
    userDataDir: './tmp'
  };
  try {
    fs.unlinkSync("results.txt")
  } catch(e) {
    fs.writeFileSync("results.txt")
  }
  const browser = await puppeteer.launch(options)

  const page = await browser.newPage()

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
  await windowSet(page) // , 'markets', ['Team to Draw First Blood'])

  // await page.evaluateOnNewDocument(preloadFile);
  await page.goto("https://www.bet365.com.au/")

  // await page.click("a#TopPromotionBetNow")
  await page.waitForSelector(".wc-HomePageHeader")
  await page.waitForSelector(".wn-Classification ")
  // await page.$x("//a[contains(text(), 'Esports')]")

  await page.mainFrame()
    .waitForSelector('.wn-Classification ')

  const divsCounts = await page.$$eval('.wn-Classification ', (divs) => {
    for (let div of divs) {
      if (div.innerText.includes("Esports")) {
        div.click()
      }
    }
  })

  const marketOdds = {}
  for (let market of markets) {
    await page.evaluate(`
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
    await page.waitForSelector(".sm-MarketGroup_HeaderOpen ")

    await page.$$eval(".sm-MarketGroup_GroupName ", (divs) => {
      console.log("Getting odds for " + market)
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
