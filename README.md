Detailed Explanation of Each Agent
1. Data Generation Agent
Purpose:
Generates realistic, industry-specific SQL database schemas and data samples based on user input.

Key Features:

Interactive: Prompts for industry and sub-domain.

Uses a large language model (LLM) to create SQL code.

Produces at least 15 tables with 15 rows each.

Exports each table’s data to separate CSV files.

Use Case:
Quickly prototype databases and generate mock data for analytics, testing, or education.

2. Data Generation Agent With Errors
Purpose:
Similar to the standard Data Generation Agent, but intentionally includes realistic data errors and outliers.

Key Features:

Generates at least 5 tables with 5 rows each.

Ensures each table contains:

Outlier values (e.g., extreme numbers, typos, odd dates).

NULLs in nullable columns.

Exports data to both CSV and a consolidated SQL file.

Use Case:
Create datasets that mimic real-world imperfections for robust testing of data pipelines and error handling.

3. Data Error Recognition Agent
Purpose:
Audits and analyzes CSV files for data quality issues.

Key Features:

Scans all CSVs in a directory.

Detects:

Missing values.

Numeric and date outliers.

Suspicious categorical values (e.g., "Unknown", "NULL").

Merges data for unified analysis.

Allows interactive querying via a conversational agent.

Use Case:
Identify and summarize data quality problems before further analysis or processing.

4. Data Modification Agent
Purpose:
Enables interactive and batch editing of CSV files using natural language instructions.

Key Features:

Two modes:

Batch: Processes a list of instructions from a file.

Interactive: User selects a file and issues commands one by one.

Uses an LLM to interpret and execute commands (e.g., filter, update, aggregate).

Saves changes directly to the CSV files.

Use Case:
Streamline data cleaning, transformation, and exploration without manual coding.

5. File Reduction Agent
Purpose:
Curates a directory by retaining only the most relevant CSV files based on content and business criteria.

Key Features:

Summarizes each file (columns, sample data).

Uses an LLM to select the most important files (e.g., those with sales, orders, customers).

Deletes all other files from the directory.

Use Case:
Reduce data clutter and focus analysis on key datasets, improving efficiency and relevance.

Each agent plays a distinct role in the data workflow, from generation and error simulation to quality auditing, modification, and curation—enabling robust, efficient, and user-friendly data management.