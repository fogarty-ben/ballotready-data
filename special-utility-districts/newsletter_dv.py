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

def augment_geojson(df, geojson):
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

def save_geojson(geojson, filepath):
    with open(filepath, 'w') as f:
        json.dump(geojson, f)

def run(data_fp, geojson_fp, output_fp):
    data = load_data_file(data_fp)
    geojson = load_geojson(geojson_fp)
    geojson = augment_geojson(data, geojson)
    save_geojson(geojson, output_fp)


