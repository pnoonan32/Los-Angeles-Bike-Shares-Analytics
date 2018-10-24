# Run code like this in terminal to obtain Plotly URLs: round_trip_and_oneway_routes_graph(x['Most Popular Trip Routes'])
# Where "x" = main() and is used to access the data in the main function


import csv
import datetime as dt
from math import sin, cos, sqrt, atan2, radians
import collections
import plotly.plotly as ply
import plotly.graph_objs as go
import plotly.tools as tls

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

    # rows yields all manipulated data
    rows = parse()

    #append computations from computed_distance() into average_distances_total 
    average_distances_total = []
    for row in rows:
        # Taking into account potential empty strings that may corrupt data  
        if (
            row['Starting Station Latitude'] == 0
            or row['Starting Station Longitude'] == 0
            or row['Ending Station Latitude'] == 0
            or row['Ending Station Longitude'] == 0
           ):
           continue

        average_distances_total.append(computed_distance(
            row['Starting Station Latitude'],
            row['Starting Station Longitude'],
            row['Ending Station Latitude'],
            row['Ending Station Longitude']
            ))

        # Most used Bike (indicated by Bike ID) from Starting Station
    starting_station_ID_counter = collections.Counter([row['Starting Station ID'] for row in rows])
        # Most used Bike (indicated by Bike ID) from Ending Station
    ending_station_ID_counter = collections.Counter([row['Ending Station ID'] for row in rows])


    # Set veriables for graphs in main function passing rows that yields manipulated
    commuters = plan_duration_and_passholder_type(rows)
    most_popular_trip_routes = trip_route_data(rows)

    # For 'Total Round Trip Trip Routes'
    round_trip_total = sorted(most_popular_trip_routes.items()) 
        #To access 'Round Trip' values in nested dictionary
    round_trip_total = [v['Round Trip'] for k,v in round_trip_total]
   
    # For 'Total One Way Trip Routes'
    one_way_total = sorted(most_popular_trip_routes.items())
        #To access 'One Way' values in nested dictionary
    one_way_total = [v['One Way'] for k,v in one_way_total]


    #for 'Time Intervals for One Way Trips'
    
    oneway_time_intervals = one_way_trip_route_and_duration_data(rows)

    dummy_test = dummy_date_functionn(rows)

    dummy_test2 = dummy_duration_functionn(rows)

    # plan_d = test_function(rows)

     #Answer for 'Most Popular Starting Station ID' follows the
     #following format: Ex.) 
     #('whatever is the Starting Station ID is ' Number of occurences)

     #^^ Same logic applies with 'Most Popular Ending Station ID'
    


    # Retuns Dictionary of all desired data
    return {
            # Answer for Average Distance is in Kilometers(Km)
                #Answer to Question 1
        'Average Distance':sum(average_distances_total)/len(average_distances_total), 
    
    #"most_common(1)" means return the MOST common or the number 1 recurring Starting Station ID
        #Answer(s) to Question 2
    'Most Popular Starting Station ID': starting_station_ID_counter.most_common(1),
        #Answer(s) to Question 2
    'Most Popular Ending Station ID': ending_station_ID_counter.most_common(1),
        #Answer to Question 4
    'Number of Regular Commuters': commuters,

    'Most Popular Trip Routes': most_popular_trip_routes, 

    'Total Round Trip Trip Routes': sum(round_trip_total),

    'Total One Way Trip Routes': sum(one_way_total),

    'Time Intervals for One Way Trips': oneway_time_intervals,

    'Test': dummy_test,

    'Test2': dummy_test2

    # 'Test3': plan_d
    }


# Will display number of commuters for monthly pass each day ANd number of commuters for flex passes each day
def plan_duration_and_passholder_type(rows):

    # rows yields all manipulated data
    # rows = parse()
    
    # Holding Data from plan_duration_and_passholder_type(rows)
    passholder_types_dates = {}

    for row in rows:
        if row['Plan Duration'] == 0:
            continue
        if row['Passholder Type'] == 'Staff Annual':
            continue

        # Filter out weekends
        date = row['Start Time'] 
        if date.weekday() == 5 or date.weekday() == 6:
            continue


        date = date.strftime("%Y-%m-%d")

        # The Dates are the KEYS and the dictionary of {'Monthly Pass' and 'Flex Pass'} are the VALUES

        # If we encounter a Start Time for the first time, add 1 to Monthly pass or flex pass:
        if date not in passholder_types_dates:
            passholder_types_dates[date] = {'Monthly Pass': 0, 'Flex Pass': 0}
        passholder_types_dates[date][ row['Passholder Type'] ] += 1

    return passholder_types_dates



