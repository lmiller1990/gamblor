Rails.application.routes.draw do
  get 'app', to: 'app#index'
  get 'admin', to: 'admin#index'

  resources :games
  resources :players

  namespace :api do
    namespace :v1 do
      resources :teams, only: [:show, :index]
      resources :games, only: [:show, :index, :create, :update]
    end
  end
end
