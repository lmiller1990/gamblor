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
  crawl "first blood"   "play-in" "bet365.csv" "fb"
  crawl "first dragon"  "play-in" "bet365.csv" "fd"
  crawl "first tower"   "play-in" "bet365.csv" "ft"
  crawl "first baron"   "play-in" "bet365.csv" "fbaron"
  crawl "total kills"   "play-in" "bet365.csv" "total_kills"
  crawl "total dragons" "play-in" "bet365.csv" "total_dragons"
  crawl "total barons"  "play-in" "bet365.csv" "total_barons"
  crawl "total towers"  "play-in" "bet365.csv" "total_towers"
  crawl "to win"        "play-in" "bet365.csv" "to_win"
}

main
