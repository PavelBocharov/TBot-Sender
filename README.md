# ✉️ TBot Sender ✉️

![screen.jpg](screen.jpg)

## 🟢 Start project

### 1️⃣ Install `pipenv`

``` bash
pip install pipenv
```

### 2️⃣ Install dependencies

   ```bash
   pipenv install
   ```

### 3️⃣ Start project

``` bash 
uvicorn main:app --reload
```

_or_

``` bash
pipenv run uvicorn main:app --reload
``` 

_or_

``` bash
python ./main.py
``` 

### 4️⃣ Build Docker image

``` bash
docker build --no-cache -t marolok/t_sender:1.0.1 .
```

``` bash
docker push marolok/t_sender:1.0.1
```