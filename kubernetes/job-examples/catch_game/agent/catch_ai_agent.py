# Copyright 2023 Google LLC.
# SPDX-License-Identifier: Apache-2.0

"""Example Catch AI agent."""

import sys

from absl import app

from dm_env_rpc.v1 import connection as dm_env_rpc_connection
from dm_env_rpc.v1 import dm_env_adaptor
from dm_env_rpc.v1 import dm_env_rpc_pb2

import sys, time, logging
import socket
import grpc
import random

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s')
handler.setFormatter(formatter)
root.handlers.clear()
root.addHandler(handler)

_ACTION_LEFT = -1
_ACTION_NOTHING = 0
_ACTION_RIGHT = 1

_ACTION_PADDLE = 'paddle'
_OBSERVATION_BOARD = 'board'

def get_ball_column(board):
  num_rows = board.shape[0]
  num_cols = board.shape[1]
  for row_index in range(num_rows):
    row = board[row_index]
    for col_index in range(num_cols):
      if row[col_index] == 1:
        return col_index

def get_my_column(board):
  num_rows = board.shape[0]
  num_cols = board.shape[1]
  row_index = num_rows - 1
  row = board[row_index]
  for col_index in range(num_cols):
    if row[col_index] == 1:
      return col_index

def wait_until_env_server_responds(hostname, port):
  logging.info(f"hostname={hostname}, port={port}")
  port = int(port)
  timeout_seconds = 60
  check_interval_seconds = 1
  start_time = time.time()
  while time.time() - start_time < timeout_seconds:
    try:
      with socket.create_connection((hostname, port), timeout=check_interval_seconds) as conn:
          logging.info(f"Server is responding, ip={socket.gethostbyname(hostname)}")
          return True
    except socket.timeout:
      logging.info("Server not responding yet, retrying...")
      time.sleep(check_interval_seconds)
    except Exception as e:
      logging.info(f"Unexpected error: {e}")
      time.sleep(check_interval_seconds)
  return False

def main(_):
  server_with_port = sys.argv[1]
  random_step_ratio = float(sys.argv[2])
  hostname, port = server_with_port.split(":")
  port = int(port)
  running = wait_until_env_server_responds(hostname, port)
  if not running:
    logging.info("Environment server is not running on the port")
    sys.exit("-1")

  channel = grpc.insecure_channel(server_with_port)
  with dm_env_rpc_connection.Connection(channel) as connection:
    world_name = dm_env_adaptor.create_world(connection, create_world_settings={})
    env = dm_env_adaptor.join_world(connection, world_name, join_world_settings={})
    with env:
      actions = {_ACTION_PADDLE: _ACTION_NOTHING}
      timestep = env.step(actions)
      board = timestep.observation[_OBSERVATION_BOARD]

      total_reward = 0
      for iteration in range(100):
        logging.info(f"iteration: {iteration}")
        requested_action = _ACTION_NOTHING
        my_column = get_my_column(board)

        # make a random move with a parametrized probability
        if random.random() < random_step_ratio:
          if random.randint(0, 1) == 0:
            requested_action = _ACTION_LEFT
          else:
            requested_action = _ACTION_RIGHT
        else:
          ball_column = get_ball_column(board)
          if my_column < ball_column:
            requested_action = _ACTION_RIGHT
          elif my_column > ball_column:
            requested_action = _ACTION_LEFT

        actions = {_ACTION_PADDLE: requested_action}
        timestep = env.step(actions)
        board = timestep.observation[_OBSERVATION_BOARD]

        reward = timestep.reward
        if reward != None:
          total_reward += reward

        logging.info(f"iteration: {iteration}, reward: {reward}")
      logging.info(f"total_reward {total_reward}")

    connection.send(dm_env_rpc_pb2.DestroyWorldRequest(world_name=world_name))


if __name__ == '__main__':
  app.run(main)
