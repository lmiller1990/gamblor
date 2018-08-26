function compile() {
  echo "Compiling..."
  tsc crawlers/better.ts
}

function crawl() {
  echo "Getting data for $4"
  node crawlers/better.js --market "$1" --event "$2" --outputFile "$3" --outputDirectory "$4"
}

function main() {
  compile
  crawl "first blood"  "cblol" "bet365.csv" "first_blood"
  crawl "first dragon" "cblol" "bet365.csv" "first_dragon"
  crawl "first tower"  "cblol" "bet365.csv" "first_turret"
  crawl "first baron"  "cblol" "bet365.csv" "first_baron"
}

main
