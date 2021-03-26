__version__ = '0.0.1'

from .io.load_data import Load_data
from .preprocess.connect_df import connect_df
from .preprocess.format_df import format_to_int, format_bike, format_weather
from .preprocess.training import training
from .preprocess.prediction import prediction
from .preprocess.add_data import add_confinement, add_couvre_feu, add_record
from .vis.plot_prediction import plot_prediction
