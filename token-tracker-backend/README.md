# Project setup (w/o Docker)

- Change Directory:

```
cd token-tracker-backend
```

- Create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

- Install the dependencies:

```
pip install -r requirements.txt
```

- Run the file:

```
uvicorn app.main:app --reload
```

# Docker Setup (Local Development + Testing)

- Start services and build dockerfile

```
docker compose up --build
```

- Stop and remove containers

```
docker compose down # to remove volumes add --volumes
```

## Grafana

Visit `http://localhost:3000` and login using `admin` and `admin`

- Add promtheus as data source
  - URL = `http://prometheus:9090`
  - Leave auth disabled
  - Save
- Add tempo as data source
  - URL = `http://tempo:3200`
  - Leave auth disabled
  - Save

### Trigger metrics (testing)

Open terminal

```
curl -X POST http://localhost:8000/debug/test    # for metrics
curl -X POST http://localhost:8000/debug/span    # for traces
```

### View Output

##### View Metrics

- Click Explore, select Prometheus, select `chat_token_usage_total` or `chat_request_latency_seconds_count` as metric and run query

##### View Traces

- Click Explore, select Tempo, select Query type as `Search`, then select `token-tracker-service` as Service Name and run query
