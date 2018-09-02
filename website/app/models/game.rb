class Game < ApplicationRecord
  def winner 
    Team.find winner_id
  end

  def loser
    Team.find loser_id
  end
end
