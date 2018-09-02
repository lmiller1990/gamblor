Rails.application.routes.draw do
  get 'app', to: 'app#index'

  namespace :api do
    namespace :v1 do
      resources :teams, only: [:show, :index]
    end
  end
end
