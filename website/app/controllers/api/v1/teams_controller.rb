module Api
  module V1
    class TeamsController < ::ActionController::API
      def index
        render json: Team.all.where(id: [params[:ids]])
      end

      def show
        team = Team.find(params[:id])

        render json: { team: team, games: team.games }
      end
    end
  end
end