# Data Visualizations total amount of monthly passes and flex passes each day 
def monthly_pass_and_flex_pass_graph(passholder_types_dates):


    passholder_types_dates = sorted(passholder_types_dates.items())
    fig = go.Figure()

    # Bar chart for Monthly Pass
    fig.add_bar(

        # k is short for "Key"
        x = [k for k,v in passholder_types_dates],

        # v is short for "Value"
        y = [v['Monthly Pass'] for k,v in passholder_types_dates],
        name = 'Monthly Pass'
    )

    # Bar chart for Flex Pass
    fig.add_bar(
        x = [k for k,v in passholder_types_dates],
        y = [v['Flex Pass'] for k,v in passholder_types_dates],
        name = 'Flex Pass'
    )

    fig.layout.title = 'Monthly Pass and Flex Pass Rides per Weekday'

    # ply.sign(username, APIkey)
    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("out.html", "w").write("<h1>My cool graph</h1>" + tls.get_embed(url))



# Will display number of Trip Routes for One Ways each day AND number of Trip Routes for Round Trips each day
def trip_route_data(rows):

    # rows yields all manipulated data
    # rows = parse()

    trip_route_dates = {}

    for row in rows:
        
        # Filter out weekends
        date = row['Start Time'] 
        if date.weekday() == 5 or date.weekday() == 6:
            continue


        date = date.strftime("%Y-%m-%d")


        # The Dates are the KEYS and the dictionary of {'Round Trip' and 'One Way'} are the VALUES
        
        # If we encounter a Start Time for the first time, add 1 to Round Trip or One Way:
        if date not in trip_route_dates:
            trip_route_dates[date] = {'Round Trip': 0, 'One Way': 0}
        trip_route_dates[date][ row['Trip Route Category'] ] += 1

    return trip_route_dates





# Data Visualizations for total amount of Round Trip (Trip Route) types and One Way (Trip Route) each day 
def round_trip_and_oneway_routes_graph(trip_route_dates):

    trip_route_dates = sorted(trip_route_dates.items())
    fig = go.Figure()

    #Bar chart for Round Trip
    fig.add_bar(
            # k is short for "Key"
        x = [k for k,v in trip_route_dates],
            # v is short for "Value"
        y = [v['Round Trip'] for k,v in trip_route_dates],
        name='RoundTrip'
    )

    #Bar chart for One Way
    fig.add_bar(
        x = [k for k,v in trip_route_dates],
        y = [v['One Way'] for k,v in trip_route_dates],
        name = 'One Way'
    )

    fig.layout.title = 'Most Popular Trip Routes'

    # ply.sign(username, APIkey)
    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("most-popular-trip-routes.html", "w").write("<h1>My cool graph</h1>" + tls.get_embed(url))


def one_way_trip_route_and_duration_data(rows):
    
    one_way_trip_route_and_duration_dictionary = {}

    for row in rows:
        
            # Ignore non-existant values
        duration = row['Duration']
        if duration == 0:
            continue
            # We only want "One Way" data
        if row['Trip Route Category'] == "Round Trip":
            continue

        # date = row['Start Time'] 
        # if date.weekday() == 5 or date.weekday() == 6:
        #     continue


        # date = date.strftime("%Y-%m-%d")

        # The Duration are the KEYS and the dictionary of {'One Way'} are the VALUES
        
        # If we encounter a Start Time for the first time, add 1 to Round Trip or One Way:
        if duration not in one_way_trip_route_and_duration_dictionary:

            # You create a new key\value pair on a dictionary by assigning a value to that key. If the key doesn't exist, it's added and points to that value. If it exists, the current value it points to is overwritten. 
            one_way_trip_route_and_duration_dictionary[duration] = {'One Way': 0}
        one_way_trip_route_and_duration_dictionary[duration][ row['Trip Route Category'] ] += 1

    return one_way_trip_route_and_duration_dictionary


def one_way_trip_route_and_duration_graph(one_way_trip_route_and_duration_dictionary):

    data_for_oneway_trips_and_duration = sorted(one_way_trip_route_and_duration_dictionary.items())
    fig = go.Figure()

    #Bar chart for One way time intervals
    fig.add_bar(
            # k is short for "Key"
        x = [k for k,v in data_for_oneway_trips_and_duration],
            # v is short for "Value"
        y = [v['One Way'] for k,v in data_for_oneway_trips_and_duration],
        name='One Way Time Intervals'
    )

    # fig.layout.title = 'Time Intervals for One Way Trips'

    # ply.sign(username, APIkey)
    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("out.html", "w").write("<h1>My cool graph</h1>" + tls.get_embed(url))



