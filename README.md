# Telecom Data Processing & Formatting Pipeline

A production-ready Python data processing solution that transforms raw telecom sector CSV data into standardized, professionally formatted Excel workbooks. This project demonstrates data manipulation, aggregation, and automated reporting capabilities.

## 📋 Project Overview

This project showcases a simple ETL (Extract, Transform, Load) pipeline designed to handle complex telecom infrastructure data. The solution processes multi-company datasets with varying structures, consolidates them into a unified format, and generates professionally styled analytical reports.

### Key Capabilities

- **Data Aggregation & Grouping**: Intelligently combines related records based on unique identifiers
- **Automated calculations**: Aggregates bandwidth allocations across multiple technology types
- **Automated Transformation**: Systematic column renaming, ordering, and derived field generation
- **Advanced Excel Formatting**: Programmatic styling including custom colors, fonts, and multi-sheet workbooks
- **Production-Ready Code**: Reusable functions, error handling, and comprehensive documentation

## 🎯 What This Project Demonstrates

### Data Science & Engineering Skills
- **ETL Pipeline Design**: End-to-end data processing workflow
- **Data Transformation**: Complex data reshaping and aggregation logic
- **Pandas Mastery**: Advanced groupby operations, multi-column transformations, and data validation
- **Office Automation**: OpenpyXL integration for professional Excel output
- **Code Organization**: Modular, reusable functions with clear separation of concerns

### Documentation & Communication
- **Jupyter Notebooks**: Interactive documentation combining code, explanations, and visualizations
- **Code Comments**: Clear inline documentation of logic and business rules
- **README Excellence**: Comprehensive project documentation for different audiences
- **Example-Driven**: Before/after examples showcasing data transformations

### Software Development Practices
- **DRY Principle**: Generic, reusable function design that works with any company dataset
- **Error Handling**: Robust file existence checks and workbook management
- **Flexibility**: Parameterized function calls for easy adaptation to new data sources
- **Scalability**: Can easily extend to handle additional companies or data fields

## 🏗️ Project Structure

```
telecom-data-pipeline/
├── README.md                              # Comprehensive project documentation
├── requirements.txt                       # Python dependencies
├── data_processor.py                      # Main processing module
├── notebooks/
│   └── data_processing_guide.ipynb       # Interactive documentation & examples
├── data/
│   ├── input/
│   │   ├── company_a_sectors.csv         # Sample raw data files
│   │   ├── company_b_sectors.csv
│   │   └── company_c_sectors.csv
│   └── output/
│       └── processed_telecom_data.xlsx   # Generated output
└── examples/
    └── sample_transformations.md         # Visual transformation examples
```

## 🔄 Data Processing Workflow

### Pipeline Overview

```
Raw CSV Data
    ↓
[Read & Validate]
    ↓
[Group by Record ID]
    ↓
[Aggregate by Technology]
    ↓
[Transform & Enrich]
    ↓
[Standardize Format]
    ↓
[Style & Export to Excel]
    ↓
Formatted Excel Workbook
```

### Input Data Structure

The pipeline expects CSV files with the following fields:

| Field | Type | Purpose |
|-------|------|---------|
| `Tier-4 id` | String | Unique tower identifier |
| `record_id` | String | Grouping key (towers may have multiple records) |
| `latitude` | Float | Geographic location (North-South) |
| `longitude` | Float | Geographic location (East-West) |
| `structure_height` | Float | Tower height in meters |
| `licence_category*` | String | Service type / license category |
| `technology` | String | Technology type (LTE, 5G, etc.) |
| `bandwidth` | Float | Bandwidth allocation in MHz |
| `tx_power` | Float | Transmission power in watts |
| `tx_ant_azimuth` | Float | Antenna azimuth angle in degrees |

### Key Transformation Logic

**1. Grouping Strategy**
- Groups multiple CSV rows by `record_id` (tower identifier)
- Handles cases where a single tower has multiple technology deployments
- Preserves unique attributes (coordinates, height) while aggregating repeated fields

**2. Bandwidth Aggregation**
```python
4G_BW = Sum of bandwidth where technology == 'LTE'
5G_BW = Sum of bandwidth where technology == '5G'
```

