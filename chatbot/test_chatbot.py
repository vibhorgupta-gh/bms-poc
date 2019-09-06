import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
from rasa.utils.endpoints import EndpointConfig
from rasa.core.agent import Agent
from typing import Text
import asyncio

action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load("./models", action_endpoint=action_endpoint)


async def parse(text: Text):
    global agent
    response = await agent.handle_text(text)
    return response


def test_ok_response(input_message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(parse(input_message))[0]['text']
    assert str(type(response)) == "<class 'str'>"


def test_bad_respone(input_message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(parse(input_message))[0]['text']
    assert str(type(response)) == "<class 'str'>"


