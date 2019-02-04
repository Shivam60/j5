"""Classes for the MotorBoardOutput support."""

from abc import ABCMeta, abstractmethod

from j5.boards import Board
from j5.components.motor_output import MotorOutput, MotorOutputInterface


class MockMotorDriver(MotorOutputInterface):
    """A testing driver for the motor output"""

    def get_motor_power(self, board: Board, identifier: int) -> int:
        """Get the motor power"""
        return -50

    def set_motor_power(self, board: Board, identifier: int, power: int):
        pass

