"""
ai_snake_lab/utils/MQHelper.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.constants.DMQ import DMQ


def mq_srv_msg(elem, data):
    return {DMQ.SENDER: DMQ.SIM_SERVER, DMQ.ELEM: elem, DMQ.DATA: data}


def mq_cli_msg(elem, data):
    return {DMQ.SENDER: DMQ.SIM_CLIENT, DMQ.ELEM: elem, DMQ.DATA: data}
