# main.py
import pygame
import sys
from constants import *
from screen_manager import ScreenManager
from clock import NHLClockApp

if __name__ == "__main__":
    app = NHLClockApp()
    app.run()