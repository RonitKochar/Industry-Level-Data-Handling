import os
import csv
import re
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# Set your desired output folder here
CSV_FOLDER = r"D:\LangChain\Internship_Pune_TCS\Industry Level Data Handling\Industry-Sub_domain Data"  # <--- Change this to your desired folder path

def generate_sales_sql(question: str, csv_folder: str) -> str:
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    load_dotenv()
    os.environ["OPENAI_API_KEY"]  = os.getenv("OPENROUTER_MISTRAL_SMALL_API_KEY")
    os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

    template = """
    You are an expert SQL database designer and data generator.

    Based on the user's input, generate:
    1. At least 15 well-structured CREATE TABLE statements.
    2. At least 15 INSERT INTO statements per table (≥15 rows per table).
    3. All values must look realistic and relevant to the user's industry and sub-domain.
    
    Strict formatting rules:
    - DO NOT use markdown formatting (no triple backticks).
    - DO NOT include explanations or prefaces like “Here is”.
    - ONLY return the SQL, starting at Final Answer.

    Use this ReAct format:

    Question: {input}
    Thought: I understand the industry and sub-domain context.
    Action: None
    Action Input: None
    Observation: None
    Thought: Now I will generate the SQL code.
    Final Answer:
    <Only raw SQL here>
    
    Available tools: {tool_names}
    {tools}
    {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template)

    llm = ChatOpenAI(
        model="mistralai/mistral-small-3.1-24b-instruct:free",
        temperature=0,
    )

    agent = create_react_agent(llm=llm, prompt=prompt, tools=[])
    executor = AgentExecutor(agent=agent, tools=[], verbose=True, handle_parsing_errors=True, 
                             max_iterations=5)
    
    result = executor.invoke({"input": question})
    output = result["output"]

    output = output.replace("``````", "").strip()
    save_insert_statements_to_csv(output, csv_folder)

    return output

def save_insert_statements_to_csv(sql_text: str, csv_folder: str):
    insert_pattern = re.compile(
        r"INSERT INTO\s+(\w+)\s*\(([^)]+)\)\s*VALUES\s*((?:\([^;]+?\))(?:\s*,\s*\([^;]+?\))*)\s*;",
        re.IGNORECASE | re.DOTALL
    )

    # Ensure the folder exists
    os.makedirs(csv_folder, exist_ok=True)

    matches = insert_pattern.finditer(sql_text)
    found_any = False

    for match in matches:
        found_any = True
        table_name = match.group(1)
        columns = [col.strip() for col in match.group(2).split(",")]
        values_block = match.group(3).replace('\n', ' ')

        value_rows = re.findall(r"\(([^)]+)\)", values_block)
        rows = []
        for value_str in value_rows:
            values = [v.strip().strip("'").strip('"') for v in re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", value_str)]
            rows.append(values)

        filename = os.path.join(csv_folder, f"{table_name.lower()}_data.csv")
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)
        print(f"Saved {len(rows)} rows to '{filename}'")

    if not found_any:
        print("⚠️ No INSERT INTO statements found in the SQL output.")

if __name__ == "__main__":
    print("\n Welcome to the Industry-Specific SQL Data Generator\n")
    while True:
        industry = input("Enter industry (e.g., film, music, toys): ").strip()
        if not industry:
            print("Industry cannot be empty.")
            continue

        subdomain = input("Enter sub-domain (e.g., revenue, retail, shop_locations): ").strip()
        if not subdomain:
            print("Sub-domain cannot be empty.")
            continue

        user_question = f"Generate a realistic SQL database for the '{industry}' industry focusing on the '{subdomain}' sub-domain. Include at least 15 tables and 15 rows per table."

        print("\n Generating SQL data...\n")
        sql_result = generate_sales_sql(user_question, CSV_FOLDER)
        print("\n SQL Generation Complete. Output:")
        print(sql_result)
        print("-" * 60)

        again = input("\n Do you want to generate another one? (y/n): ").strip().lower()
        if again != "y":
            print("Exiting...")
            break
