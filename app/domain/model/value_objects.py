from enum import Enum

class Routine(str, Enum):
    SEDENTARY   = "SEDENTARY"
    LIGHT       = "LIGHT"
    MODERATE    = "MODERATE"
    ACTIVE      = "ACTIVE"
    VERY_ACTIVE = "VERY_ACTIVE"

class Goal(str, Enum):
    LOSE_WEIGHT    = "LOSE_WEIGHT"
    GAIN_MUSCLE    = "GAIN_MUSCLE"
    MAINTAIN       = "MAINTAIN"
    IMPROVE_CARDIO = "IMPROVE_CARDIO"
    FLEXIBILITY    = "FLEXIBILITY"

class IMCCategory(str, Enum):
    UNDERWEIGHT = "UNDERWEIGHT"
    NORMAL      = "NORMAL"
    OVERWEIGHT  = "OVERWEIGHT"
    OBESE       = "OBESE"