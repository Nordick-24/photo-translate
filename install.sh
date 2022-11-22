#!/bin/bash
meis="$(whoami)"

if [ "$meis" = "root" ]; then

	apt-get update
	apt-get install git python3 python3-pip tesseract-ocr tesseract-ocr-rus tesseract-ocr-ell tesseract-ocr-tur -y
	pip3 install -r requirements.txt

	echo done!

else

	echo "I need root persmissions! try 'sudo !!'"

fi
