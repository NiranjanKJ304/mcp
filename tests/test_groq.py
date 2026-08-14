from backend.llm import GroqLLM

llm = GroqLLM()

print("Groq Chat Started")
print("Type 'exit' to quit.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    response = llm.chat(messages)

    print("\nAssistant:")
    print(response.choices[0].message.content)
    print("-" * 50)