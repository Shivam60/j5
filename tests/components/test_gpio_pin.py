"""Tests for the GPIO Pin Classes."""
from typing import List, Optional, Type

import pytest

from j5.backends import Backend
from j5.boards import Board
from j5.components import Component, NotSupportedByHardwareError
from j5.components.gpio_pin import (
    BadGPIOPinModeError,
    GPIOPin,
    GPIOPinInterface,
    GPIOPinMode,
)


class MockGPIOPinDriver(GPIOPinInterface):
    """A testing driver for the GPIO pin component."""

    def __init__(self):

        self.pin_count: int = 10
        self._mode: List[GPIOPinMode] = [
            GPIOPinMode.DIGITAL_OUTPUT for _ in range(0, self.pin_count)
        ]

        self._written_digital_state: List[bool] = [
            False for _ in range(0, self.pin_count)
        ]

        self._digital_state: List[bool] = [
            False for _ in range(0, self.pin_count)
        ]

    def set_gpio_pin_mode(self, board: Board, identifier: int, pin_mode: GPIOPinMode):
        """Set the hardware mode of a pin."""
        self._mode[identifier] = pin_mode

    def get_gpio_pin_mode(self, board: Board, identifier: int) -> GPIOPinMode:
        """Get the hardware mode of a GPIO pin."""
        return self._mode[identifier]

    def write_gpio_pin_digital_state(self, board: Board, identifier: int, state: bool):
        """Write to the digital state of a GPIO pin."""
        self._written_digital_state[identifier] = state

    def get_gpio_pin_digital_state(self, board: Board, identifier: int):
        """Get the last written state of the GPIO pin."""
        return self._written_digital_state[identifier]

    def read_gpio_pin_digital_state(self, board: Board, identifier: int):
        """Read the digital state of the GPIO pin."""
        return self._digital_state[identifier]

    def read_gpio_pin_analogue_value(self, board: Board, identifier: int) -> float:
        """Read the scaled analogue value of the GPIO pin."""
        return 0.6

    def write_gpio_pin_dac_value(
            self,
            board: Board,
            identifier: int,
            scaled_value: float,
    ) -> None:
        """Write a scaled analogue value to the DAC on the GPIO pin."""
        pass

    def write_gpio_pin_pwm_value(
            self,
            board: Board,
            identifier: int,
            duty_cycle: float,
    ) -> None:
        """Write a scaled analogue value to the PWM on the GPIO pin."""
        pass


class MockGPIOPinBoard(Board):
    """A testing board for the GPIO pin."""

    @property
    def name(self) -> str:
        """The name of this board."""
        return "Testing GPIO Pin Board"

    @property
    def serial(self) -> str:
        """The serial number of this board."""
        return "SERIAL"

    @property
    def firmware_version(self) -> Optional[str]:
        """Get the firmware version of this board."""
        return None

    def make_safe(self):
        """Make this board safe."""
        pass

    @staticmethod
    def supported_components() -> List[Type[Component]]:
        """List the types of component that this Board supports."""
        return [GPIOPin]

    @staticmethod
    def discover(backend: Backend) -> List[Board]:
        """Detect all of the boards on a given backend."""
        return []


def test_gpio_pin_interface_implementation():
    """Test that we can implement the GPIO pin interface."""
    MockGPIOPinDriver()


def test_gpio_pin_instantiation():
    """Test that we can instantiate a GPIO pin."""
    GPIOPin(0, MockGPIOPinBoard(), MockGPIOPinDriver())


def test_gpio_pin_interface_class():
    """Test that the GPIO pin Interface class is a GPIOPinInterface."""
    assert GPIOPin.interface_class() is GPIOPinInterface


