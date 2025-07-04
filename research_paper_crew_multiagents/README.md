# Research Paper Analyer & Future Predictor

# Application Setup #
- Run below command to install all dependent libraries
pip install -r requirements.txt

# Running project 
~ Streamlit :-
    streamlit run future_predictor.py
~ Fast API :-
    -------------------
    python api.py  
    -------------------
    uvicorn api:app 
    -------------------
~ Docker command :-
    docker build -t abhishekamar/research-paper-analyst:1.0 .
    docker push abhishekamar/research-paper-analyst:1.0