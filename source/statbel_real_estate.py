import pandas as pd
import numpy as np
import os
from typing import List
from typing import Dict

#visualisation for testing purpose
pd.options.display.max_rows = 20
pd.options.display.max_columns = None

REAL_ESTATE_CSV_FILEPATH = os.path.join(os.path.dirname(os.getcwd()), "data", "clean_dataset.csv")
STATBEL_REAL_ESTATE_CSV_FILEPATH = os.path.join(os.path.dirname(os.getcwd()), "data", "statbel_date_facades_price_median_and_selling_by_municipality.csv")
MUNICIPALITIES_CSV_FILEPATH = os.path.join(os.path.dirname(os.getcwd()), "data", "zipcode-belgium.csv")
CLEANED_CSV_FILEPATH = os.path.join(os.path.dirname(os.getcwd()), "assets", "outputs", "df_with_statbel.csv")

#paths for windows users
REAL_ESTATE_CSV_FILEPATH_WIN = os.path.dirname(os.getcwd()) + r"\data" + "\clean_dataset.csv"
STATBEL_REAL_ESTATE_CSV_FILEPATH_WIN = os.path.dirname(os.getcwd()) + r"\data" + "\statbel date facades price_median and selling by municipality.csv"
MUNICIPALITIES_CSV_FILEPATH_WIN = os.path.dirname(os.getcwd()) + r"\data" + "\zipcode-belgium.csv"
CLEANED_CSV_FILEPATH_WIN = os.path.dirname(os.getcwd()) + r"\assets" + r"\outputs" + "df_after_cleaning.csv"


""" CONSIDERATIONS
Index price overs year could have been better but influence expected to be not so high anyway 
"""

def add_postcode_price(statbel_csv_filepath: str = STATBEL_REAL_ESTATE_CSV_FILEPATH,
             municipalities_csv_filepath: str = MUNICIPALITIES_CSV_FILEPATH,
             real_estate_csv_filepath: str = REAL_ESTATE_CSV_FILEPATH
             ):

    real_estate_0 = pd.read_csv(real_estate_csv_filepath)
    real_estate_out = real_estate_0.copy(deep=True)
    re_postcodes = list(real_estate_out.loc[:,"postcode"].unique())

    municipalities = pd.read_csv(municipalities_csv_filepath, header=None)
    municipalities_columns = ['postcode', 'municipality', 'longitude', 'latitude']
    municipalities.rename(columns=dict(zip(municipalities.columns, municipalities_columns)), inplace=True)
    municipalities = municipalities[municipalities.postcode.isin(re_postcodes)]

    statbel = pd.read_csv(statbel_csv_filepath)
    #fill na to avoid zeros later
    statbel.fillna(0, inplace=True)
    statbel_columns = ["region_sb", "province", "district", "municipality", "year", "building_type", "price_median",
                       "sellings"]
    statbel.rename(columns=dict(zip(statbel.columns, statbel_columns)), inplace=True)
    statbel["pm_per_s"] = statbel.apply(lambda x: x["price_median"] * x["sellings"], axis=1)
           
    # first matching all in dataset, all detected but Antwerp is both 2000 and 2060
    #applying statbel only on selected postcode
    #some locations have no province
    statbel_pc = municipalities.merge(statbel, on='municipality', how='left')
    #saving complete file before manipulation

    sb_postcode = statbel_pc.loc[:, ['postcode', 'pm_per_s', 'sellings', 'latitude', 'longitude']].groupby(by="postcode").agg(
        {'pm_per_s': sum, 'sellings':sum, 'latitude':np.median, 'longitude': np.median})
    sb_postcode["price_m_by_postcode"] = sb_postcode["pm_per_s"] / sb_postcode["sellings"]
    sb_postcode.loc[:, ["price_m_by_postcode", 'latitude', 'longitude']] = sb_postcode.loc[:,
        ["price_m_by_postcode", 'latitude', 'longitude']].apply(lambda x: round(x, 2))

    """aggregations not required
    sb_district = statbel.groupby(by="district").agg(sum)
    sb_district["price_m_by_"] = sb_district["pm_per_s"] / sb_district["sellings"]
    sb_district["price_m_by_"] = sb_district["price_m_by_"].transform(lambda x: round(x, 2))
    sb_province = statbel.groupby(by="province").agg(sum)
    sb_province["price_m_by_"] = sb_province["pm_per_s"] / sb_province["sellings"]
    sb_province["price_m_by_"] = sb_province["price_m_by_"].transform(lambda x: round(x, 2))
    sb_region = statbel.groupby(by="region_sb").agg(sum)
    sb_region["price_m_by_"] = sb_region["pm_per_s"] / sb_region["sellings"]
    sb_region["price_m_by_"] = sb_region["price_m_by_"].transform(lambda x: round(x, 2))
    """
    #drop longitude and latitude before getting median values by postcode
    statbel_pc.drop(columns=["longitude", "latitude"], inplace=True)
    statbel_pc = statbel_pc.merge(sb_postcode.loc[:, ["price_m_by_postcode", "longitude", "latitude"]],
                                  on=["postcode"], how='left')
    #statbel_pc.rename(columns={"price_m_by_postcode": "price_m_by_postcode"}, inplace=True)

    """aggregations not required
    statbel_pc = statbel_pc.merge(sb_district.loc[:, "price_m_by_"], on='district', how='left')
    statbel_pc.rename(columns={"price_m_by_": "price_m_by_district"}, inplace=True)
    statbel_pc = statbel_pc.merge(sb_province.loc[:, "price_m_by_"], on='province', how='left')
    statbel_pc.rename(columns={"price_m_by_": "price_m_by_province"}, inplace=True)
    statbel_pc = statbel_pc.merge(sb_region.loc[:, "price_m_by_"], on='region_sb', how='left')
    statbel_pc.rename(columns={"price_m_by_": "price_m_by_region"}, inplace=True)
    """

    #then I can remove municipalities keeping only valid postcode

    # filtering valid values before removing duplicates after
    statbel_pc = statbel_pc[statbel_pc.pm_per_s > 0]
    # after grouping only location-related columns are kept in statbel_pc before merging with results
    statbel_pc = statbel_pc.drop(columns=["municipality", "year", "building_type", "price_median", "sellings", "pm_per_s"])
    statbel_pc.drop_duplicates(inplace=True)

    out_columns = ["postcode", "price_m_by_postcode", "latitude", "longitude" ] # "price_m_by_district", "price_m_by_province", "price_m_by_region"]

    real_estate_out = real_estate_out.merge(statbel_pc.loc[:, out_columns], on='postcode', how='left')

    return real_estate_out


#TESTING ON WINDOWS (to exclude as comment when running Jupyter NB)
"""
df = add_postcode_price(statbel_csv_filepath= STATBEL_REAL_ESTATE_CSV_FILEPATH_WIN,
                        municipalities_csv_filepath = MUNICIPALITIES_CSV_FILEPATH_WIN,
                        real_estate_csv_filepath = REAL_ESTATE_CSV_FILEPATH_WIN )

df.to_csv(CLEANED_CSV_FILEPATH)
"""
