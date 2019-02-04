from abc import ABCMeta, abstractmethod

from j5.boards import Board
from j5.components import Component


class MotorOutputInterface(metaclass=ABCMeta):
    """An interface containing the methods to control a motor output"""

    @abstractmethod
    def get_motor_power(self, board: Board, identifier: int):
        """Gets the output power of a motor"""
        raise NotImplementedError

    @abstractmethod
    def set_motor_power(self, board: Board, identifier: int, power: int):
        """Set the output power"""
        raise NotImplementedError


class MotorOutput(Component):
    """An output port on the motor board"""

    def __int__(self, identifier: int, board: Board, backend: MotorOutputInterface):
        self._board = board
        self._backend = backend
        self._identifier = identifier

    @staticmethod
    def interface_class():
        """Get the interface class that is required to use this component"""
        return MotorOutputInterface

    @property
    def motor_power(self) -> int:
        """Get the power value of the motor"""
        return self._backend.get_motor_power(self._board, self._identifier)

    @motor_power.setter
    def motor_power(self, power_value: int):
        """Set the power value for a motor output"""
        if abs(power_value) > 100:
            """Checks if value is within range"""
            raise ValueError("Motor speed value out of range! Should be between -100 and 100!")
        
        self._backend.set_motor_power(self._board, self._identifier, power_value)
