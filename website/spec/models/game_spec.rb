require 'rails_helper'

describe Game do
  let!(:blue_side_team) { create(:blue_side_team) }
  let!(:red_side_team) { create(:red_side_team) }
  let!(:game) { 
    create(:game, 
           winner_id: blue_side_team.id, 
           loser_id: red_side_team.id,
           first_baron_team_id: red_side_team.id,
           first_blood_team_id: red_side_team.id,
           first_turret_team_id: red_side_team.id,
           first_dragon_team_id: red_side_team.id,
           blue_side_team_id: blue_side_team.id,
           red_side_team_id: red_side_team.id) }

  describe '#winner' do
    it { expect(game.winner).to eq blue_side_team }
  end

  describe '#loser' do
    it { expect(game.loser).to eq red_side_team }
  end
  
  describe '#blue_side_team' do
    it { expect(game.blue_side_team).to eq blue_side_team }
  end

  describe '#red_side_team' do
    it { expect(game.red_side_team).to eq red_side_team }
  end

  describe '#first_baron_team' do
    it { expect(game.first_baron_team).to eq red_side_team }
  end

  describe '#first_dragon_team' do
    it { expect(game.first_dragon_team).to eq red_side_team }
  end

  describe '#first_turret_team' do
    it { expect(game.first_turret_team).to eq red_side_team }
  end

  describe '#first_blood_team' do
    it { expect(game.first_blood_team).to eq red_side_team }
  end

  describe '#teams' do
    it { expect(game.teams).to eq [blue_side_team, red_side_team] }
  end
end
