"""Classes for GPIO Pins."""

from abc import abstractmethod
from enum import IntEnum
from typing import List, Optional, Type

from j5.boards import Board
from j5.components.component import (
    Component,
    Interface,
    NotSupportedByHardwareError,
)


class BadGPIOPinModeError(Exception):
    """The pin is not in the correct mode."""

    pass


class GPIOPinMode(IntEnum):
    """Hardware modes that a GPIO pin can be set to."""

    DIGITAL_INPUT = 0  #: The digital state of the pin can be read
    DIGITAL_INPUT_PULLUP = 1  #: Same as DIGITAL_INPUT but internal pull-up is enabled
    DIGITAL_INPUT_PULLDOWN = 2  #: Same as DIGITAL_INPUT but internal pull-down is enabled
    DIGITAL_OUTPUT = 3  #: The digital state of the pin can be set.

    ANALOGUE_INPUT = 4  #: The analogue voltage of the pin can be read.
    ANALOGUE_OUTPUT = 5  #: The analogue voltage of the pin can be set using a DAC.

    PWM_OUTPUT = 6  #: A PWM output signal can be created on the pin.


class GPIOPinInterface(Interface):
    """An interface containing the methods required for a GPIO Pin."""

    @abstractmethod
    def set_gpio_pin_mode(self,
                          board: Board,
                          identifier: int,
                          pin_mode: GPIOPinMode,
                          ) -> None:
        """Set the hardware mode of a GPIO pin."""
        raise NotImplementedError  # pragma: nocover

    @abstractmethod
    def get_gpio_pin_mode(self, board: Board, identifier: int) -> GPIOPinMode:
        """Get the hardware mode of a GPIO pin."""
        raise NotImplementedError  # pragma: nocover

    @abstractmethod
    def write_gpio_pin_digital_state(self,
                                     board: Board,
                                     identifier: int,
                                     state: bool,
                                     ) -> None:
        """Write to the digital state of a GPIO pin."""
        raise NotImplementedError  # pragma: nocover

    @abstractmethod
    def get_gpio_pin_digital_state(self, board: Board, identifier: int) -> bool:
        """Get the last written state of the GPIO pin."""
        raise NotImplementedError  # pragma: nocover

    @abstractmethod
    def read_gpio_pin_digital_state(self, board: Board, identifier: int) -> bool:
        """Read the digital state of the GPIO pin."""
        raise NotImplementedError  # pragma: nocover

    @abstractmethod
    def read_gpio_pin_analogue_value(self, board: Board, identifier: int) -> float:
        """Read the scaled analogue value of the GPIO pin."""
        raise NotImplementedError  # pragma: nocover

    @abstractmethod
    def write_gpio_pin_dac_value(
            self,
            board: Board,
            identifier: int,
            scaled_value: float,
    ) -> None:
        """Write a scaled analogue value to the DAC on the GPIO pin."""
        raise NotImplementedError  # pragma: nocover

    @abstractmethod
    def write_gpio_pin_pwm_value(
            self,
            board: Board,
            identifier: int,
            duty_cycle: float,
    ) -> None:
        """Write a scaled analogue value to the PWM on the GPIO pin."""
        raise NotImplementedError  # pragma: nocover


class GPIOPin(Component):
    """A GPIO Pin."""

    def __init__(
            self,
            identifier: int,
            board: Board,
            backend: GPIOPinInterface,
            supported_modes: List[GPIOPinMode] = [GPIOPinMode.DIGITAL_OUTPUT],
            initial_mode: Optional[GPIOPinMode] = None,
    ) -> None:
        self._board = board
        self._backend = backend
        self._identifier = identifier
        self._supported_modes = supported_modes

        if len(supported_modes) < 1:
            raise ValueError("A GPIO pin must support at least one GPIOPinMode.")

        if initial_mode is None:
            # If no initial mode is set, choose the first supported mode.
            initial_mode = self._supported_modes[0]
        self.mode = initial_mode

    @staticmethod
    def interface_class() -> Type[GPIOPinInterface]:
        """Get the interface class that is required to use this component."""
        return GPIOPinInterface

    def _require_pin_modes(self, pin_modes: List[GPIOPinMode]) -> None:
        """Ensure that this pin is in the specified hardware mode."""
        if not any(self.mode == mode for mode in pin_modes) and not len(pin_modes) == 0:
            raise BadGPIOPinModeError(
                f"Pin {self._identifier} needs to be in one of {pin_modes}",
            )

    @property
    def mode(self) -> GPIOPinMode:
        """Get the hardware mode of this pin."""
        return self._backend.get_gpio_pin_mode(self._board, self._identifier)

    @mode.setter
    def mode(self, pin_mode: GPIOPinMode) -> None:
        """Set the hardware mode of this pin."""
        if pin_mode not in self._supported_modes:
            raise NotSupportedByHardwareError(
                f"Pin {self._identifier} on {str(self._board)} \
                does not support {str(pin_mode)}.",
            )
        self._backend.set_gpio_pin_mode(self._board, self._identifier, pin_mode)

    @property
    def digital_state(self) -> bool:
        """Get the digital state of the pin."""
        self._require_pin_modes([
            GPIOPinMode.DIGITAL_OUTPUT,
            GPIOPinMode.DIGITAL_INPUT,
            GPIOPinMode.DIGITAL_INPUT_PULLUP,
            GPIOPinMode.DIGITAL_INPUT_PULLDOWN],
        )

        # Behave differently depending on the hardware mode.
        if self.mode is GPIOPinMode.DIGITAL_OUTPUT:
            return self._backend.get_gpio_pin_digital_state(self._board, self._identifier)

        return self._backend.read_gpio_pin_digital_state(self._board, self._identifier)

    @digital_state.setter
    def digital_state(self, state: bool) -> None:
        """Set the digital state of the pin."""
        self._require_pin_modes([GPIOPinMode.DIGITAL_OUTPUT])
        self._backend.write_gpio_pin_digital_state(self._board, self._identifier, state)

    @property
    def analogue_value(self) -> float:
        """Get the scaled analogue reading of the pin."""
        self._require_pin_modes([GPIOPinMode.ANALOGUE_INPUT])
        return self._backend.read_gpio_pin_analogue_value(self._board, self._identifier)

    @analogue_value.setter
    def analogue_value(self, new_value: float) -> None:
        """Set the analogue value of the pin."""
        self._require_pin_modes([
            GPIOPinMode.ANALOGUE_OUTPUT,
            GPIOPinMode.PWM_OUTPUT,
        ])
        if new_value < 0 or new_value > 1:
            raise ValueError("An analogue pin value must be between 0 and 1.")

        if self.mode is GPIOPinMode.ANALOGUE_OUTPUT:
            self._backend.write_gpio_pin_dac_value(
                self._board,
                self._identifier,
                new_value,
            )
        else:
            # We must be a PWM_OUTPUT
            self._backend.write_gpio_pin_pwm_value(
                self._board,
                self._identifier,
                new_value,
            )
