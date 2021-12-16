FROM python:3.9.7
WORKDIR /usr/src/app

# 1 to avoid reinstall the pacjages every time we make a change on the code we copy the requirements.txt file first
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# 2 then we copy the code
COPY . .
# 3 then we run the code
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
