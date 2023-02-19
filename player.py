## player entity, components, and processors

from dataclasses import dataclass as component
import esper
import tkinter as tk

@component
class Position(object):
    x: float = 100
    y: float = 100

