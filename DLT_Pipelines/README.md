# DLT Medallion Architecture Pipeline

This pipeline implements an end-to-end **Medallion Architecture** using Databricks Delta Live Tables (DLT), demonstrating a complete data engineering workflow from raw data ingestion to business-ready analytics.

## Architecture Overview

This pipeline follows the **Bronze → Silver → Gold** medallion architecture pattern:

### 🥉 Bronze Layer (`transformations/bronze/`)
**Purpose**: Raw data ingestion with initial data quality checks

- **`customers_ingest.py`**: Ingests customer data from source with validation rules
  - Validates: `customer_id` and `customer_name` are not null
  - Creates: `customers_stg` table

- **`products_ingest.py`**: Ingests product data from source with validation rules
  - Validates: `product_id` is not null and `price >= 0`
  - Creates: `products_stg` table

- **`sales_ingest.py`**: Ingests sales data from multiple sources (east and west regions)
  - Validates: `sales_id` is not null
  - Uses `append_flow` to merge data from multiple source streams
  - Creates: `sales_stg` table

### 🥈 Silver Layer (`transformations/silver/`)
**Purpose**: Cleaned, enriched, and standardized data with Change Data Capture (CDC)

- **`customers_transform.py`**: Transforms customer data
  - Enrichment: Converts customer names to uppercase
  - CDC: Uses SCD Type 1 (overwrites) with `customer_id` as key
  - Creates: `customers_enr` table

- **`products_transform.py`**: Transforms product data
  - Enrichment: Casts price to integer
  - CDC: Uses SCD Type 1 (overwrites) with `product_id` as key
  - Creates: `products_enr` table

- **`sales_transform.py`**: Transforms sales data
  - Enrichment: Calculates `total_amount = quantity * amount`
  - CDC: Uses SCD Type 1 (overwrites) with `sales_id` as key
  - Creates: `sales_enr` table

### 🥇 Gold Layer (`transformations/gold/`)
**Purpose**: Business-level aggregated data in a star schema design

**Dimension Tables** (SCD Type 2 - tracks historical changes):
- **`dim_customers.py`**: Customer dimension table with full history tracking
- **`dim_products.py`**: Product dimension table with full history tracking

**Fact Tables**:
- **`fact_sales.py`**: Sales fact table (SCD Type 1) containing transactional sales data

**Aggregated Business Metrics**:
- **`business_sales.py`**: Aggregated sales report by region and category
  - Joins fact and dimension tables
  - Calculates total sales grouped by region and category

## Data Flow

```
Source Systems
    ↓
Bronze Layer (Raw Ingestion + Quality Checks)
    ↓
Silver Layer (Cleaned & Enriched + CDC)
    ↓
Gold Layer (Business Metrics + Star Schema)
    ↓
Business Analytics
```

## Key Features

- **Data Quality**: Expectation rules at the Bronze layer to catch data issues early
- **Change Data Capture (CDC)**: Automatic handling of updates and deletes using `create_auto_cdc_flow`
- **SCD Types**: 
  - Type 1 (overwrite) for Silver layer and fact tables
  - Type 2 (history tracking) for dimension tables
- **Streaming Processing**: All tables use streaming for real-time data processing
- **Multi-Source Ingestion**: Sales data combines multiple source streams (east/west)

## Project Structure

```
DLT_Pipelines/
├── transformations/
│   ├── bronze/          # Raw data ingestion
│   ├── silver/           # Cleaned and enriched data
│   ├── gold/             # Business-ready analytics
│   └── demo/              # Example/demo transformations
├── utilities/             # Utility functions (e.g., email validation)
└── explorations/          # Ad-hoc notebooks for data exploration
```

## Getting Started

### Running the Pipeline

1. **Run a single transformation**: Use `Run file` to execute and preview a single transformation
2. **Run entire pipeline**: Use `Run pipeline` to execute all transformations in the correct dependency order
3. **Schedule the pipeline**: Use `Schedule` to run the pipeline automatically on a schedule

### Development

- Each dataset is defined in a separate file under `transformations`
- Read more about DLT syntax at https://docs.databricks.com/ldp/developer/python-ref
- Use `+ Add` in the file browser to add new dataset definitions
- Explore the demo files in `transformations/demo/` for additional examples

### Data Exploration

- Use notebooks in the `explorations/` folder to analyze pipeline outputs
- These notebooks are not executed as part of the pipeline
- Make sure to run the pipeline first to materialize the datasets

## Documentation

For more tutorials and reference material, see:
- [Databricks Delta Live Tables Documentation](https://docs.databricks.com/ldp)
- [DLT Python Reference](https://docs.databricks.com/ldp/developer/python-ref)