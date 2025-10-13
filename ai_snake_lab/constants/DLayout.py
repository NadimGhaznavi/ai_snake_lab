"""
constants/DLayout.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.utils.ConstGroup import ConstGroup


class DLayout(ConstGroup):
    """Layout fields used in the TUI"""

    BUTTON_BOX: str = "button_box"
    BUTTON_PAUSE: str = "button_pause"
    BUTTON_QUIT: str = "button_quit"
    BUTTON_RESTART: str = "button_restart"
    BUTTON_ROW: str = "button_row"
    BUTTON_START: str = "button_start"
    BUTTON_DEFAULTS: str = "button_defaults"
    BUTTON_UPDATE: str = "button_update"
    CUR_EPSILON: str = "cur_epsilon"
    CUR_MEM_TYPE: str = "cur_mem_type"
    CUR_MODEL_TYPE: str = "cur_model_type"
    CUR_MOVE_DELAY: str = "cur_move_delay"
    CUR_TRAINING_GAME_ID: str = "cur_training_game_id"
    FILLER_1: str = "filler_1"
    FILLER_2: str = "filler_2"
    FILLER_3: str = "filler_3"
    FILLER_4: str = "filler_4"
    FILLER_5: str = "filler_5"
    FILLER_6: str = "filler_6"
    FILLER_7: str = "filler_7"
    FILLER_8: str = "filler_8"
    GAME_BOARD: str = "game_board"
    GAME_BOX: str = "game_box"
    GAME_SCORE: str = "game_score"
    GAME_SCORE_PLOT: str = "game_score_plot"
    HIGHSCORES: str = "highscores"
    HIGHSCORES_BOX: str = "highscores_box"
    HIGHSCORES_HEADER: str = "highscores_header"
    HIGHSCORES_PLOT: str = "highscore_plot"
    EPSILON_DECAY: str = "epsilon_decay"
    EPSILON_INITIAL: str = "initial_epsilon"
    EPSILON_MIN: str = "epsilon_min"
    INPUT_10: str = "input_10"
    LABEL: str = "label"
    LABEL_SETTINGS: str = "label_settings"
    LABEL_SETTINGS_12: str = "label_settings_12"
    LABEL_SETTINGS_19: str = "label_settings_19"
    MEM_TYPE: str = "memory_type"
    MODEL_TYPE: str = "model_type"
    MOVE_DELAY: str = "move_delay"
    RUNTIME_BOX: str = "runtime_box"
    RUNTIME: str = "runtime"
    SCORE: str = "score"
    SETTINGS_BOX: str = "settings_box"
    SNAKE_LAB_THEME: str = "snake_lab_theme"
    STORED_GAMES: str = "stored_games"
    TABBED_PLOTS: str = "tabbed_plots"
    TITLE: str = "title"
    VARIABLE: str = "variable"
