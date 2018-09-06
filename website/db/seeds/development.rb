adc = Position.create!(name: 'ADC')
support = Position.create!(name: 'Support')
jungle = Position.create!(name: 'Jungle')
top = Position.create!(name: 'Top')
middle = Position.create!(name: 'Middle')

c9 = Team.create!(name: 'Cloud 9')
tsm = Team.create!(name: 'Team Solomid')
thieves = Team.create!(name: '100 Thieves')

Game.create!(
  winner_id: Team.first.id, 
  loser_id: Team.second.id,
  blue_side_team_id: Team.first.id,
  red_side_team_id: Team.second.id,
  first_blood_team_id: Team.first.id,
  first_turret_team_id: Team.second.id,
  date: DateTime.now
)

doublelift = Player.create!(
  name: "Doublelift",
  position_id: adc.id
)

sneaky = Player.create!(
  name: "Sneaky",
  position_id: adc.id
)

Contract.create!(player: sneaky, team: c9, start: 3.year.ago)
Contract.create!(player: doublelift, team: tsm, start: 1.year.ago)
Contract.create!(player: doublelift, team: c9, start: 2.years.ago, end: 1.year.ago)
