"""
constants/DMQ.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.utils.ConstGroup import ConstGroup


class DMQ(ConstGroup):
    """MQ Constants"""

    AVG_EPOCH_LOSS: str = "avg_epoch_loss"
    CMD: str = "cmd"
    CUR_EPSILON: str = "cur_epsilon"
    DATA: str = "data"
    DIRECTION: str = "direction"
    DYNAMIC_TRAINING: str = "dynamic_training"
    ELEM: str = "elem"
    EPOCH: str = "epoch"
    EPSILON_MIN: str = "epsilon_min"
    EPSILON_DECAY: str = "epsilon_decay"
    EPSILON_INITIAL: str = "epsilon_initial"
    ERROR: str = "error"
    EXPLORE_TYPE: str = "explore_type"
    FOOD: str = "food"
    GAME_ID: str = "game_id"
    GAME_NUM: str = "game_num"
    GET_STATE: str = "get_state"
    HIGHSCORE_EVENT: str = "highscore_event"
    LEARNING_RATE: str = "learning_rate"
    MEM_TYPE: str = "mem_type"
    MODEL_TYPE: str = "model_type"
    MOVE_DELAY: str = "move_delay"
    NUM_FRAMES: str = "num_frames"
    OK: str = "ok"
    PAUSE: str = "pause"
    PAUSED: str = "paused"
    REGISTER: str = "register"
    RESET: str = "reset"
    SENDER: str = "sender"
    SNAKE_HEAD: str = "snake_head"
    SNAKE_BODY: str = "snake_body"
    STATUS: str = "status"
    STORED_GAMES: str = "stored_games"
    RESET_MODEL_PARAMS: str = "reset_model_params"
    RUNNING: str = "running"
    RUNTIME: str = "runtime"
    SCORE: str = "score"
    SIM_CLIENT: str = "SimClient"
    SIM_SERVER: str = "SimServer"
    START: str = "start"
    STARTED: str = "started"
    STOP: str = "stop"
    STOPPED: str = "stopped"
    UNSET: str = "unset"
    UPDATE_SNAKE: str = "update_snake"
    UPDATE_FOOD: str = "update_food"


class DMQ_Label(ConstGroup):
    CONNECTED_TO_ROUTER: str = "connected to router at"
    MALFORMED_MESSAGE: str = "Malformed message"
    RECEIVE_ERROR: str = "Error receiving message"
    ROUTER_ERROR: str = "Router error: %s"
    SHUTDOWN_MSG: str = "SimServer shutting down..."
    STARTUP_MSG: str = "SimServer running on %s"
    UNKNOWN_COMMAND: str = "Unknown command"
    UNKNOWN_SENDER: str = "Unknown sender"
    NO_SIMSERVER_CONNECTED: str = "No SimServer connected"
