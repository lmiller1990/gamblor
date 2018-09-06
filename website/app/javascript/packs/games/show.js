import axios from 'axios'

document.addEventListener('DOMContentLoaded', () => {
  const selects = document.querySelectorAll('.side_select')

  for (let select of selects) {
    select.addEventListener('change', async (e) => {
      const teamId = e.target.value

      const res = await axios.get(`/api/v1/teams/${teamId}`)
      console.log(res.data.players)
    })
  }
})
