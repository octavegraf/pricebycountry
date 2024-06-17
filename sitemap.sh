#!/bin/bash

SUBSCRIPTIONS_URL="https://octavegraf.github.io/pricebycountry/subscriptions_list.json"

BASE_URL="https://octavegraf.github.io/pricebycountry/"

curl -s $SUBSCRIPTIONS_URL -o subscriptions_list.json

echo '<?xml version="1.0" encoding="UTF-8"?>' > sitemap.xml
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' >> sitemap.xml

STATIC_PAGES=(
  "${BASE_URL}"
  "${BASE_URL}about.html"
  "${BASE_URL}contact.html"
)

for PAGE in "${STATIC_PAGES[@]}"; do
  echo "  <url>" >> sitemap.xml
  echo "    <loc>${PAGE}</loc>" >> sitemap.xml
  echo "  </url>" >> sitemap.xml
done

jq -r '.Subscriptions[] | .Path' subscriptions_list.json | while read path; do
  FILE_NAME=$(basename "$path" .json)
  URL="${BASE_URL}subscription/?file=${FILE_NAME}"
  echo "  <url>" >> sitemap.xml
  echo "    <loc>${URL}</loc>" >> sitemap.xml
  echo "  </url>" >> sitemap.xml
done

echo '</urlset>' >> sitemap.xml

rm subscriptions_list.json

echo "Sitemap generated successfully!"
