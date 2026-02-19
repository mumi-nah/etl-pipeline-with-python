# Building ETL Pipeline with Python

This repository houses the scripts and methodologies used in extracting data from the countries API, transforming it and loading it into a postgres Database.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Architecture Flow](#architecture-flow)
- [How it works](#how-it-works)
- [Project Setup](#project-setup)
- [Logging](#logging)
- [Resources](#resources)

---

## Overview

This project implements a simple ETL (Extract, Transform, Load) pipeline in python. It extracts country data from the [REST Countries API](https://restcountries.com/v3.1/all), cleans and transforms the data, such as creating a standard calling code, add a column that counts languages spoken in each country, and loads into a postgeSQL database for storage and further analysis.

---

## Features

- Extracts countries data/information using the countries API
- Cleans and transforms the data
- Loads the clean data to a postgres database and csv for further analysis
- Modular and configurable pipeline using environment variables for replication

---

## Project Structure

```bash
etl-pipeline-with-python/
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
│
├── data/
|   └─── raw_countries_data.json
├── pipeline.log
├── requirements.txt
└── README.md
```

---

## Architecture Flow

![Architecture flow](image/workflow.svg)

---

## How it works

**Extract**

- Calls the REST Countries API.
- Saves raw JSON to `data/raw_countries_data.json` or any specified path.

**Transform**

- Flattens nested fields (common and official name, languages, idd, etc.).
- Cleans suffixes and continents.
- Adds `lang_count` and `calling_code`.

**Load**

- Connects to PostgreSQL using environment variables.
- Loads the cleaned DataFrame into a `countries` table.
- Optionally saves a CSV copy.

---

## Project Setup

1. Clone the repo

```bash
https://github.com/mumi-nah/etl-pipeline-with-python.git
cd etl-pipeline-with-python
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Environment Variables: create a .env file and add the following:

```bash
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=database_name
```

4. Run the pipeline

```bash
from src.extract import extract
from src.transform import transform
from src.load import get_engine, load
```

Verify the postgres conection to ensure the data has been loaded

---

### Logging

All pipeline activitiy is logged in pipeline.log

```bash
2026-02-16 22:30: INFO: Data successfully saved to raw_countries_data.json
2026-02-16 22:31: INFO: Data transformed successfully!
2026-02-16 22:32: INFO: Data loaded into Postgres successfully
```

## Resources

[Rest Countries API](https://restcountries.com/v3.1/all)
