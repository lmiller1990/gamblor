require 'rails_helper'

describe Game do
  let!(:blue_side_team) { create(:blue_side_team) }
  let!(:red_side_team) { create(:red_side_team) }
  let!(:game) { 
    create(:game, winner_id: blue_side_team.id, loser_id: red_side_team.id) }

  describe '#winner' do
    it { expect(game.winner).to eq blue_side_team }
  end

  describe '#loser' do
    it { expect(game.loser).to eq red_side_team }
  end

  describe '#teams' do
    it { expect(game.teams).to eq [blue_side_team, red_side_team] }
  end
end
