#!/bin/bash

echo [$(date)]: "START"
echo "Creating base file..."

echo "Enter week number: "
read weekno

if cp driver_folder/base.ipynb docs/week${weekno} ; then
  echo "File copied successfully."
else
  echo "Error copying file!"
  exit 1  # Exit script with error code 1
fi

echo "Enter lecture number: "
read lec_name

mv docs/week${weekno}/base.ipynb docs/week${weekno}/${lec_name}.ipynb

if [ $? -eq 0 ]; then
  echo "File renamed successfully."
else
  echo "Error renaming file!"
fi

echo [$(date)]: "END"
