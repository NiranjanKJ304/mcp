import asyncio

from backend.agent import Agent


async def main():

    agent = Agent()

    while True:

        question = input("\nYou : ")

        if question.lower() == "exit":
            break

        answer = await agent.ask(question)

        print("\nAssistant:")
        print(answer)

asyncio.run(main())
