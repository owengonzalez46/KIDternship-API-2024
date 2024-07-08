#!/bin/bash

# Load environment variables from .env file
if [[ -f ./.env ]]; then
  source ./.env
else
  echo "Error: .env file not found!"
  exit 1
fi

WORDS=("API" "integration" "software" "applications" "developers" "robust" "scalable" "solutions" "RESTful" "services" "HTTP" "protocols" "JSON" "payloads" "data" "exchange" "authentication" "authorization" "mechanisms" "programming" "languages" "Python" "JavaScript" "Java" "libraries" "frameworks" "interact" "efficiency" "productivity" "OAuth" "JWT" "keys" "secure" "access" "rate" "limiting" "caching" "optimize" "performance" "Webhooks" "endpoints" "SDKs" "streamline" "development" "processes" "understanding" "documentation" "versioning" "error" "handling" "crucial" "successful" "implementation" "continuous" "testing" "monitoring" "maintain" "reliability" "functionality" "request" "response" "methods" "URI" "client" "server" "status" "codes" "headers" "payload" "resource" "REST" "SOAP" "graphQL")

# Export the password to avoid being prompted
export PGPASSWORD=$DB_PASSWORD

# Truncate the wordcloud table
  psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER" -d "$DATABASE_NAME" -c "TRUNCATE TABLE wordcloud;"

#Modify this for the prepopulation of words into the database.
for i in {1..50}
do
  WORD=${WORDS[$RANDOM % ${#WORDS[@]}]}
  curl -X POST https://api-kidternship.thegonzalezes.io/wordcloud/words -H "Content-Type: application/json" -d "{\"word\": \"$WORD\"}"
done

echo "Database has been truncated, example words have been inserted."

# Unset the password environment variable
unset PGPASSWORD