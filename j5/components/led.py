"""Classes for the LED support."""

from abc import abstractmethod
from typing import Type

from j5.boards import Board
from j5.components.component import Component, Interface


class LEDInterface(Interface):
    """An interface containing the methods required to control an LED."""

    @abstractmethod
    def get_led_state(self, board: Board, identifier: int) -> bool:
        """Get the state of an LED."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def set_led_state(self, board: Board, identifier: int, state: bool) -> None:
        """Set the state of an LED."""
        raise NotImplementedError  # pragma: no cover


class LED(Component):
    """A standard Light Emitting Diode."""

    def __init__(self, identifier: int, board: Board, backend: LEDInterface) -> None:
        self._board = board
        self._backend = backend
        self._identifier = identifier

    @staticmethod
    def interface_class() -> Type[LEDInterface]:
        """Get the interface class that is required to use this component."""
        return LEDInterface

    @property
    def state(self) -> bool:
        """Get the current state of the LED."""
        return self._backend.get_led_state(self._board, self._identifier)

    @state.setter
    def state(self, new_state: bool) -> None:
        """Set the state of the LED."""
        self._backend.set_led_state(self._board, self._identifier, new_state)
