FROM python:3

WORKDIR /Users/user/Dev/Sigma-Terminal/_main_

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./


CMD [ "python", "./run_app.py" ]