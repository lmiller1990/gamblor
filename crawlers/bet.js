const fs = require("fs")
const puppeteer = require("puppeteer")
const { options } = require("./launch-options")

const theEvent = "NA LCS"
const theMarket = "Team to Draw First Blood"

async function visitEsportsPage(page) {
  await page.goto("https://www.bet365.com.au/")
  await page.mainFrame().waitForSelector(".wn-Classification ")

  await page.$$eval(".wn-Classification ", divs => 
    Array.from(divs)
    .find(x => x.innerText.includes("Esports"))
    .click()
  )
}

async function main() {
  const browser = await puppeteer.launch(options)
  const page = await browser.newPage()

  await visitEsportsPage(page)
  await page.mainFrame().waitForSelector(".sm-MarketGroup_GroupName ")

  await page.$$eval(".sm-MarketGroup_GroupName ", (divs) => {
    const theLeague = Array.from(divs).find(x => x.innerText.toLowerCase().includes('na lcs'))
    // the table containing all the markets
    //
    const table = theLeague.parentElement.parentElement
    Array.from(table.querySelectorAll(".sm-CouponLink_Label "))
      .find(x => x.innerText.toLowerCase().includes("draw first blood"))
      .click()


  })
}

main()
