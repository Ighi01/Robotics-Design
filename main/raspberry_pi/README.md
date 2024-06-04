# Robotics and Design - Group 4 - Raspberry Pi code

This folder contains the code for the Raspberry Pi. The code is written in Python and is used to control the robot.

## Installation

[Poetry](https://python-poetry.org/) is used to manage the dependencies. To install the dependencies, run the following command:

```bash
poetry install
```

## Structure

The code is structured as follows:

- `main.py`: The main entry point of the program. All configuration and setup is done here.
- `components`: Contains the code for the different physical components of the robot.
- `robot`: Contains the code for the logical components of the robot.
- `state`: Contains the code for the different states of the robot and the routines that are executed in each state.
- `static`: Contains the static files for audio and images.
- `pyproject.toml`: The configuration file for Poetry.
- `poetry.lock`: The lock file for Poetry.
