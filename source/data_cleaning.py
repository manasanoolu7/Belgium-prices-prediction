import pandas as pd
import numpy as np
import os
from typing import List

SOURCE_PATH = os.path.dirname(os.getcwd())+r"\data"+"\clean_dataset.csv"
COLUMNS_NAN_REPLACE = ["terrace_area", "garden_area", "land_surface", "price"]
COLUMNS_OUTLIERS_IGNORE = ["terrace_area", "source", "garden_area"]


def get_dataset_cleaned(filepath: str = SOURCE_PATH,
                        columns_nan_to_replace: List[str] = COLUMNS_NAN_REPLACE,
                        columns_outliers_ignore: List[str] = COLUMNS_OUTLIERS_IGNORE):
    df = pd.read_csv(filepath)
    #percentiles for screening out later
    df_description = df.describe(percentiles=[0.75, 0.5, 0.25], include=np.number)
    for column in df_description:


    #deep copy to avoid warnings when indexing
    df_cleaned = df.copy(deep=True)
    for column in columns_nan_to_replace:
        df_cleaned[column] = df_cleaned[column].transform(lambda x: np.nan if x == 0 else x)
    for column in df_description:
        if column not in columns_outliers_ignore:
            p95 = df_description.loc["95%", column]
            p94 = df_description.loc["94%", column]
            p06 = df_description.loc["6%", column]
            p05 = df_description.loc["5%", column]


