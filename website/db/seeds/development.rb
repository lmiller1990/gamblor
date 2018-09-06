adc = Position.create!(name: 'ADC')
support = Position.create!(name: 'Support')
jungle = Position.create!(name: 'Jungle')
top = Position.create!(name: 'Top')
middle = Position.create!(name: 'Middle')

c9 = Team.create!(name: 'Cloud 9')
tsm = Team.create!(name: 'Team Solomid')
tl = Team.create!(name: 'Team Liquid')

Game.create!(
  winner_id: Team.first.id, 
  loser_id: Team.second.id,
  blue_side_team_id: Team.first.id,
  red_side_team_id: Team.second.id,
  first_blood_team_id: Team.first.id,
  first_turret_team_id: Team.second.id,
  date: DateTime.now
)

doublelift = Player.create!(name: "Doublelift", position_id: adc.id)
xmithie = Player.create!(name: "Xmithie", position_id: jungle.id)
impact = Player.create!(name: "Impact", position_id: top.id)

sneaky = Player.create!(name: "Sneaky", position_id: adc.id)
jensen = Player.create!(name: "Jensen", position_id: middle.id)

bjergsen = Player.create!(name: "Bjergsen", position_id: middle.id)
hauntzer = Player.create!(name: "Hauntzer", position_id: top.id)

Contract.create!(player: sneaky, team: c9, start: 3.year.ago)
Contract.create!(player: doublelift, team: tl, start: 1.year.ago)
Contract.create!(player: doublelift, team: tsm, start: 2.years.ago, end: 1.year.ago)
Contract.create!(player: xmithie, team: tl, start: 2.years.ago)
Contract.create!(player: jensen, team: c9, start: 2.years.ago)
Contract.create!(player: bjergsen, team: tsm, start: 3.years.ago)
Contract.create!(player: hauntzer, team: tsm, start: 2.years.ago)
