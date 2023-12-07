#!/bin/bash

# Define global variables
CWD=$(pwd)

# Read config settings
WAVEDUMP_CONFIG_FILE=$(           grep -w "WAVEDUMP_CONFIG_FILE"           config | cut -d'=' -f2)
WAVEDUMP_OUTPUT_PATH=$(           grep -w "WAVEDUMP_OUTPUT_PATH"           config | cut -d'=' -f2)
WATCHER_LOG_PATH=$(               grep -w "WATCHER_LOG_PATH"               config | cut -d'=' -f2)
DATABASE_SERVER_HOST=$(           grep -w "DATABASE_SERVER_HOST"           config | cut -d'=' -f2)
DATABASE_SERVER_DATA_DIRECTORY=$( grep -w "DATABASE_SERVER_DATA_DIRECTORY" config | cut -d'=' -f2)
LOAD_PERIOD_SECONDS=$(            grep -w "LOAD_PERIOD_SECONDS"            config | cut -d'=' -f2)
CSV_OUTPUT_PATH=$(                grep -w "CSV_OUTPUT_PATH"                config | cut -d'=' -f2)
REMOTE_DIR_TMP=$(                 grep -w "REMOTE_DIR_TMP"                 config | cut -d'=' -f2)
MYSQL_USER=$(                     grep -w "MYSQL_USER"                     config | cut -d'=' -f2)
MYSQL_PASSWORD=$(                 grep -w "MYSQL_PASSWORD"                 config | cut -d'=' -f2)
MYSQL_DATABASE=$(                 grep -w "MYSQL_DATABASE"                 config | cut -d'=' -f2)
MYSQL_TABLE=$(                    grep -w "MYSQL_TABLE"                    config | cut -d'=' -f2)