class Game < ApplicationRecord
  FIRST_MARKETS = %w(blood turret dragon baron).freeze

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


  def first_turret_team
    Team.find first_turret_team_id
  end

  def first_dragon_team
    Team.find first_dragon_team_id
  end

  def first_team_to_get(market)
    Team.find self["first_#{market}_team_id".to_sym]
  end

  def player_to_get_first(market)
    Player.find(self["first_#{market}_player_id".to_sym])
  end
end
