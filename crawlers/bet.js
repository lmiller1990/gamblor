const fs = require("fs")
const puppeteer = require("puppeteer")
const { options } = require("./launch-options")

const theEvent = "NA LCS"
const theMarket = "Team to Draw First Blood"

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
/**
 * @param {HTMLElement} 
 * Contains <span class="gl-Participant_Name">{teamNAme}</span>
 */  
async function getTeams(el) {
  return Array.from(el.querySelectorAll(".gl-Participant_Name"))
    .map(x => x.innerHTML)
}

/**
 * @param {HTMLElement} 
 * Contains <span class="gl-Participant_Odds">{odds}</span>
 */  
async function getOdds(el) {
  return Array.from(el.querySelectorAll(".gl-Participant_Odds"))
    .map(x => x.innerHTML)
}

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

  await page.waitForSelector(".cm-CouponMarketGroupButton_Title")
  await attachToWindow(page, 'getTeams', getTeams)
  await attachToWindow(page, 'getOdds', getOdds)
  await page.$eval(".gl-MarketGroup", async (marketGroup) => {
      const tableRows = marketGroup.querySelectorAll(".gl-Market_General")
    for (const tableRow of tableRows) {
      const teams = await getTeams(tableRow)
      const odds = await getOdds(tableRow)
      console.log(teams)
      console.log(odds)

    }
  })
}

main()
