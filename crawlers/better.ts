import * as fs from "fs"
import * as puppeteer from "puppeteer"
import { options } from "./launch-options"

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
const getTeams = (function getTeams(el) {
  return Array.from(el.querySelectorAll(".gl-Participant_Name"))
    .map((x: HTMLElement) => x.innerHTML)
})

/**
 * @param {HTMLElement} 
 * Contains <span class="gl-Participant_Odds">{odds}</span>
 */  
const getOdds = (el => {
  return Array.from(el.querySelectorAll(".gl-Participant_Odds"))
    .map((x: HTMLElement) => x.innerHTML)
})

const visitEsportsPage = (async page => {
  await page.goto("https://www.bet365.com.au/")
  await page.mainFrame().waitForSelector(".wn-Classification ")

  await page.$$eval(".wn-Classification ", divs => 
    (Array.from(divs)
    .find((x: HTMLElement) => x.innerText.includes("Esports")) as HTMLElement)
    .click()
  )
})

const main = (async function main() {
  
  console.log("Executing")
  const browser = await puppeteer.launch(options)
  const page = await browser.newPage()

  await visitEsportsPage(page)
  await page.mainFrame().waitForSelector(".sm-MarketGroup_GroupName ")

  await page.$$eval(".sm-MarketGroup_GroupName ", (divs) => {
    const theLeague: HTMLElement = Array.from(divs)
      .find((x: HTMLElement) => x.innerText.toLowerCase().includes('na lcs')) as HTMLElement
    // the table containing all the markets
    //
    const table: HTMLElement = theLeague.parentElement.parentElement
    const market = (Array.from(table.querySelectorAll(".sm-CouponLink_Label "))
      .find((x: HTMLElement) => x.innerText.toLowerCase().includes("draw first blood")) as HTMLElement)
      .click()
    
  })

  await page.waitForSelector(".cm-CouponMarketGroupButton_Title")
  console.log("Here")
  await attachToWindow(page, 'getTeams', getTeams)
  await attachToWindow(page, 'getOdds', getOdds)
  await page.$eval(".gl-MarketGroup", (marketGroup) => {
      
    const tableRows: Array<Element> = Array.from(marketGroup.querySelectorAll(".gl-Market_General"))
    for (const tableRow of tableRows) {
      Promise.all([
        getTeams(tableRow),
        getOdds(tableRow)
      ]).then(([ teams, odds ]) => {
        console.log(teams)
        console.log(odds)
      })
    }
  })
})()

// main()
