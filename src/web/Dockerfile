FROM python:3.11

RUN apt-get update

RUN apt-get install -y curl wget

ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

RUN pip3 install -U pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN /root/.cargo/bin/uv pip install --system --no-cache -r requirements.txt

COPY . /app

EXPOSE 80

CMD ["python3", "-m", "streamlit", "run", "main.py", "--server.port", "80", "--server.enableCORS", "false","--server.enableXsrfProtection", "false"]