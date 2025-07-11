import os
import atexit
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.agents import create_csv_agent

# Directory containing CSV files
CSV_FOLDER = "D:\\Langchain\\Internship_Pune_TCS\\SQL Project (Industry Level Data Implementation)\\Industry-Sub_domain Data"
MERGED_FILE_NAME = "__merged_all_data.csv"
temp_merged_path = os.path.join(CSV_FOLDER, MERGED_FILE_NAME)

# Register cleanup to delete merged file on exit
def cleanup():
    if os.path.exists(temp_merged_path):
        try:
            os.remove(temp_merged_path)
            print(f"Deleted file: {temp_merged_path}")
        except Exception as e:
            print(f"Could not delete {temp_merged_path}: {e}")

atexit.register(cleanup)

def parse_dates_with_multiple_formats(series):
    import dateutil.parser
    parsed_dates = []
    for val in series:
        parsed = None
        for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%Y/%m/%d']:
            try:
                parsed = pd.to_datetime(val, format=fmt, errors='raise')
                break
            except Exception:
                continue
        if parsed is None:
            try:
                parsed = dateutil.parser.parse(val)
            except Exception:
                parsed = pd.NaT
        parsed_dates.append(parsed)
    return pd.Series(parsed_dates)

def analyze_csv_file(file_path):
    df = pd.read_csv(file_path)
    analysis = {}
    analysis['file_name'] = os.path.basename(file_path)
    analysis['num_rows'] = df.shape[0]
    analysis['num_columns'] = df.shape[1]
    analysis['columns'] = list(df.columns)

    # Missing data
    missing_data = df.isnull().sum()
    analysis['missing_data'] = missing_data[missing_data > 0].to_dict()

    # Numeric outliers using IQR
    outliers = {}
    for col in df.select_dtypes(include=[float, int, np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outlier_values = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col].tolist()
        if outlier_values:
            outliers[col] = outlier_values

    # Date outliers (dates far in past or future)
    for col in df.select_dtypes(include=['object']).columns:
        try:
            dates = parse_dates_with_multiple_formats(df[col])
            if dates.notnull().any():
                outlier_dates = dates[(dates < pd.Timestamp('1900-01-01')) | (dates > pd.Timestamp('2100-01-01'))]
                if not outlier_dates.empty:
                    outliers[col] = [str(d) for d in outlier_dates.dt.strftime('%Y-%m-%d')]
        except Exception:
            pass

    analysis['outliers'] = outliers

    # Suspicious categorical values
    suspicious_values = {}
    suspicious_list = ['Unknown', 'unknown', 'XX', 'NULL', 'null', None]
    for col in df.select_dtypes(include=['object']).columns:
        suspicious_vals = df[col][df[col].isin(suspicious_list)].dropna().unique().tolist()
        if suspicious_vals:
            suspicious_values[col] = suspicious_vals
    analysis['suspicious_values'] = suspicious_values

    return analysis

def analyze_all_csv_files(csv_folder):
    results = []
    for filename in os.listdir(csv_folder):
        if filename.lower().endswith('.csv') and filename != MERGED_FILE_NAME:
            file_path = os.path.join(csv_folder, filename)
            try:
                analysis = analyze_csv_file(file_path)
                results.append(analysis)
            except Exception as e:
                results.append({'file_name': filename, 'error': str(e)})
    return results

def print_incorrect_data_summary(analysis_results):
    for result in analysis_results:
        print(f"\nFile: {result.get('file_name')}")
        if 'error' in result:
            print(f"  Error reading file: {result['error']}")
            continue
        print(f"  Number of rows: {result.get('num_rows')}")
        print(f"  Number of columns: {result.get('num_columns')}")
        print(f"  Columns: {result.get('columns')}")
        print(f"  Missing data counts: {result.get('missing_data')}")
        print(f"  Outliers detected: {result.get('outliers')}")
        print(f"  Suspicious categorical values: {result.get('suspicious_values')}")
        print("-" * 60)

def load_and_prepare_csvs(csv_folder):
    csv_files = [f for f in os.listdir(csv_folder)
                 if f.lower().endswith('.csv') and f != MERGED_FILE_NAME]
    dataframes = {}
    for fname in csv_files:
        path = os.path.join(csv_folder, fname)
        try:
            df = pd.read_csv(path)
            # Prefix columns with file name (except for the index)
            prefix = os.path.splitext(fname)[0]
            df = df.add_prefix(f"{prefix}__")
            dataframes[fname] = df
        except Exception as e:
            print(f"Error loading {fname}: {e}")
    return dataframes

def merge_dataframes(dataframes):
    # Concatenate all DataFrames side by side (outer join on index)
    if not dataframes:
        return None
    dfs = list(dataframes.values())
    merged = pd.concat(dfs, axis=1)
    return merged

def main():
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_MISTRAL_SMALL_API_KEY")
    os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

    # Analyze all CSV files (for summary/incorrect data reporting)
    analysis_results = analyze_all_csv_files(CSV_FOLDER)

    # Print incorrect data summary at program start
    print("\nSummary of missing/outlier/suspicious data in all CSV files:")
    print_incorrect_data_summary(analysis_results)

    # Load and merge all CSVs for agent
    dataframes = load_and_prepare_csvs(CSV_FOLDER)
    merged_df = merge_dataframes(dataframes)
    if merged_df is None or merged_df.empty:
        print("No CSV files found or data could not be loaded.")
        return

    # Save merged dataframe to a temp file for the agent
    merged_df.to_csv(temp_merged_path, index=False)

    # Use a powerful free model if desired:
    # model_id = "openrouter/openrouter/quasar-alpha"
    model_id = "mistralai/mistral-small-3.1-24b-instruct:free"

    # Create a single CSV agent over the merged data
    csv_agent = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model=model_id),
        path=temp_merged_path,
        verbose=True,
        allow_dangerous_code=True
    )

    print("\nAll CSVs loaded. You can now ask any question about any or all files!")
    print("Column names are prefixed with their file name, e.g., 'artists_data__Name'.")
    print("Type 'exit' to quit.")

    while True:
        user_q = input("\nAsk a question about the CSV data (or type 'exit' to quit): ").strip()
        if user_q.lower() == "exit":
            print("Exiting...")
            break
        try:
            result = csv_agent.invoke({"input": user_q})
            print("\nAgent answer:\n", result["output"])
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    main()
