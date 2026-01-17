# Personal Finance Analytics

This is a Python-based personal finance analytics application focused on salary and expense analysis for the Argentinian economy. The project combines data analysis, web API, and visualization capabilities.

## Project Structure & Architecture

### Technology Stack:

- **Backend**: FastAPI (REST API)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Machine Learning**: Scikit-learn
- **Environment**: Python 3.11+
- **Package Management**: Pipenv + pip-tools

## Architecture Pattern: Clean Architecture with layered design:

- **API Layer**: FastAPI routes with authentication
- **Domain Layer**: Business logic (FinanceAnalyst, entities)
- **Infrastructure Layer**: Data access (Google Sheets integration)
- **Utils**: Settings, exceptions, configurations

## Core Functionality

### 1. Salary Analytics (/salary-analytics/{password})

- Personal salary tracking with inflation adjustments
- IT industry salary percentiles (using SysArmy survey data)
- Salary variance analysis (3m, 6m, 1y comparisons)
- Junior-to-Senior salary deltas
- Personal salary progression vs. inflation

### 2. Available Funds Analysis (/available-funds/{password})

- Monthly expense tracking by categories
 Budget allocation limits per category (e.g., rent: 30%, transport: 5%)
- Available funds calculation
- Daily spending limits for remaining month

### 3. Data Sources

- **Personal Salaries**: Google Sheets (monthly salary data with inflation rates)
- **Expenses**: Google Sheets (categorized monthly expenses)
- **IT Salaries**: SysArmy survey CSV files (Argentinian tech salaries)

## Key Components

### Domain Entities:

- SalaryAnalytics: Net salary, adjusted salary, percentiles, deltas
- AvailableFunds: Category budgets, balances, daily limits

### Business Logic (FinanceAnalyst):

- salary_analysis(): Computes personal salary metrics vs. IT market
month_expenses_analysis(): Calculates available funds per category

### Data Processing:

- Inflation-adjusted salary calculations
- Category-based expense budgeting
- IT salary percentile ranking
- Monthly expense projections

### API Features:

- Password-protected endpoints
- JSON responses with formatted currency strings
- Comprehensive error handling
- Health check endpoint

### Data Analysis Notebooks

The project includes Jupyter notebooks for:

- Salary trend analysis
- Expense pattern visualization
- IT salary comparisons
- Inflation impact studies

### Configuration

- Environment variables for Google Sheets IDs
- API password authentication
- Spreadsheet URLs for dynamic data loading

### Testing

- Unit tests for API routes
- Domain logic testing
- FastAPI TestClient integration
