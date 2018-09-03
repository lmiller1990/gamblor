class Game < ApplicationRecord
  def winner 
    Team.find winner_id
  end

  def loser
    Team.find loser_id
  end

  def teams
    Team.where(id: [red_side_team_id, blue_side_team_id])
  end
end
