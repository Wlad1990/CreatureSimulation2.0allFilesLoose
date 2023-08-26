import openai
import random
from interaction import Fight, Trade, Cooperate


class Behavior:
    def __init__(self, creature, api_key):
        self.creature = creature
        openai.api_key = api_key

    def decide(self, world):
        prompt = self.creature.generate_prompt(world)

        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=prompt,
          temperature=0.5,
          max_tokens=100
        )

        actions = self.parse_response(response.choices[0].text.strip())
        return actions

    def parse_response(self, response):
        # Here we're assuming that the responses from OpenAI are in the form "action_type:target:details"
        actions = [action.split(':') for action in response.split(', ')]
        
        # Return the list of actions
        return actions

    def execute_action(self, actions):
        for action in actions:
            self.creature.execute_action(action)
