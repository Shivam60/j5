"""Classes for Battery Sensing Components."""

from abc import abstractmethod
from typing import Type

from j5.boards import Board
from j5.components.component import Component, Interface


class BatterySensorInterface(Interface):
    """An interface containing the methods required to read data from a BatterySensor."""

    @abstractmethod
    def get_battery_sensor_voltage(self, board: Board, identifier: int) -> float:
        """Get the voltage of a battery sensor."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_battery_sensor_current(self, board: Board, identifier: int) -> float:
        """Get the current of a battery sensor."""
        raise NotImplementedError  # pragma: no cover


class BatterySensor(Component):
    """A sensor capable of monitoring a battery."""

    def __init__(
        self, identifier: int, board: Board, backend: BatterySensorInterface,
    ) -> None:
        self._board = board
        self._backend = backend
        self._identifier = identifier

    @staticmethod
    def interface_class() -> Type[BatterySensorInterface]:
        """Get the interface class that is required to use this component."""
        return BatterySensorInterface

    @property
    def voltage(self) -> float:
        """Get the voltage of the battery sensor."""
        return self._backend.get_battery_sensor_voltage(self._board, self._identifier)

    @property
    def current(self) -> float:
        """Get the current of the battery sensor."""
        return self._backend.get_battery_sensor_current(self._board, self._identifier)
