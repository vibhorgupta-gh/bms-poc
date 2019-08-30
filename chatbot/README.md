# Install Dependencies
1.) pip install rasa
2.) pip install rasa[spacy]
3.) python -m spacy download en_core_web_md
4.) python -m spacy link en_core_web_md en
# Run
5.) rasa run actions& (In separate cmd)
6.) python main.py
# Interact
7.) send post requests with message in JSON format using postman(recommended) or curl(eww).
