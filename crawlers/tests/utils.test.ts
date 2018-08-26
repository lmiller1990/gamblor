import { Match } from "../better"
import { removeDupMatches } from "../utils"

const match: Match = { 
  firstTeamName: 'echo fox',
  firstTeamOdds: 1.5,
  secondTeamName: 'flyquest',
  secondTeamOdds: 4.2
}

const matches: Match[] = [ match, match ]

describe("removeDupMatches", () => {
  it("removes matches that have the exact same keys", () => {
    const result = removeDupMatches(matches)

    expect(result).toEqual([ match ])
  })
})