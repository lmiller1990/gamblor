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
  crawl "first blood"  "na lcs" "bet365.csv" "fb"
  crawl "first dragon" "na lcs" "bet365.csv" "fd"
  crawl "first tower"  "na lcs" "bet365.csv" "ft"
  crawl "first baron"  "na lcs" "bet365.csv" "fbaron"
}

main
