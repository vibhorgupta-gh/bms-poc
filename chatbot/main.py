from flask import Flask, request
from flask_cors import CORS
from rasa.utils.endpoints import EndpointConfig
from rasa.core.agent import Agent
import asyncio
import os
from typing import Dict, Text, Any, List, Union, Optional

app = Flask(__name__)
app.secret_key = ''
CORS(app)

global agent
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load("./models", action_endpoint=action_endpoint)


@app.route('/', methods=['POST'])
def webhook():
    global agent
    print(request.json)
    userMsg = request.json['Msg']
    if agent.is_ready():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(parse(userMsg))

    if response is not None:
        if type(response) is list:
            return response[0].get('text')
        else:
            return response
    else:
        return 'The response was not valid'


async def parse(text: Text):
    global agent
    response = await agent.handle_text(text)
    return response


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='192.168.43.13')
