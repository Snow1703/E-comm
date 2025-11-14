# E-commerce Analytics Dashboard

A comprehensive e-commerce analytics dashboard with synthetic data generation, SQLite database, and a modern Flask web interface.

## Features

- **Synthetic Data Generation**: Generate realistic e-commerce data (users, products, orders, payments, events)
- **SQL Analytics**: Advanced SQL queries for RFM analysis, sustainability metrics, and cohort analysis
- **Web Dashboard**: Beautiful, responsive web interface displaying real-time analytics
- **Network Accessible**: Access the dashboard from any device on your local network

## Project Structure

```
E-commerce-main/
├── data/              # CSV data files
├── templates/         # HTML templates
├── app.py             # Flask web application
├── generate_data.py   # Data generation script
├── ingest.py          # Database ingestion script
├── analytics.sql      # Advanced SQL queries
├── query.sql          # Basic SQL queries
├── ecom.db            # SQLite database (generated)
└── README.md          # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install pandas faker flask
```

### 2. Generate Data

```bash
python generate_data.py
```

This will create CSV files in the `data/` directory.

### 3. Ingest Data into Database

```bash
python ingest.py
```

This creates `ecom.db` SQLite database and loads all CSV data.

### 4. Run the Web Dashboard

```bash
python app.py
```

The server will start on port 8080. Access it at:
- **Local**: http://localhost:8080
- **Network**: http://YOUR_IP:8080 (check the terminal output for your IP)

## Analytics Features

### 1. User Spending Analysis
Shows total spending per user with the number of distinct brands they've purchased from.

### 2. RFM Customer Analysis
- **Recency**: Days since last order
- **Frequency**: Number of orders
- **Monetary**: Total amount spent

### 3. Sustainability Revenue
Percentage of revenue from high-sustainability products (sustainability_score ≥ 0.7).

### 4. Cohort Analysis
Monthly user cohorts and their purchasing behavior over time.

## API Endpoints

- `GET /` - Main dashboard page
- `GET /api/stats` - Overall statistics (users, orders, revenue, products)
- `GET /api/user-spending` - User spending with distinct brands
- `GET /api/rfm-analysis` - RFM customer analysis
- `GET /api/sustainability` - Sustainability revenue metrics
- `GET /api/cohort` - Cohort analysis data

## Technologies Used

- **Python 3**
- **Flask** - Web framework
- **SQLite** - Database
- **Pandas** - Data manipulation
- **Faker** - Synthetic data generation
- **HTML/CSS/JavaScript** - Frontend

## Data Schema

- **users**: User information with behavioral fields
- **products**: Product catalog with sustainability scores
- **orders**: Order transactions
- **order_items**: Individual items in orders
- **payments**: Payment information
- **events**: User events for funnel analysis

## License

This project is open source and available for educational purposes.
