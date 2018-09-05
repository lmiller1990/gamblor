adc = Position.create!(name: 'ADC')
support = Position.create!(name: 'Support')
jungle = Position.create!(name: 'Jungle')
top = Position.create!(name: 'Top')
middle = Position.create!(name: 'Middle')

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

Player.create!(
  name: "Doublelift",
  position_id: adc.id
)