# THIS FUNCTION IS INCOMPLETE
def dummy_date_functionn(rows):
    
    dummy_dict = {}

    for row in rows:
        
            # Ignore non-existant values
        duration = row['Duration']
        if duration == 0:
            continue
            # We only want "One Way" data
        if row['Trip Route Category'] == "Round Trip":
            continue
            # Filter out weekends
        date = row['Start Time'] 
        if date.weekday() == 5 or date.weekday() == 6:
            continue


        date = date.strftime("%Y-%m-%d")

        # The Duration are the KEYS and the dictionary of {'One Way'} are the VALUES
        
        # If we encounter a Start Time for the first time, add 1 to Round Trip or One Way:
        if date not in dummy_dict:
        
            # You create a new key\value pair on a dictionary by assigning a value to that key. If the key doesn't exist, it's added and points to that value. If it exists, the current value it points to is overwritten. 
            dummy_dict[date] = {'One Way': 0, 'Duration': []}
        dummy_dict[date][ row['Trip Route Category'] ] += 1
        # dummy_dict[duration] = dummy_dict[date]
        dummy_dict[date]['Duration'].append(row['Duration'])
        
    for dates in dummy_dict:
        temp = dummy_dict[dates]['Duration']
        if temp:
            # Divide by 60 to convert to minutes from seconds
            dummy_dict[dates]['Duration'] = (sum(temp)/len(temp)) /60 
        else:
            dummy_dict[dates]['Duration'] = 0

    return dummy_dict



def dummy_duration_functionn(rows):
    
    dummy_duration_dict = {}

    for row in rows:
        
            # Ignore non-existant values
        duration = row['Duration']
        if duration == 0:
            continue
            # We only want "One Way" data
        if row['Trip Route Category'] == "Round Trip":
            continue

        # The Duration are the KEYS and the dictionary of {'One Way'} are the VALUES
        
        # If we encounter a Start Time for the first time, add 1 to Round Trip or One Way:
        if duration not in dummy_duration_dict:
        
            # You create a new key\value pair on a dictionary by assigning a value to that key. If the key doesn't exist, it's added and points to that value. If it exists, the current value it points to is overwritten. 
            dummy_duration_dict[duration] = {'One Way': 0}
        dummy_duration_dict[duration][ row['Trip Route Category'] ] += 1
        # dummy_dict[duration] = dummy_dict[date]
        


    return dummy_duration_dict




def dummy_graph(dummy_dict):

    duration_data_for_graph = sorted(dummy_dict.items())
        # "x" short fpr one_way_trip_route_and_duration_dictionary data
    # x_data = sorted(one_way_trip_route_and_duration_dictionary.items())

    # round_trip_and_one_way = sorted(trip_route_dates.items())
    
    fig = go.Figure()

    fig.layout.scene.xaxis.title = 'X-axis: Date'
            
    fig.layout.scene.yaxis.title = 'Y-axis: One Way Trip Routes'

    fig.layout.scene.zaxis.title = 'Z-axis: Average Duration'
    # k is short for "Key"
    # v is short for "Value"
    fig.add_scatter3d(
        
        # Date
        x = [k for k,v in duration_data_for_graph],
        # One Way Trips    
        y = [v ['One Way'] for k,v in duration_data_for_graph],
        # Duration (Minutes)
         z = [v['Duration'] for k,v in duration_data_for_graph],
        #Graph accessories
        mode='markers',
    marker=dict(
        size=18,               
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
    ),

    # go.Layout(
    #     margin=dict(
    #     l=0,
    #     r=0,
    #     b=0,
    #     t=0,
        
    # )
    # )
    # import pdb;pdb.set_trace()

    # fig.layout.title = 'ScatterPlot'
    # ply.sign(username, APIkey)
    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("scatterplot.html", "w").write("<h1>My cool graph</h1>" + tls.get_embed(url))




# def test_function(rows):

#     plan_duration_dict = {}


#     for row in rows:

#         plan_d = row['Plan Duration']
#         # Filter out weekends
#         date = row['Start Time'] 
#         if date.weekday() == 5 or date.weekday() == 6:
#             continue


#         date = date.strftime("%Y-%m-%d")


#         if plan_d is not plan_duration_dict:
#             plan_duration_dict[date] = plan_d
        
#         plan_duration_dict[date][row ['Plan Duration']] += 1 





if __name__ == "__main__":
    x = main()


