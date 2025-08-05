from utils.helpers import print_welcome
from agents.gemini_agent import AgenticModel

def main():
    print_welcome()
    agent = AgenticModel()
    print("Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break
        response = agent.run(user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()