class GamesController < ApplicationController
  before_action :set_game, only: [:show, :edit, :update]
  before_action :set_teams, only: [:show, :edit, :update]

  def index
    @games = Game.all.order(date: :asc)
  end

  def new
    @game = Game.new
  end

  def show
    set_first_teams
  end

  def create
    game = Game.create!(game_params)

    redirect_to game
  end

  def edit
    set_players_for_first
    @players_for_select = @game.teams.first.players.collect {|t| [ t.name, t.id ] }
  end

  def update
    @game.update_attributes(game_params)

    redirect_to @game
  end

  private

  # Get the correct list of players based on which team 
  # got the first blood/dragon
  def set_players_for_first
    Game::FIRST_MARKETS.each do |market|
      team_id =  @game["first_#{market}_team_id".to_sym]

      if team_id
        players = Team.find(team_id).players
        instance_variable_set(
          "@players_for_first_#{market}", players.collect {|p| [ p.name, p.id ] } 
        )
      end
    end
  end

  # Set the first team for each market dynamically 
  def set_first_teams
    Game::FIRST_MARKETS.each do |market|
      if @game["first_#{market}_team_id".to_sym]
        instance_variable_set(
          "@first_#{market}_team", @game.send("first_team_to_get", market).name)
      else
      end
    end
  end

  def game_params
    params.require(:game).permit(
      :blue_side_team_id, :red_side_team_id, :date,
      :first_blood_team_id, :first_turret_team_id,
      :first_baron_team_id, :first_dragon_team_id,
      :first_blood_player_id, :first_turret_player_id,
      :first_baron_player_id, :first_dragon_player_id
    )
  end

  def set_game
    @game = Game.find(params[:id])
  end

  def set_teams
    @teams_for_select = Team.all.collect {|t| [ t.name, t.id ] }
  end
end
