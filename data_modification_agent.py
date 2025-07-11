import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_csv_agent

# Load environment variables (for API key)
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_MISTRAL_SMALL_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

CSV_DIR = r"D:\LangChain\Internship_Pune_TCS\Industry Level Data Handling\Industry-Sub_domain Data"

def list_csv_files(directory):
    return [f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith('.csv')]

def process_instruction_file(instruction_file):
    try:
        with open(instruction_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Could not read file '{instruction_file}': {e}")
        return

    if not lines:
        print("Instruction file is empty.")
        return

    files = set(list_csv_files(CSV_DIR))
    llm = ChatOpenAI(model="mistralai/mistral-small-3.1-24b-instruct:free", temperature=0)
    agents = {}

    for idx, line in enumerate(lines, 1):
        if ':' not in line:
            print(f"Line {idx} skipped (missing colon): {line}")
            continue
        filename, instruction = line.split(':', 1)
        filename = filename.strip()
        instruction = instruction.strip()
        if filename not in files:
            print(f"Line {idx} skipped (CSV file '{filename}' not found): {line}")
            continue

        file_path = os.path.join(CSV_DIR, filename)
        if filename not in agents:
            agents[filename] = create_csv_agent(
                llm, file_path, verbose=True, allow_dangerous_code=True
            )
        agent_executor = agents[filename]

        print(f"\nInstruction {idx} for '{filename}': {instruction}")
        response = agent_executor.invoke({"input": instruction})
        print("Agent:", response.get("output"))

        tool = agent_executor.tools[0]
        try:
            if hasattr(tool, "df"):
                df = tool.df
                df.to_csv(file_path, index=False)
                print(f"Changes saved to '{filename}'.")
            elif hasattr(tool, "locals") and "df" in tool.locals:
                df = tool.locals["df"]
                df.to_csv(file_path, index=False)
                print(f"Changes saved to '{filename}'.")
            elif hasattr(tool, "_locals") and "df" in tool._locals:
                df = tool._locals["df"]
                df.to_csv(file_path, index=False)
                print(f"Changes saved to '{filename}'.")
            else:
                print("No DataFrame found to save.")
        except Exception as e:
            print(f"Warning: Could not save changes to '{filename}': {e}")
        print("-" * 50)

def interactive_mode():
    llm = ChatOpenAI(model="mistralai/mistral-small-3.1-24b-instruct:free", temperature=0)
    while True:
        files = list_csv_files(CSV_DIR)
        if not files:
            print("No CSV files found.")
            return

        print("\nAvailable CSV files:")
        for fname in files:
            print(f"- {fname}")

        selected = input("Enter the exact name of the file to work on (or type 'exit' to quit, or 'mode' to switch mode): ").strip()
        if selected.lower() == "exit":
            return
        if selected.lower() == "mode":
            break
        if selected not in files:
            print("File not found. Please enter the exact file name as shown above.")
            continue

        file_path = os.path.join(CSV_DIR, selected)
        agent_executor = create_csv_agent(
            llm, file_path, verbose=True, allow_dangerous_code=True
        )

        while True:
            user_input = input(f"\nEnter instruction for '{selected}' (or type 'change' to pick another file, 'exit' to quit, or 'mode' to switch mode):\n")
            if user_input.lower() == "exit":
                return
            if user_input.lower() == "change":
                break
            if user_input.lower() == "mode":
                return

            response = agent_executor.invoke({"input": user_input})
            print("Agent:", response.get("output"))

            tool = agent_executor.tools[0]
            try:
                if hasattr(tool, "df"):
                    df = tool.df
                    df.to_csv(file_path, index=False)
                    print(f"Changes saved to '{selected}'.")
                elif hasattr(tool, "locals") and "df" in tool.locals:
                    df = tool.locals["df"]
                    df.to_csv(file_path, index=False)
                    print(f"Changes saved to '{selected}'.")
                elif hasattr(tool, "_locals") and "df" in tool._locals:
                    df = tool._locals["df"]
                    df.to_csv(file_path, index=False)
                    print(f"Changes saved to '{selected}'.")
                else:
                    print("No DataFrame found to save.")
            except Exception as e:
                print(f"Warning: Could not save changes to '{selected}': {e}")

def main():
    while True:
        print("\nChoose mode:")
        print("1. Instruction file mode (batch process instructions from a text file)")
        print("2. Interactive mode (enter instructions one by one for a selected CSV)")
        print("Type 'exit' to quit.")
        mode = input("Enter 1 or 2 (or 'exit'): ").strip()
        if mode == "exit":
            break
        elif mode == "1":
            instruction_file = input("Enter the name of the instruction file: ").strip()
            if not os.path.isfile(instruction_file):
                print("Instruction file not found. Please enter a valid filename.")
                continue
            process_instruction_file(instruction_file)
        elif mode == "2":
            interactive_mode()
        else:
            print("Invalid input. Please enter 1, 2, or 'exit'.")

if __name__ == "__main__":
    main()