def test_pin_mode_getter():
    """Test the mode getter."""
    driver = MockGPIOPinDriver()

    pin = GPIOPin(
        0,
        MockGPIOPinBoard(),
        driver,
        initial_mode=GPIOPinMode.DIGITAL_INPUT,
        supported_modes=[GPIOPinMode.DIGITAL_INPUT, GPIOPinMode.DIGITAL_OUTPUT],
    )

    assert pin.mode is GPIOPinMode.DIGITAL_INPUT
    driver._mode[0] = GPIOPinMode.DIGITAL_OUTPUT
    assert pin.mode is GPIOPinMode.DIGITAL_OUTPUT


def test_pin_mode_setter():
    """Test the setter for the pin mode."""
    driver = MockGPIOPinDriver()

    pin = GPIOPin(
        0,
        MockGPIOPinBoard(),
        driver,
        initial_mode=GPIOPinMode.DIGITAL_INPUT,
        supported_modes=[GPIOPinMode.DIGITAL_INPUT, GPIOPinMode.DIGITAL_OUTPUT],
    )

    assert driver._mode[0] is GPIOPinMode.DIGITAL_INPUT
    pin.mode = GPIOPinMode.DIGITAL_OUTPUT
    assert driver._mode[0] is GPIOPinMode.DIGITAL_OUTPUT

    with pytest.raises(NotSupportedByHardwareError):
        pin.mode = GPIOPinMode.ANALOGUE_INPUT


def test_initial_mode():
    """Test that the initial mode of the pin is set correctly."""
    driver = MockGPIOPinDriver()

    # Implicit initial mode with default supported modes
    GPIOPin(0, MockGPIOPinBoard(), driver)
    assert driver._mode[0] is GPIOPinMode.DIGITAL_OUTPUT

    # Implicit initial mode with specified supported modes
    GPIOPin(
        1,
        MockGPIOPinBoard(),
        driver,
        supported_modes=[GPIOPinMode.DIGITAL_INPUT],
    )
    assert driver._mode[1] is GPIOPinMode.DIGITAL_INPUT

    # Explicit initial mode with default supported modes
    GPIOPin(
        2,
        MockGPIOPinBoard(),
        driver,
        initial_mode=GPIOPinMode.DIGITAL_OUTPUT,
    )
    assert driver._mode[2] is GPIOPinMode.DIGITAL_OUTPUT

    # Explicit initial mode with specified supported modes
    GPIOPin(
        2,
        MockGPIOPinBoard(),
        driver,
        initial_mode=GPIOPinMode.DIGITAL_INPUT,
        supported_modes=[GPIOPinMode.DIGITAL_INPUT],
    )
    assert driver._mode[2] is GPIOPinMode.DIGITAL_INPUT

    # Unsupported explicit initial mode with default supported modes
    with pytest.raises(NotSupportedByHardwareError):
        GPIOPin(
            2,
            MockGPIOPinBoard(),
            driver,
            initial_mode=GPIOPinMode.DIGITAL_INPUT,
        )
    # Unsupported explicit initial mode with specified supported modes
    with pytest.raises(NotSupportedByHardwareError):
        GPIOPin(
            2,
            MockGPIOPinBoard(),
            driver,
            initial_mode=GPIOPinMode.DIGITAL_INPUT,
            supported_modes=[GPIOPinMode.DIGITAL_OUTPUT],
        )


def test_supported_modes_length():
    """Test that a pin cannot be created with zero supported modes."""
    driver = MockGPIOPinDriver()

    with pytest.raises(ValueError):
        GPIOPin(
            0,
            MockGPIOPinBoard(),
            driver,
            supported_modes=[],
        )


def test_required_pin_modes():
    """Test the runtime check for required pin modes."""
    driver = MockGPIOPinDriver()
    pin = GPIOPin(
        0,
        MockGPIOPinBoard(),
        driver,
        supported_modes=[
            GPIOPinMode.DIGITAL_OUTPUT,
            GPIOPinMode.DIGITAL_INPUT,
        ],
    )

    # 0
    pin._require_pin_modes([])

    # 1
    pin._require_pin_modes([GPIOPinMode.DIGITAL_OUTPUT])

    with pytest.raises(BadGPIOPinModeError):
        pin._require_pin_modes([GPIOPinMode.DIGITAL_INPUT_PULLUP])

    # 2
    pin._require_pin_modes([
        GPIOPinMode.DIGITAL_OUTPUT,
        GPIOPinMode.DIGITAL_INPUT,
    ])


