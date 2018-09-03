Rails.application.routes.draw do
  get 'app', to: 'app#index'

  resources :games

  namespace :api do
    namespace :v1 do
      resources :teams, only: [:show, :index]
      resources :games, only: [:show, :index, :create, :update]
    end
  end
end
