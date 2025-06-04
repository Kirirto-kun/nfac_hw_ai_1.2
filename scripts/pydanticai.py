from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result_sync = agent.run_sync('what is PydanticAI?')
print(result_sync.output)
#> Rome


async def main():
    result = await agent.run('What is the capital of France?')
    print(result.output)
    #> Paris

    async with agent.run_stream('What is the capital of the UK?') as response:
        print(await response.get_output())
        #> London