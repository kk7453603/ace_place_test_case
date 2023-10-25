FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
ENV EMAIL=test@example.com
ENV DB_URI=mongodb://mongodb:27017/
ENV SMTP_HOST=smtp.gmail.com
ENV SMTP_PORT=587
ENV SMTP_LOGIN=your_email@gmail.com
ENV SMTP_PASSWORD=your_password
ENV SMTP_EMAIL=your_email@gmail.com
ENV SMTP_NAME=user

CMD ["python3", "app.py"]