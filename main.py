# main.py
import pygame
import sys
from constants import *
from screen_manager import ScreenManager
from clock import SharksClockApp

if __name__ == "__main__":
    app = SharksClockApp()
    app.run()