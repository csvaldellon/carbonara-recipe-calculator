FROM selenium/standalone-chrome

WORKDIR /carbonara-recipe-calculator

COPY ./requirements.txt ./requirements.txt

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install -r ./requirements/api.txt

COPY . ./

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]
