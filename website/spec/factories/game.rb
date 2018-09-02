FactoryBot.define do
  factory :game do

  end

  factory :game_with_result do
    after :create do |game|
      winner = create(:team)
      loser = create(:team)

      game.winner_id = winner.id
      game.loser_id = loser.id
    end
  end
end
