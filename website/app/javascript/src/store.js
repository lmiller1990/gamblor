import { createStore } from 'redux'

const initialState = {
  teams: {}
}

const reducer = (state, action) => {
  switch (action.type) {
    case 'GET_TEAM':
      state = {
        ...state, 
        teams: {...state.teams, 1: action.team } 
      } 
  }

  return state
}

const store = createStore(reducer, initialState)

export default store
window.store = store
