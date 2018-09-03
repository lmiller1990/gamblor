class GamesController < ApplicationController
  before_action :set_game, only: [:show, :edit, :update]
  def new
    @game = Game.new
    @teams_for_select = Team.all.collect {|t| [ t.name, t.id ] }
  end

  def show
  end

  def create
    game = Game.create!(game_params)

    redirect_to game
  end

  def edit
    @teams_for_select = @game.teams.collect {|t| [ t.name, t.id ] }
  end

  def update
    @game.update_attributes(game_params)
  end

  private

  def game_params
    params.require(:game).permit(
      :blue_side_team_id, :red_side_team_id, :date,
      :first_blood_team_id, :first_turret_team_id,
      :first_baron_team_id, :first_dragon_team_id
    )
  end

  def set_game
    @game = Game.find(params[:id])
  end
end