**3. Tower Classification**
```python
Type = 'Micro' if Height < 10 meters else 'Macro'
```

**4. Field Consolidation**
- Repeated values (services, technologies) joined with pipe separator (|)
- Example: A tower with multiple services shows as `Cellular|Fixed|PCS`

### Output Data Structure

| Column | Source | Description |
|--------|--------|-------------|
| `Code` | Tier-4 id | Tower identifier |
| `Name` | Generated | Tower name (user-provided) |
| `Province` | Parameter | Geographic province |
| `Tower ID` | record_id | Primary grouping key |
| `Licensee` | Parameter | Company/licensee name |
| `LATITUDE` | latitude | Geographic coordinate |
| `LONGITUDE` | longitude | Geographic coordinate |
| `Height (m)` | structure_height | Tower height |
| `Type` | Derived | Classification (Micro/Macro) |
| `Micro` | Derived | Micro tower indicator |
| `Macro` | Derived | Macro tower indicator |
| `TX_ANT_AZI` | tx_ant_azimuth | Antenna azimuth |
| `SERVICES` | licence_category* | Aggregated services |
| `TECHNOLOGY` | technology | Aggregated technologies |
| `TR_BW_BLOCS` | bandwidth | Concatenated bandwidth values |
| `4G_BW` | Calculated | Total 4G bandwidth (MHz) |
| `5G_BW` | Calculated | Total 5G bandwidth (MHz) |
| `TX_PWR` | tx_power | Transmission power |

## 💻 Core Function: `process_company_data()`

```python
def process_company_data(input_csv, company_name, licensee_name, 
                        province, sheet_name, workbook_name):
    """
    Process a company's CSV data and add formatted worksheet to Excel workbook.
    
    Parameters:
    -----------
    input_csv : str
        Path to input CSV file
    company_name : str
        Display name for logging
    licensee_name : str
        Official company/licensee name for output
    province : str
        Province code (e.g., 'QC', 'ON')
    sheet_name : str
        Name for Excel worksheet
    workbook_name : str
        Path to output Excel file (creates if doesn't exist)
    
    Returns:
    --------
    pd.DataFrame
        Processed and formatted dataframe
    """
```

### Function Features
- ✅ Automatic workbook creation if file doesn't exist
- ✅ Seamless addition to existing workbooks
- ✅ Professional header styling (dark blue background, white bold text)
- ✅ Comprehensive feedback with progress logging
- ✅ Returns processed DataFrame for further analysis

## 📊 Usage Examples

### Basic Usage

```python
from data_processor import process_company_data

# Process a single company
process_company_data(
    input_csv="company_a_data.csv",
    company_name="Company A",
    licensee_name="Company A Inc.",
    province="QC",
    sheet_name="CompanyA",
    workbook_name="output.xlsx"
)
```

### Batch Processing Multiple Companies

```python
companies = [
    {
        "input_csv": "company_a_data.csv",
        "company_name": "Company A",
        "licensee_name": "Company A Inc.",
        "province": "QC",
        "sheet_name": "CompanyA"
    },
    {
        "input_csv": "company_b_data.csv",
        "company_name": "Company B",
        "licensee_name": "Company B Corp.",
        "province": "ON",
        "sheet_name": "CompanyB"
    }
]

output_file = "telecom_data_consolidated.xlsx"

for company in companies:
    process_company_data(
        **company,
        workbook_name=output_file
    )

print(f"✅ Consolidated report: {output_file}")
```

### Using the Jupyter Notebook

The included Jupyter notebook provides an interactive walkthrough:

```bash
jupyter notebook notebooks/data_processing_guide.ipynb
```

Features:
- Step-by-step explanations with Markdown cells
- Function definitions with detailed docstrings
- Before/after data examples
- Visual output previews
- Reproducible workflows

## 📈 Before & After Examples

### Input Data (Raw CSV)

