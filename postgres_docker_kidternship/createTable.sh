#!/bin/bash

# Load environment variables from .env file
if [[ -f ./.env ]]; then
  source ./.env
else
  echo "Error: .env file not found!"
  exit 1
fi

# Function to execute SQL commands
execute_sql() {
  local command="$1"
  psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER" -d "$DATABASE_NAME" -c "$command"
  local status=$?
  if [ $status -ne 0 ]; then
    echo "Error: Failed to execute SQL command: $command"
    exit $status
  fi
}

# Define SQL commands for menu table
SQL_MENU=$(cat <<EOF
-- Table: public.menu

-- DROP TABLE IF EXISTS public.menu;

CREATE TABLE IF NOT EXISTS public.menu
(
    uuid uuid NOT NULL,
    menuitem character varying COLLATE pg_catalog."default" NOT NULL,
    category character varying COLLATE pg_catalog."default" NOT NULL,
    flavor character varying COLLATE pg_catalog."default",
    size character varying COLLATE pg_catalog."default",
    temperature character varying COLLATE pg_catalog."default",
    CONSTRAINT menu_pkey PRIMARY KEY (uuid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.menu
    OWNER to "$DATABASE_USER"; 
EOF
)

# Define SQL commands for orders table
SQL_ORDERS=$(cat <<EOF
-- Table: public.orders

-- DROP TABLE IF EXISTS public.orders;

CREATE TABLE IF NOT EXISTS public.orders
(
    orderid character varying COLLATE pg_catalog."default" NOT NULL,
    status character varying COLLATE pg_catalog."default" NOT NULL,
    item character varying COLLATE pg_catalog."default" NOT NULL,
    flavor character varying COLLATE pg_catalog."default",
    size character varying COLLATE pg_catalog."default",
    temperature character varying COLLATE pg_catalog."default",
    notes character varying COLLATE pg_catalog."default",
    CONSTRAINT orders_pkey PRIMARY KEY (orderid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.orders
    OWNER to "$DATABASE_USER"; 
EOF
)

# Define SQL commands for wordcloud table
SQL_WORDCLOUD=$(cat <<EOF
-- Table: public.wordcloud

-- DROP TABLE IF EXISTS public.wordcloud;

CREATE TABLE IF NOT EXISTS public.wordcloud
(
    uuid uuid NOT NULL,
    words text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT wordcloud_pkey PRIMARY KEY (uuid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.wordcloud
    OWNER to "$DATABASE_USER"; 
EOF
)

# Export the password to avoid being prompted
export PGPASSWORD=$DATABASE_PASS

# Execute SQL commands
execute_sql "$SQL_MENU"
execute_sql "$SQL_ORDERS"
execute_sql "$SQL_WORDCLOUD"

echo "Tables created successfully: menu, orders, wordcloud."

# Unset the password environment variable
unset PGPASSWORD
