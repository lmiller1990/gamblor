import axios from 'axios'

export const GET_TEAM = 'GET_TEAM'

export function getTeam(id) {
  return {
    type: GET_TEAM,
    id
  }
}
