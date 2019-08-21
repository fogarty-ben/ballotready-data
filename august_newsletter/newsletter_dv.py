import json
import pandas as pd

ABBREVIATIONS_STATES = {"AL": "Alabama",
                       "AK": "Alaska",
                       "AS": "American Samoa",
                       "AZ": "Arizona",
                       "AR": "Arkansas",
                       "CA": "California",
                       "CO": "Colorado",
                       "CT": "Connecticut",
                       "DE": "Delaware",
                       "DC": "District Of Columbia",
                       "FM": "Federated States Of Micronesia",
                       "FL": "Florida",
                       "GA": "Georgia",
                       "GU": "Guam",
                       "HI": "Hawaii",
                       "ID": "Idaho",
                       "IL": "Illinois",
                       "IN": "Indiana",
                       "IA": "Iowa",
                       "KS": "Kansas",
                       "KY": "Kentucky",
                       "LA": "Louisiana",
                       "ME": "Maine",
                       "MH": "Marshall Islands",
                       "MD": "Maryland",
                       "MA": "Massachusetts",
                       "MI": "Michigan",
                       "MN": "Minnesota",
                       "MS": "Mississippi",
                       "MO": "Missouri",
                       "MT": "Montana",
                       "NE": "Nebraska",
                       "NV": "Nevada",
                       "NH": "New Hampshire",
                       "NJ": "New Jersey",
                       "NM": "New Mexico",
                       "NY": "New York",
                       "NC": "North Carolina",
                       "ND": "North Dakota",
                       "MP": "Northern Mariana Islands",
                       "OH": "Ohio",
                       "OK": "Oklahoma",
                       "OR": "Oregon",
                       "PW": "Palau",
                       "PA": "Pennsylvania",
                       "PR": "Puerto Rico",
                       "RI": "Rhode Island",
                       "SC": "South Carolina",
                       "SD": "South Dakota",
                       "TN": "Tennessee",
                       "TX": "Texas",
                       "UT": "Utah",
                       "VT": "Vermont",
                       "VI": "Virgin Islands",
                       "VA": "Virginia",
                       "WA": "Washington",
                       "WV": "West Virginia",
                       "WI": "Wisconsin",
                       "WY": "Wyoming"
                       }

def load_data_file(filepath):
    df = pd.read_csv(filepath)
    df['state'] = df.state.map(ABBREVIATIONS_STATES)

    return df

def load_geojson(filepath):
    with open(filepath, 'r') as f:
        geojson = json.load(f)

    return geojson

def augment_geojson_special_districts(df, geojson):
    for d in geojson['features']:
        properties = d['properties']
        if sum((df.state == properties['NAME']) & (df.next_election_year == 2019)):
            properties['2019_special_districts'] = int(df.loc[(df.state == properties['NAME']) & (df.next_election_year == 2019), 'count'].iloc[0])
        else:
            properties['2019_special_districts'] = 0
        if sum((df.state == properties['NAME']) & (df.next_election_year == 2020)):
            properties['2020_special_districts'] = int(df.loc[(df.state == properties['NAME']) & (df.next_election_year == 2020), 'count'].iloc[0])
        else:
            properties['2020_special_districts']  = 0

    return geojson

def augment_geojson_special_district_types(df, geojson):
    for d in geojson['features']:
        properties = d['properties']
        #2019
        if sum((df.state == properties['NAME']) & (df.next_election_year == 2019) & (df.type == 'land')):
            properties['2019_land'] = int(df.loc[(df.state == properties['NAME']) & (df.next_election_year == 2019) & (df.level == 'land'), 'count'].iloc[0])
        else:
            properties['2019_land'] = 0
        if sum((df.state == properties['NAME']) & (df.next_election_year == 2019) & (df.level == 'utility')):
            properties['2019_utility'] = int(df.loc[(df.state == properties['NAME']) & (df.next_election_year == 2019) & (df.level == 'utility'), 'count'].iloc[0])
        else:
            properties['2019_utility'] = 0

        #2020
        if sum((df.state == properties['NAME']) & (df.next_election_year == 2020) & (df.level == 'land')):
            properties['2020_land] = int(df.loc[(df.state == properties['NAME']) & (df.next_election_year == 2020) & (df.level == 'land'), 'count'].iloc[0])
        else:
            properties['2020_land'] = 0
        if sum((df.state == properties['NAME']) & (df.next_election_year == 2020) & (df.level == 'utility')):
            properties['2020_utility'] = int(df.loc[(df.state == properties['NAME']) & (df.next_election_year == 2020) & (df.level == 'utility'), 'count'].iloc[0])
        else:
            properties['2020_utility'] = 0

    return geojson


def augment_geojson_cities(df, geojson):
    for d in geojson['features']:
        properties = d['properties']
        #2019
        if sum((df.state == properties['NAME']) & (df.next_election_year == 2019) & (df.level == 'Executive')):
            properties['2019_city_executive'] = int(df.loc[(df.state == properties['NAME']) & (df.next_election_year == 2019) & (df.level == 'Executive'), 'count'].iloc[0])
        else:
            properties['2019_city_executive'] = 0
        if sum((df.state == properties['NAME']) & (df.next_election_year == 2019) & (df.level == 'Legislative')):
            properties['2019_city_legislative'] = int(df.loc[(df.state == properties['NAME']) & (df.next_election_year == 2019) & (df.level == 'Legislative'), 'count'].iloc[0])
        else:
            properties['2019_city_legislative'] = 0

        #2020
        if sum((df.state == properties['NAME']) & (df.next_election_year == 2020) & (df.level == 'Executive')):
            properties['2020_city_executive'] = int(df.loc[(df.state == properties['NAME']) & (df.next_election_year == 2020) & (df.level == 'Executive'), 'count'].iloc[0])
        else:
            properties['2020_city_executive'] = 0
        if sum((df.state == properties['NAME']) & (df.next_election_year == 2020) & (df.level == 'Legislative')):
            properties['2020_city_legislative'] = int(df.loc[(df.state == properties['NAME']) & (df.next_election_year == 2020) & (df.level == 'Legislative'), 'count'].iloc[0])
        else:
            properties['2020_city_legislative'] = 0

    return geojson


def save_geojson(geojson, filepath):
    with open(filepath, 'w') as f:
        json.dump(geojson, f)

def run(data_fp, geojson_fp, output_fp, special_districts=False, cities=False,
        special_district_types=False):
    assert special_districts or cities or special_district_types, 'Must specify one of special districts or cities'
    data = load_data_file(data_fp)
    geojson = load_geojson(geojson_fp)
    if special_districts:
        geojson = augment_geojson_special_districts(data, geojson)
    elif cities:
        geojson = augment_geojson_cities(data, geojson)
    elif special_district_types:
        geojson = augment_geojson_special_district_types(data, geojson)
    save_geojson(geojson, output_fp)


