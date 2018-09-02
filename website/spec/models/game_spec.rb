require 'rails_helper'

describe Game do
  context 'the game is complete' do
    let!(:game) { create(:game) }
    let!(:winner) { create(:team) }
    let!(:loser) { create(:team) }

    before do
      game.winner_id = winner.id
      game.loser_id = loser.id
    end

    it 'has a winning and losing team' do
      expect(game.winner).to eq winner
      expect(game.loser).to eq loser
    end
  end
end
