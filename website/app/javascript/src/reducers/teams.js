import { GET_TEAM } from '../actions/teams.js'

const teams = {
}

function timelineApp(state = teams, action) {
  switch (action.type) {
    case GET_TEAM:
      return {...state, , [action.id]: action.
  }
  return state
}
