Change Directory:

```
cd token-tracker-backend
```

Create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the dependencies:

```
pip install -r requirements.txt
```

Run the file:

```
uvicorn app.main:app --reload
```
