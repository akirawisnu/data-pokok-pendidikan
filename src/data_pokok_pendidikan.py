#!/usr/bin/env python

import pandas as pd
import requests
from random import randint
from time import sleep


def get_province(randmin=3, randmax=5):
    """
    Returns summary data at province level.
    """

    df = 'http://dapo.dikdasmen.kemdikbud.go.id/rekap/progres?'
    df = requests.get(df)
    df = df.json()
    df = pd.DataFrame(df)
    df['kode_wilayah'] =  df['kode_wilayah'].apply(lambda x: x.replace(" ", ""))
    print(df.tail())
    return df

def get_district(randmin=3, randmax=5):
    """
    Returns summary data at district level.

    Args:
        randmin (int) = minimum time interval
        randmax (int) = maximum time interval
    """
    df_prov = get_province(randmin, randmax)
    prov_code = df_prov['kode_wilayah'].unique()
    district_by_prov = [None] * len(df_prov)
    df = pd.DataFrame()

    for i in range(len(prov_code)):
        try:
            dapodik_url = 'http://dapo.dikdasmen.kemdikbud.go.id/rekap/progres?'
            district_url = 'id_level_wilayah=1&kode_wilayah={}&semester_id=20182'.format(prov_code[i])
            district_by_prov[i] = dapodik_url + district_url
            district_by_prov[i] = requests.get(district_by_prov[i])
            district_by_prov[i] = district_by_prov[i].json()
            district_by_prov[i] = pd.DataFrame(district_by_prov[i])
            df = df.append(district_by_prov[i])
            df['kode_wilayah'] =  df['kode_wilayah'].apply(lambda x: x.replace(" ", ""))
            print(df.tail())
            sleep(randint(randmin, randmax))
        except requests.exceptions.HTTPError:
            print("HTTP error")
            pass
        
    return df

def get_subdistrict(randmin=3, randmax=5):
    """
    Returns summary data at subdistrict level.

    Args:
        randmin (int) = minimum time interval
        randmax (int) = maximum time interval    
    """
        
    df_district = get_district(randmin, randmax)
    district_code = df_district['kode_wilayah'].unique()
    subdistrict_by_district = [None] * len(district_code)
    df = pd.DataFrame()

    for i in range(len(district_code)):
        try:
            dapodik_url = 'http://dapo.dikdasmen.kemdikbud.go.id/rekap/progres?'
            subdistrict_url = 'id_level_wilayah=2&kode_wilayah={}&semester_id=20182'.format(district_code[i])
            subdistrict_by_district[i] = dapodik_url + subdistrict_url
            subdistrict_by_district[i] = requests.get(subdistrict_by_district[i])
            subdistrict_by_district[i] = subdistrict_by_district[i].json()
            subdistrict_by_district[i] = pd.DataFrame(subdistrict_by_district[i])
            df = df.append(subdistrict_by_district[i])
            df['kode_wilayah'] =  df['kode_wilayah'].apply(lambda x: x.replace(" ", ""))
            print(df.tail())
            sleep(randint(randmin, randmax))
        except requests.exceptions.HTTPError:
            print("HTTP error")
            pass
        
    return df

def get_school(randmin=3, randmax=5):
    """
    Returns summary data at school level.

    Args:
        randmin (int) = minimum time interval
        randmax (int) = maximum time interval    
    """

    df_subdistrict = get_subdistrict(randmin, randmax)
    subdistrict_code = df_subdistrict['kode_wilayah'].unique()
    school_by_subdistrict = [None] * len(subdistrict_code)
    df = pd.DataFrame()

    for i in range(len(subdistrict_code)):
        try:
            school_by_subdistrict[i] = 'http://dapo.dikdasmen.kemdikbud.go.id/rekap/progresSP?id_level_wilayah=3&kode_wilayah={}&semester_id=20182'.format(subdistrict_code[i])
            school_by_subdistrict[i] = requests.get(school_by_subdistrict[i])
            school_by_subdistrict[i] = school_by_subdistrict[i].json()
            school_by_subdistrict[i] = pd.DataFrame(school_by_subdistrict[i])
            df = df.append(school_by_subdistrict[i])
            print(df.tail())
            sleep(randint(randmin, randmax))
        except requests.exceptions.HTTPError:
            print("HTTP error")
            pass            

    return df

def get_school_detail(randmin=3, randmax=5):
    """
    Returns school information detail for each province, district, and subdistrict.

    Args:
        randmin (int) = minimum time interval
        randmax (int) = maximum time interval    
    """
        
    df_school = get_school(randmin, randmax)
    school_code = df_school['sekolah_id_enkrip'].unique()    
    school_detail = [None] * len(school_code)
    df = pd.DataFrame()
    for i in range(len(school_code)):
        try:
            school_detail[i] = 'http://dapo.dikdasmen.kemdikbud.go.id/rekap/sekolahDetail?semester_id=20182&sekolah_id={}'.format(school_code[i])
            school_detail[i] = requests.get(school_detail[i])
            school_detail[i] = school_detail[i].json()
            school_detail[i] = pd.DataFrame(school_detail[i])
            school_detail[i]['sekolah_id_enkrip'] = school_code[i]
            df = df.append(school_detail[i])
            print(df.tail())
            sleep(randint(randmin, randmax))            
        except requests.exceptions.HTTPError:
            print("HTTP error")
            pass
        
    df = pd.merge(df, df_school, how='left', on='sekolah_id_enkrip')
    return df    

def main():
    return get_school_detail()

if __name__ == "__main__":
    main()