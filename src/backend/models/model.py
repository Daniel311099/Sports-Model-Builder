import json
import os
import pickle
import openai
import numpy as np
import pandas as pd
import dataclasses
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from torch import nn
import math
import matplotlib.pyplot as plt
import torch

class Game(dataclasses):
    id_: int
    home_team: str
    away_team: str
    score: int
    game_week: int

class Comment(dataclasses):
    id_: int
    text: str
    embedding: np.ndarray
    game: Game

class Model(nn.Module):
    pass

    def load_data(self, path: str):
        with open(path, "r") as f:
            self.data = json.load(f)

    def train(self, mode: bool = True):
        return super().train(mode)
    
    # def fit