#!/usr/bin/env python3

import asyncio
import json
import os
import websockets

from game import Game
from game_state import GameState


async def play():
    """
    The main loop of the game. It creates a connection to the server,
    receives the state of the game and responds with the calculated action
    """

    url = os.environ['URL']
    key = os.environ['KEY']

    async with websockets.connect(f'{url}?key={key}') as websocket:
        print('Waiting for initial state...', flush=True)
        game = Game()

        while True:
            game_state_json = await websocket.recv()
            game_state = convert_json_string_to_game_state(game_state_json)

            if not game_state.is_running():
                print('game over')
                break
            if not game_state.get_player().is_active():
                print('player died')
                break

            action = game.predict_move(game_state)

            for player in game_state.get_players():
                if player.get_id() == game_state.get_you():
                    print('WE: pos: %s, alive: %s' % (player.get_pos(), player.is_active()))
                else:
                    print('id: %s, active: %s' % (player.get_id(), player.is_active()))

            print('player still alive after %s moves' % game.get_move_counter())

            action_json = json.dumps({'action': str(action)})
            await websocket.send(action_json)

def convert_json_string_to_game_state(json_string):
    """Converts the json string of the game state into an object of type [GameState] and returns it

    Args:
        json_string ([string]): game state as json string

    Returns:
        [GameState]: The converted GameState object
    """
    game_state_as_dict = json.loads(json_string)

    game_state = GameState.from_dict(game_state_as_dict)

    return game_state

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(play())
