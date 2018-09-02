winner = Team.create!(name: 'Cloud 9')
loser = Team.create!(name: 'Team Solomid')

Game.create!(
  winner_id: winner.id, 
  loser_id: loser.id,
  first_blood_team_id: loser.id,
  first_turret_team_id: winner.id,
  date: DateTime.now
)
