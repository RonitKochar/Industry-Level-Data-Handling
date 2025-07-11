import os
import pandas as pd
import re
import ast
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_MOONSHOT_KIMI_DEV_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# Directory containing CSV files
CSV_DIR = r"D:\LangChain\Internship_Pune_TCS\Industry Level Data Handling\Industry-Sub_domain Data"

def list_csv_files(directory):
    return [f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith('.csv')]

def get_file_summaries(files):
    summaries = []
    for file in files:
        path = os.path.join(CSV_DIR, file)
        try:
            df = pd.read_csv(path, nrows=3)  # Read first 3 rows for a sample
            summary = f"File: {file}\nColumns: {', '.join(df.columns)}\nSample:\n{df.head(1).to_dict(orient='records')[0]}"
        except Exception as e:
            summary = f"File: {file}\nCould not read file: {e}"
        summaries.append(summary)
    return summaries

def extract_list_from_response(response):
    # Find the first [...] block in the response
    match = re.search(r"\[.*?\]", response, re.DOTALL)
    if match:
        try:
            return ast.literal_eval(match.group(0))
        except Exception:
            return None
    return None

def main():
    files = list_csv_files(CSV_DIR)
    if not files:
        print("No CSV files found.")
        return

    print(f"Found {len(files)} CSV files:")
    for f in files:
        print(" -", f)

    n_keep = int(input("How many important files do you want to keep? "))

    summaries = get_file_summaries(files)
    summaries_text = "\n\n".join(summaries)

    # Construct the prompt for the LLM
    prompt = (
        f"You are a data analyst. Here are summaries of CSV files:\n\n"
        f"{summaries_text}\n\n"
        f"From the above, select the {n_keep} most important files to keep (based on file names and file data)."
        f"!IMPORTANT: The important files are the ones that contain sales, order and customer information or details about the product or industry-sub_domain."
        f"Make sure all the important files are kept in the directory"
        f"Return only the file names as a Python list, with no explanation or formatting, and do not include markdown or code blocks."
        f"For example: ['file1.csv', 'file2.csv']"
    )

    # Use LangChain OpenAI agent (replace model name as needed)
    llm = ChatOpenAI(model="moonshotai/kimi-dev-72b:free", temperature=0)
    response = llm.invoke(prompt)
    response_text = str(response)
    
    print("\nLLM response:", response_text)

    keep_files = extract_list_from_response(response_text)
    if not keep_files or not isinstance(keep_files, list):
        print("Could not parse LLM response. Please check the output.")
        return

    # Remove files not in the keep list
    remove_files = [f for f in files if f not in keep_files]
    for f in remove_files:
        os.remove(os.path.join(CSV_DIR, f))
        print(f"Removed: {f}")

    print("\nKept files:")
    for f in keep_files:
        print(f" - {f}")

if __name__ == "__main__":
    main()
