#!/bin/bash

# Author: Caleb Trepowski
# Last modification date: 07/Dec/2023

##############################  DEFINE VARIABLES  ###############################

source ./common.sh

#################################################################################

###########################  Wavedump Output Watcher  ###########################

schedule_watcher(){
  nohup bash ./data_process.sh $WAVEDUMP_OUTPUT_PATH >> $WATCHER_LOG_PATH 2>&1 & watcher_pid=$!
  echo "Watcher PID: $watcher_pid"
}

cleanup_watcher(){
  echo -e "\nWavedump finished, killing watcher..."
  kill "$watcher_pid"
  # returnValue=$?
  if [ $? -ne 0 ]; then
    echo "Couldnt kill Watcher with PID $watcher_pid."
  else
    echo "Watcher with PID $watcher_pid killed succesfully."
  fi
}

#################################################################################


#################################  Main program  ################################

schedule_watcher
trap cleanup_watcher EXIT

wavedump $WAVEDUMP_CONFIG_FILE $WAVEDUMP_OUTPUT_PATH