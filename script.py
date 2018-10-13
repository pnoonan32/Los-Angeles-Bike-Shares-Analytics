import csv
import datetime as dt
from math import sin, cos, sqrt, atan2, radians
import collections

# approximate radius of earth in km
Radius_of_earth = 6373.0

# parse() is just to manipulate the data to be more flexible for future purposes
def parse():
    reader = csv.DictReader(open("metro-bike-share-trip-data.csv"))
    excel_rows = list(reader)
    for row in excel_rows:
        # Duration & Plan Duration --> converted to an integer
        row['Duration'] = int(row['Duration'])
        row['Plan Duration'] = int(row['Plan Duration'] or -1)

        # Reformatting the Times into datetime objects
        row['Start Time'] = dt.datetime.strptime(row['Start Time'],'%Y-%m-%dT%H:%M:%S')

        row['End Time'] = dt.datetime.strptime(row['End Time'],'%Y-%m-%dT%H:%M:%S')

        # Starting Latitude & Longitude --> converted to float
        row['Starting Station Latitude'] = float(row['Starting Station Latitude'] or 0)

        row['Starting Station Longitude'] = float(row['Starting Station Longitude']or 0)

        # Ending Latitude & Longitude --> converted to float
        row['Ending Station Latitude'] = float(row['Ending Station Latitude'] or 0)

        row['Ending Station Longitude'] = float(row['Ending Station Longitude'] or 0)

    return excel_rows

#To calculate average distance of Latitude(s) & Longitude(s) 
def computed_distance(latitude1, longitude1, latitude2, longitude2):

    lat1 = radians(latitude1)
    lon1 = radians(longitude1)
    lat2 = radians(latitude2)
    lon2 = radians(longitude2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Computations for finding distances based on Latitude and Longitude
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    final_answer = Radius_of_earth * c

    return final_answer



def main():
    rows = parse()
    #append computations from computed_distance() into average_distances_sum 
    average_distances_sum = []
    for row in rows:
        # Taking into account potential empty strings that may corrupt data  
        if (
            row['Starting Station Latitude'] == 0
            or row['Starting Station Longitude'] == 0
            or row['Ending Station Latitude'] == 0
            or row['Ending Station Longitude'] == 0
           ):
           continue

        average_distances_sum.append(computed_distance(
            row['Starting Station Latitude'],
            row['Starting Station Longitude'],
            row['Ending Station Latitude'],
            row['Ending Station Longitude']
            ))

    starting_station_ID_counter = collections.Counter([row['Starting Station ID'] for row in rows])

    ending_station_ID_counter = collections.Counter([row['Ending Station ID'] for row in rows])

     # Answer for Average Distance is in Kilometers(Km)

     #Answer for 'Most Popular Starting Station ID' follows the
     #following format: Ex.) 
     #('whatever is the Starting Station ID is ' Number of occurences)

     #^^ Same logic applies with 'Most Popular Ending Station ID'
    


    # Retuns Dictionary of all desired data
    return {
        'Average Distance':sum(computed_distance)/len(computed_distance), 
    
    #"most_common(1)" means return the MOST common or the number 1 recurring Starting Station ID
    'Most Popular Starting Station ID': starting_station_ID_counter.most_common(1),
    
    'Most Popular Ending Station ID': ending_station_ID_counter.most_common(1),
    }

if __name__ == "__main__":
    x = main()


