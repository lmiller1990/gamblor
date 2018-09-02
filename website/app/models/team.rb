class Team < ApplicationRecord
  def games
    Game.where(winner_id: id).or(Game.where(loser_id: id))
  end
end
