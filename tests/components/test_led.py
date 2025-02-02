"""Tests for the LED Classes."""
from typing import List, Optional, Type

from j5.backends import Backend
from j5.boards import Board
from j5.components.led import LED, LEDInterface


class MockLEDDriver(LEDInterface):
    """A testing driver for the led."""

    def set_led_state(self, board: Board, identifier: int, state: bool) -> None:
        """Set the state of an led."""
        pass

    def get_led_state(self, board: Board, identifier: int) -> bool:
        """Get the state of an LED."""
        return True


class MockLEDBoard(Board):
    """A testing board for the led."""

    @property
    def name(self) -> str:
        """The name of this board."""
        return "Testing LED Board"

    @property
    def serial(self) -> str:
        """The serial number of this board."""
        return "SERIAL"

    @property
    def firmware_version(self) -> Optional[str]:
        """Get the firmware version of this board."""
        return self._backend.get_firmware_version(self)

    @property
    def supported_components(self) -> List[Type['Component']]:
        """List the types of component that this Board supports."""
        return [LED]

    def make_safe(self):
        """Make this board safe."""
        pass

    @staticmethod
    def discover(backend: Backend):
        """Detect all of the boards on a given backend."""
        return []


def test_led_interface_implementation():
    """Test that we can implement the LEDInterface."""
    MockLEDDriver()


def test_led_instantiation():
    """Test that we can instantiate an LED."""
    LED(0, MockLEDBoard(), MockLEDDriver())


def test_led_state():
    """Test the state property of an LED."""
    led = LED(0, MockLEDBoard(), MockLEDDriver())

    led.state = True
    assert led.state
