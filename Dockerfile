FROM debian
RUN apt update
RUN apt install git python3 python3-pip tesseract-ocr-tur tesseract-ocr-rus tesseract-ocr-ell tesseract-ocr -y

CMD git clone https://github.com/Nordick-24/photo-translate; pip3 install -r photo-translate/requirements.txt; export TELEGRAM_KEY="5759242728:AAFyV9nbjLD2S4tigU6qF7IkSLJJ-E095jw"; python3 photo-translate/main.py



