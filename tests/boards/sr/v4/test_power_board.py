"""Tests for the SR v4 Power Board and related classes."""
from datetime import timedelta
from typing import Optional

from j5.backends import Backend, Environment
from j5.boards import Board
from j5.boards.sr.v4 import PowerBoard, PowerOutputGroup, PowerOutputPosition
from j5.components import (
    LED,
    BatterySensor,
    BatterySensorInterface,
    Button,
    ButtonInterface,
    LEDInterface,
    Piezo,
    PiezoInterface,
    PowerOutput,
    PowerOutputInterface,
)
from j5.components.piezo import Pitch

MockEnvironment = Environment("MockEnvironment")


class MockPowerBoardBackend(
    PowerOutputInterface,
    PiezoInterface,
    ButtonInterface,
    BatterySensorInterface,
    LEDInterface,
    Backend,
):
    """A mock power board backend implementation."""

    environment = MockEnvironment
    board = PowerBoard

    @classmethod
    def discover(cls):
        """Discover the PowerBoards on this backend."""
        return []

    def get_firmware_version(self, board: 'Board') -> Optional[str]:
        """Get the firmware version reported by the board."""
        return None

    def get_power_output_enabled(self, board: Board, identifier: int) -> bool:
        """Get the enabled status of a power output."""
        return True

    def set_power_output_enabled(
        self, board: Board, identifier: int, enabled: bool,
    ) -> None:
        """Set the enabled status of a power output."""
        pass

    def get_power_output_current(self, board: Board, identifier: int) -> float:
        """Get the current of a power output."""
        return 1.0

    def buzz(
        self, board: Board, identifier: int, duration: timedelta, pitch: Pitch,
    ) -> None:
        """Buzz the buzzer."""
        pass

    def get_button_state(self, board: Board, identifier: int) -> bool:
        """Get the state of a button."""
        return True

    def wait_until_button_pressed(self, board: Board, identifier: int) -> bool:
        """Wait until the button is pressed."""
        pass

    def get_battery_sensor_voltage(self, board: Board, identifier: int) -> float:
        """Get the voltage of a battery sensor."""
        return 11.1

    def get_battery_sensor_current(self, board: Board, identifier: int) -> float:
        """Get the current of a battery sensor."""
        return 1.0

    def get_led_state(self, board: Board, identifier: int) -> bool:
        """Get the state of an LED."""
        return True

    def set_led_state(self, board: Board, identifier: int, state: bool) -> None:
        """Set the state of an LED."""
        pass


def test_power_board_instantiation():
    """Test that we can instantiate a PowerBoard."""
    PowerBoard("SERIAL0", MockPowerBoardBackend())


def test_power_board_discover():
    """Test that we can discover PowerBoards."""
    assert MockPowerBoardBackend.discover() == []


def test_power_board_name():
    """Test the name attribute of the PowerBoard."""
    pb = PowerBoard("SERIAL0", MockPowerBoardBackend())

    assert pb.name == "Student Robotics v4 Power Board"


def test_power_board_serial():
    """Test the serial attribute of the PowerBoard."""
    pb = PowerBoard("SERIAL0", MockPowerBoardBackend())

    assert pb.serial == "SERIAL0"


def test_power_board_make_safe():
    """Test the make_safe method of the PowerBoard."""
    pb = PowerBoard("SERIAL0", MockPowerBoardBackend())
    pb.make_safe()


def test_power_board_outputs():
    """Test the power outputs on the PowerBoard."""
    pb = PowerBoard("SERIAL0", MockPowerBoardBackend())

    assert type(pb.outputs) is PowerOutputGroup
    assert len(pb.outputs) == 6

    assert type(pb.outputs[PowerOutputPosition.H0])

    for output in pb.outputs:
        assert type(output) is PowerOutput


def test_power_board_piezo():
    """Test the Piezo on the PowerBoard."""
    pb = PowerBoard("SERIAL0", MockPowerBoardBackend())

    assert type(pb.piezo) is Piezo


def test_power_board_button():
    """Test the Button on the PowerBoard."""
    pb = PowerBoard("SERIAL0", MockPowerBoardBackend())

    assert type(pb.start_button) is Button


def test_power_board_battery_sensor():
    """Test the Battery Sensor on the Power Board."""
    pb = PowerBoard("SERIAL0", MockPowerBoardBackend())

    assert type(pb.battery_sensor) is BatterySensor


def test_power_board_run_led():
    """Test the run LED on the Power Board."""
    pb = PowerBoard("SERIAL0", MockPowerBoardBackend())

    assert type(pb._run_led) is LED


def test_power_board_error_led():
    """Test the error LED on the Power Board."""
    pb = PowerBoard("SERIAL0", MockPowerBoardBackend())

    assert type(pb._error_led) is LED
