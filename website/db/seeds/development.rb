Team.create!(name: 'Cloud 9')
Team.create!(name: 'Team Solomid')
Team.create!(name: '100 Thieves')

Game.create!(
  winner_id: Team.first.id, 
  loser_id: Team.second.id,
  blue_side_team_id: Team.first.id,
  red_side_team_id: Team.second.id,
  first_blood_team_id: Team.first.id,
  first_turret_team_id: Team.second.id,
  date: DateTime.now
)