| record_id | Tier-4 id | latitude | longitude | height | technology | bandwidth | licence_category |
|-----------|-----------|----------|-----------|--------|------------|-----------|------------------|
| T-001 | A-001 | 45.50 | -73.57 | 25 | LTE | 20 | Cellular |
| T-001 | A-001 | 45.50 | -73.57 | 25 | LTE | 30 | Cellular |
| T-001 | A-001 | 45.50 | -73.57 | 25 | 5G | 100 | Cellular |
| T-002 | A-002 | 45.51 | -73.58 | 8 | LTE | 15 | Cellular |
| T-003 | A-003 | 45.52 | -73.59 | 35 | LTE | 25 | Fixed |

**Observations:**
- Tower T-001 has 3 rows (2x LTE, 1x 5G)
- Towers have duplicate structure data
- Technologies and bandwidths repeat per tower
- Data needs aggregation and standardization

### Output Data (Formatted Excel)

| Code | Tower ID | Licensee | Height | Type | Micro | Macro | TECHNOLOGY | 4G_BW | 5G_BW |
|------|----------|----------|--------|------|-------|-------|------------|-------|-------|
| A-001 | T-001 | Company A | 25 | Macro | - | 1 | 4G\|5G | 50 | 100 |
| A-002 | T-002 | Company A | 8 | Micro | 1 | - | 4G | 15 | 0 |
| A-003 | T-003 | Company A | 35 | Macro | - | 1 | 4G | 25 | 0 |

**Transformations Applied:**
- ✅ Grouped T-001's 3 rows into 1 consolidated row
- ✅ Summed 4G bandwidth: 20+30=50 MHz
- ✅ Aggregated 5G bandwidth: 100 MHz
- ✅ Classified as Micro (height<10) or Macro (height≥10)
- ✅ Technology normalized: LTE → 4G
- ✅ Removed duplicate structural data

## 🛠️ Installation & Setup

### Requirements
- Python 3.7+
- pandas >= 1.1.0
- openpyxl >= 3.0.0

### Installation

```bash
# Clone repository
git clone <repository-url>
cd telecom-data-pipeline

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### requirements.txt
```
pandas>=1.1.0
openpyxl>=3.0.0
jupyter>=1.0.0
ipython>=7.0.0
```

## 🎨 Output Formatting

The generated Excel workbooks include professional styling:

- **Header Rows**: Dark blue background (#002060) with white bold text
- **Multiple Sheets**: One worksheet per company for easy navigation
- **Proper Column Widths**: Optimized for readability
- **Data Types**: Numeric columns formatted appropriately
- **Preserves Structure**: Maintains data integrity for downstream analysis

## 🔍 Data Quality Considerations

### Validation Performed
- ✅ File existence checks
- ✅ Column presence verification
- ✅ Data type conversions
- ✅ Bandwidth aggregation logic

### Assumptions
- `record_id` is unique per tower
- Unique columns don't vary within a record_id group
- Bandwidth values are numeric
- Technology field uses consistent naming

### Notably, the following was intentionally ommited from this code:
- [ ] Add comprehensive error logging
- [ ] Implement data validation rules with reporting
- [ ] Add unit tests for transformation logic
- [ ] Create data quality dashboards
- [ ] Add support for partial data updates

## 📝 Code Quality Highlights

### Design Principles Applied
1. **DRY (Don't Repeat Yourself)**: Generic function handles all companies
2. **Single Responsibility**: Each code section has one purpose
3. **Parameterization**: Easy to adapt for new data sources
4. **Documentation**: Comprehensive docstrings and comments
5. **Separation of Concerns**: Data processing, transformation, and export are distinct

### Best Practices Demonstrated
- Clear variable naming conventions
- Logical code organization with sections
- Comprehensive function documentation
- Error handling for file operations
- Use of pandas best practices for performance
- Professional logging and user feedback

## 📚 Learning Resources

This project demonstrates:
- **Pandas**: groupby, aggregation, data transformation, pivot operations
- **OpenpyXL**: Excel file creation, styling, multi-sheet management
- **Python**: Functions, loops, conditional logic, file I/O
- **Data Engineering**: ETL patterns, data validation, batch processing
- **Documentation**: Comprehensive README, docstrings, inline comments


## 👤 Author

Navit Dori