def test_digital_state_getter():
    """Test that we can get the digital state correctly."""
    driver = MockGPIOPinDriver()
    pin = GPIOPin(
        0,
        MockGPIOPinBoard(),
        driver,
        supported_modes=[
            GPIOPinMode.DIGITAL_OUTPUT,
            GPIOPinMode.DIGITAL_INPUT,
            GPIOPinMode.DIGITAL_INPUT_PULLUP,
            GPIOPinMode.DIGITAL_INPUT_PULLDOWN,
            GPIOPinMode.ANALOGUE_INPUT,
        ],
    )

    # Digital Output
    pin.mode = GPIOPinMode.DIGITAL_OUTPUT
    assert pin.digital_state is driver._written_digital_state[0]
    driver._written_digital_state[0] = not driver._written_digital_state[0]
    assert pin.digital_state is driver._written_digital_state[0]

    # Digital Input
    for mode in [
        GPIOPinMode.DIGITAL_INPUT,
        GPIOPinMode.DIGITAL_INPUT_PULLUP,
        GPIOPinMode.DIGITAL_INPUT_PULLDOWN,
    ]:
        pin.mode = mode
        assert pin.digital_state is driver._digital_state[0]
        driver._digital_state[0] = not driver._digital_state[0]
        assert pin.digital_state is driver._digital_state[0]

    # Analogue
    pin.mode = GPIOPinMode.ANALOGUE_INPUT
    with pytest.raises(BadGPIOPinModeError):
        _ = pin.digital_state


def test_digital_state_setter():
    """Test that we can set the digital state."""
    driver = MockGPIOPinDriver()
    pin = GPIOPin(
        0,
        MockGPIOPinBoard(),
        driver,
        supported_modes=[
            GPIOPinMode.DIGITAL_OUTPUT,
            GPIOPinMode.DIGITAL_INPUT,
            GPIOPinMode.DIGITAL_INPUT_PULLUP,
            GPIOPinMode.ANALOGUE_INPUT,
        ],
    )

    pin.mode = GPIOPinMode.DIGITAL_OUTPUT
    pin.digital_state = True
    assert driver._written_digital_state[0]
    pin.digital_state = False
    assert not driver._written_digital_state[0]


def test_analogue_value_getter():
    """Test that we can get a scaled analogue value."""
    driver = MockGPIOPinDriver()
    pin = GPIOPin(
        0,
        MockGPIOPinBoard(),
        driver,
        supported_modes=[
            GPIOPinMode.DIGITAL_OUTPUT,
            GPIOPinMode.DIGITAL_INPUT,
            GPIOPinMode.DIGITAL_INPUT_PULLUP,
            GPIOPinMode.ANALOGUE_INPUT,
        ],
    )
    pin.mode = GPIOPinMode.ANALOGUE_INPUT
    assert pin.analogue_value == 0.6

    with pytest.raises(BadGPIOPinModeError):
        pin.mode = GPIOPinMode.DIGITAL_OUTPUT
        _ = pin.analogue_value


def test_analogue_value_setter():
    """Test that we can set a scaled analogue value."""
    driver = MockGPIOPinDriver()
    pin = GPIOPin(
        0,
        MockGPIOPinBoard(),
        driver,
        supported_modes=[
            GPIOPinMode.ANALOGUE_OUTPUT,
            GPIOPinMode.PWM_OUTPUT,
        ],
    )

    pin.mode = GPIOPinMode.ANALOGUE_OUTPUT
    pin.analogue_value = 0.6

    pin.mode = GPIOPinMode.PWM_OUTPUT
    pin.analogue_value = 0.7

    with pytest.raises(ValueError):
        pin.analogue_value = -1
