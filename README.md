# OptiRide ETL Pipeline

A data engineering pipeline that extracts NYC Citi Bike and weather data, transforms it into a dimensional model, and loads it into PostgreSQL using PySpark and Apache Airflow.

## Architecture

```
[Citi Bike API] ──┐                    ┌─── dim_station
                  ├──► Extract ──► Transform ──► dim_weather      ──► PostgreSQL
[Weather API]  ───┘                    └─── fact_bike_weather
```

## Tech Stack

- **Orchestration:** Apache Airflow
- **Processing:** PySpark
- **Database:** PostgreSQL
- **APIs:** Citi Bike NYC, Open-Meteo Weather

## Data Model

### Dimension Tables
- **dim_station** - Bike station details (id, name, location, capacity)
- **dim_weather** - Hourly weather conditions (temperature, precipitation, wind, humidity)

### Fact Table
- **fact_bike_weather** - Bike availability joined with weather data by timestamp

## Project Structure

```
optiride_eetl/
├── extract.py          # API data extraction
├── transform.py        # PySpark transformations
├── load.py             # PostgreSQL loading
├── optiride_dag.py     # Airflow DAG definition
├── logger.py           # Custom logging utility
├── config.yaml         # Configuration file
└── requirements.txt    # Dependencies
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

Create a `config.yaml` file:

```yaml
storage:
  raw: ./data/raw
  processed: ./data/processed

database:
  host: localhost
  port: 5432
  dbname: optiride
  user: your_user
  password: your_password
```

### 3. Download PostgreSQL JDBC Driver

```bash
# Download to your preferred location
wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar
```

Update the path in `load.py` to match your driver location.

### 4. Run the Pipeline

**Manual execution:**
```bash
python extract.py
python transform.py
python load.py
```

**With Airflow:**
```bash
# Copy DAG to Airflow
cp optiride_dag.py ~/airflow/dags/

# Start Airflow
airflow standalone
```

## Pipeline Flow

1. **Extract** - Fetches real-time data from Citi Bike and Open-Meteo APIs, saves as JSON
2. **Transform** - Processes with PySpark, creates dimensional model, outputs Parquet files
3. **Load** - Creates PostgreSQL schema and tables, loads data via JDBC

## Sample Queries

```sql
-- Bike availability by weather condition
SELECT 
    w.temperature,
    w.precipitation,
    AVG(f.free_bikes) as avg_bikes
FROM optiride.fact_bike_weather f
JOIN optiride.dim_weather w ON f.weather_id = w.weather_id
GROUP BY w.temperature, w.precipitation;

-- Station utilization
SELECT 
    s.station_name,
    AVG(f.free_bikes) as avg_available,
    AVG(f.slots) as avg_capacity
FROM optiride.fact_bike_weather f
JOIN optiride.dim_station s ON f.station_id = s.station_id
GROUP BY s.station_name
ORDER BY avg_available DESC;
```

## Author

Chima Ojini

## License

MIT
