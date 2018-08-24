import * as fs from "fs"
import { options } from "./launch-options"
import * as puppeteer from "puppeteer";

interface Match {
  firstTeamName: String
  secondTeamName: String
  firstTeamOdds: Number
  secondTeamOdds: Number
}

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

function clearPreviouslyScrapedData() {
  try {
    fs.unlinkSync("results.txt")
  } catch(e) {
    // doesn't exist
  }

  fs.appendFileSync("results.txt", "team_1,team_2,team_1_odds,team_2_odds")
}

function getTeams(el: HTMLElement) {
  return Array.from(el.querySelectorAll(".gl-Participant_Name"))
    .map((x: HTMLElement) => x.innerHTML)
}

function getOdds(el: HTMLElement) {
  return Array.from(el.querySelectorAll(".gl-Participant_Odds"))
    .map((x: HTMLElement) => x.innerHTML)
}

const visitEsportsPage = (async (page: puppeteer.Page) => {
  await page.goto("https://www.bet365.com.au/")
  await page.mainFrame().waitForSelector(".wn-Classification ")

  await page.$$eval(".wn-Classification ", divs => 
    (Array.from(divs)
    .find((x: HTMLElement) => x.innerText.includes("Esports")) as HTMLElement)
    .click()
  )
})

const main = (async function main() {

  clearPreviouslyScrapedData()
  const browser: puppeteer.Browser = await puppeteer.launch(options)
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
  await attachToWindow(page, 'getTeams', getTeams)
  await attachToWindow(page, 'getOdds', getOdds)

  const matches: Match[] = await page.$eval(".gl-MarketGroup", (marketGroup) => {
    const results: Match[] = []

    const tableRows: Array<Element> = Array.from(marketGroup.querySelectorAll(".gl-Market_General"))

    for (const tableRow of tableRows) {
      Promise.all([
        getTeams(tableRow as HTMLElement),
        getOdds(tableRow as HTMLElement)
      ]).then(([ teams, odds ]) => {
        const match: Match = {
          firstTeamName: teams[0].toLowerCase(),
          secondTeamName: teams[1].toLowerCase(),
          firstTeamOdds: parseFloat(odds[0].toLowerCase()),
          secondTeamOdds: parseFloat(odds[1].toLowerCase())
        } 

        results.push(match)      
      })
    }

    return results
  })

  for (const match of matches) {
    fs.appendFileSync("results.txt", `\n${match.firstTeamName},${match.secondTeamName},${match.firstTeamOdds},${match.secondTeamOdds}`)
  }
  
  await browser.close()
})()
