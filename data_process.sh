#!/bin/bash

source ./common.sh

PROCESSED_FLAG="processed-"

while true; do
  sleep $LOAD_PERIOD_SECONDS
  unprocessedFiles=$(find $WAVEDUMP_OUTPUT_PATH -maxdepth 1 -type f -not -name "$PROCESSED_FLAG*" -exec ls -A1tr {} +)
  for unprocessedFile in $unprocessedFiles
  do
    lsofUnprocessedFile=$(lsof $unprocessedFile)
    if [[ $lsofUnprocessedFile ]]; then
      echo "File $unprocessedFile still used by another process"
      true
    else
      grep --text -v 'RecordLength:10RecordLength:100' $unprocessedFile > "$unprocessedFile.tmp"
      mv "$unprocessedFile.tmp" $unprocessedFile
      echo -n "$(date)  " && ./process_output.py $unprocessedFile $CSV_OUTPUT_PATH #>> $WATCHER_LOG_PATH 2>&1
      if [ $? -eq 0 ]; then
        # if [ true ]; then
        filename=$(basename "$unprocessedFile")
        extension="${unprocessedFile##*.}"
        processed_filename="processed-${filename%.*}.${extension}"
        mv "$unprocessedFile" "$WAVEDUMP_OUTPUT_PATH/$processed_filename"
        
      else
        echo -e "$(date)\t$Processing $unprocessedFile failed"
      fi
    fi
  done
  scp "$CSV_OUTPUT_PATH" "$DATABASE_SERVER_HOST:$REMOTE_DIR_TMP"
  if [ $? -eq 0 ]; then
    echo -e "$(date)\tSCP was successful"
    sql_command="mysql -u$MYSQL_USER -p'$MYSQL_PASSWORD' $MYSQL_DATABASE -e \"LOAD DATA LOCAL INFILE '$REMOTE_DIR_TMP/$(basename $CSV_OUTPUT_PATH)' INTO TABLE $MYSQL_TABLE FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES;\""
    ssh $DATABASE_SERVER_HOST $sql_command
    if [ $? -eq 0 ]; then
      echo -e "$(date)\tLoad to DB successful. Removing CSV content and processed files."
      echo -n "" > $CSV_OUTPUT_PATH
      rm $WAVEDUMP_OUTPUT_PATH"processed-"*
    else
      echo -e "$(date)\tFailed to load to DB."
    fi
  else
    echo -e "$(date)\tSCP failed."
  fi
done