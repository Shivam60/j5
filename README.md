# j5

[![CircleCI](https://circleci.com/gh/j5api/j5.svg?style=svg)](https://circleci.com/gh/j5api/j5)
[![Test Coverage](https://api.codeclimate.com/v1/badges/54e440aba5a51c9ee133/test_coverage)](https://codeclimate.com/github/j5api/j5/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/54e440aba5a51c9ee133/maintainability)](https://codeclimate.com/github/j5api/j5/maintainability)
[![Documentation Status](https://readthedocs.org/projects/j5/badge/?version=master)](https://j5.readthedocs.io/en/master/?badge=master)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](http://opensource.org/licenses/MIT)
![Bees](https://img.shields.io/badge/bees-110%25-yellow.svg)

j5 Robotics API - Currently under development.

## What is j5?

`j5` is a Python 3 library that aims to abstract away robotics hardware and provide a consistent API for robotics. It was created to reduce the replication of effort into developing the separate, yet very similar APIs for several robotics competitions. Combining the API into a single library with support for various hardware gives a consistent feel for students and volunteers. This means more time to work on building robots!

## How do I use j5?

`j5` is designed to never be visible to students. It sits behind the scenes and works magic.

```python
from robot import Robot

r = Robot()
r.motor_boards[0].motors[1] = 0.5
```

The above code is likely to be familiar to any student who has competed in one of the below competitions. However, it is not a trivial problem to make this code portable across the platforms. For example, the motor board for Student Robotics is a separate board to the brain board, but is built into the same board for HR RoboCon.

`j5` lets competition vendors define how the basic parts of the apis are accessed. A robot can thus be constructed from any combination of parts from various organisations.

```python
from j5.boards import BoardGroup
from j5.backends.hw import HardwareEnvironment

from j5.boards.sr.v4 import PowerBoard, MotorBoard, ServoBoard, Ruggeduino


class Robot:

    def __init__(self):

        self._env = HardwareEnvironment()

        self.power_board = PowerBoard(self._env)

        self.motor_boards = BoardGroup(MotorBoard, self._env)
        self.motor_board = self.motor_boards.singular()

        self.servo_boards = BoardGroup(ServoBoard, self._env)
        self.servo_board = self.servo_boards.singular()

        self.ruggeduino = Ruggeduino(self._env)

```

## Competitions

We intend to support the kits of the following robotics competitions:

- [SourceBots](https://sourcebots.co.uk/)
- [Student Robotics](https://studentrobotics.org/)
- [Hills Road RoboCon](https://hr-robocon.org/)

Whilst `j5` isn't officially endorsed by Student Robotics or RoboCon, we are working closely with Student Robotics to ensure perfect compatibility. Many `j5` contributors are members of Student Robotics and SourceBots.

If you are interested in adding support for your hardware, please get in touch.

## Contributions

This project is released under the MIT Licence. For more information, please see `LICENSE`.

`j5 contributors` refers to the people listed in the `CONTRIBUTORS` file.

The `CONTRIBUTORS` file can be generated by executing `CONTRIBUTORS.gen`. This generated file contains a list of people who have contributed to the `j5` project.

`j5` is being developed by a group of volunteers primarily based at the University of Southampton. We welcome contributions and reside in a channel on the SourceBots Slack.
