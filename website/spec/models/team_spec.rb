require 'rails_helper'

describe Team do
  describe '#games' do
    let!(:team)  { create(:team) }
    let!(:victory) { create(:game, winner_id: team.id) }
    let!(:defeat) { create(:game, loser_id: team.id) }

    it 'returns games played' do
      expect(team.games).to eq [victory, defeat]
    end
  end
end