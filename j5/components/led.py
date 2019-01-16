"""Classes for the LED support."""

from abc import ABCMeta, abstractmethod

from j5.components import Component


class LEDInterface(metaclass=ABCMeta):
    """An interface containing the methods required to control an LED."""

    @abstractmethod
    def set_led_state(self, identifier: int, state: bool) -> None:
        """Set the state of an LED."""
        raise NotImplementedError

    @abstractmethod
    def get_led_state(self, identifier: int) -> bool:
        """Set the state of an LED."""
        raise NotImplementedError


class LED(Component):
    """A standard Light Emitting Diode."""

    def __init__(self, identifier: int, backend: LEDInterface) -> None:
        self._backend = backend
        self._identifier = identifier

    @property
    def state(self) -> bool:
        return self._backend.get_led_state(self._identifier)

    @state.setter
    def state(self, new_state: bool) -> None:
        self._backend.set_led_state(self._identifier, new_state)
