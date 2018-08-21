const puppeteer = require("puppeteer")
const fs = require("fs")


const markets = ['Team to Draw First Blood']

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
  const browser = await puppeteer.launch(options)
  // await page.setViewport({width: 1000, height: 500})

  // const preloadFile = fs.readFileSync('./crawlers/preload.js', 'utf8');

  const page = await browser.newPage()

  const windowSet = (page, name, value) => {
    page.evaluateOnNewDocument(`
      Object.defineProperty(window, 'markets', {
        get() {
          return ['Team to Draw First Blood']
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

  await page.waitForSelector(".sm-MarketGroup_HeaderOpen ")

  await page.$$eval(".sm-MarketGroup_GroupName ", (divs) => {
    for (let div of divs) {
      if (div.innerText.includes("LOL")) {
        const table = div.parentElement.parentElement
        table.querySelectorAll(".sm-CouponLink_Label ").forEach(x => {
          if (x.innerText.includes(markets[0])) {
            //console.log(x.innerText, "includes", markets[0])
            //console.log('clicking', x)
            x.click()
          }
        })
      }
    }
  })

  await page.waitForSelector(".cm-CouponMarketGroupButton_Title")

  await page.$eval(".gl-MarketGroupContainer ", (el) => {
    const groups = el.querySelectorAll(".cm-MarketSubGroup ")
    for (let g of groups) {
      console.log(g)
      const matchup = g.querySelector(".cm-MarketSubGroup_Label").innerText
      const teams = 
        matchup.substr(0, matchup.indexOf("-"))
        .split("vs")
        .map(x => x.trim())
        .map(x => x.toLowerCase())

      const odds = g.nextElementSibling.querySelectorAll(".gl-Participant_Odds")
      odds.forEach(odd => teams.push(odd.innerText))
      console.log(teams)
    }
  })


  await page.waitForSelector(".sm-MarketGroup_HeaderOpen")
  // await browser.close()
}

getPic()
