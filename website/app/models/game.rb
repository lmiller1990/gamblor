class Game < ApplicationRecord
  def winner 
    Team.find winner_id
  end

  def teams
    Team.where(id: [red_side_team_id, blue_side_team_id])
  end

  def loser
    Team.find loser_id
  end

  def red_side_team
    Team.find red_side_team_id
  end

  def blue_side_team
    Team.find blue_side_team_id
  end

  def first_baron_team
    Team.find first_baron_team_id
  end

  def first_blood_team
    Team.find first_blood_team_id
  end

  def first_turret_team
    Team.find first_turret_team_id
  end

  def first_dragon_team
    Team.find first_dragon_team_id
  end
end
