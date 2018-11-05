"""
Run Code code in terminal to obtain data from 'parsed csv section' functions: ex.) x['2nd Pie Chart of Combinations']

 Run code in terminal to obtain Plotly URLs: ex.) round_trip_and_oneway_routes_graph(x['Most Popular Trip Routes'])
 Where "x" = main() and is used to access the data in the main function
 """
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
        row['Start Time'] = dt.datetime.strptime(
            row['Start Time'], '%Y-%m-%dT%H:%M:%S')

        row['End Time'] = dt.datetime.strptime(
            row['End Time'], '%Y-%m-%dT%H:%M:%S')

        # Starting Latitude & Longitude --> converted to float
        row['Starting Station Latitude'] = float(
            row['Starting Station Latitude'] or 0)

        row['Starting Station Longitude'] = float(
            row['Starting Station Longitude']or 0)

        # Ending Latitude & Longitude --> converted to float
        row['Ending Station Latitude'] = float(
            row['Ending Station Latitude'] or 0)

        row['Ending Station Longitude'] = float(
            row['Ending Station Longitude'] or 0)

    return excel_rows

# To calculate average distance of Latitude(s) & Longitude(s)


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

    # append computations from computed_distance() into average_distances_total
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
    starting_station_ID_counter = collections.Counter(
        [row['Starting Station ID'] for row in rows])
    # Most used Bike (indicated by Bike ID) from Ending Station
    ending_station_ID_counter = collections.Counter(
        [row['Ending Station ID'] for row in rows])

    # Set veriables for graphs in main function passing rows that yields manipulated
    commuters = plan_duration_and_passholder_type(rows)
    most_popular_trip_routes = trip_route_data(rows)

    # For 'Total Round Trip Trip Routes'
    round_trip_total = sorted(most_popular_trip_routes.items())
    # To access 'Round Trip' values in nested dictionary
    round_trip_total = [v['Round Trip'] for k, v in round_trip_total]

    # For 'Total One Way Trip Routes'
    one_way_total = sorted(most_popular_trip_routes.items())
    # To access 'One Way' values in nested dictionary
    one_way_total = [v['One Way'] for k, v in one_way_total]

    # for 'Time Intervals for One Way Trips'

    # oneway_time_intervals = one_way_trip_route_and_duration_data(rows)

    scatterplot = scatterplot_data(rows)

    combinations_for_piechart = combination_data(rows)

    combinations_for_piechart2 = combination_data2(rows)

    combinations_for_piechart3 = combination_data3(rows)

    combinations_for_piechart4 = combination_data4(rows)

    trip_time = average_trip_time_data(rows)

# UNCOMMENT
    # distance = distance_traveled_over_time(rows)

    # dummy_test = dummy_functionn(rows)

    # Answer for 'Most Popular Starting Station ID' follows the
    # following format: Ex.)
    # ('whatever is the Starting Station ID is ' Number of occurences)

    # ^^ Same logic applies with 'Most Popular Ending Station ID'

    """
    Retuns Dictionary of all desired data
    """
    return {

        # 'Average Bike Share Path Map': rows,

        # Answer for Average Distance is in Kilometers(Km)
        # Answer to Question 1
        'Average Distance': sum(average_distances_total)/len(average_distances_total),

        # 'Z': distance,

        # "most_common(1)" means return the MOST common or the number 1 recurring Starting Station ID
        # Answer(s) to Question 2
        'Most Popular Starting Station ID': starting_station_ID_counter.most_common(1),
        # Answer(s) to Question 2
        'Most Popular Ending Station ID': ending_station_ID_counter.most_common(1),
        # Answer to Question 4
        'Number of Regular Commuters': commuters,

        'Most Popular Trip Routes': most_popular_trip_routes,

        'Total Round Trip Trip Routes': sum(round_trip_total),

        'Total One Way Trip Routes': sum(one_way_total),

        'Scatterplot': scatterplot,

        'Pie Chart of Combinations': combinations_for_piechart,

        '2nd Pie Chart of Combinations': combinations_for_piechart2,

        '3rd Pie Chart of Combinations': combinations_for_piechart3,

        '4th Pie Chart of Combinations': combinations_for_piechart4,

        'Trip Time': trip_time

        # 'Test': dummy_test
    }


"""
Parsed data from csv Section

"""


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
        passholder_types_dates[date][row['Passholder Type']] += 1

    return passholder_types_dates


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
        trip_route_dates[date][row['Trip Route Category']] += 1

    return trip_route_dates


def scatterplot_data(rows):

    scatterplot_dictionary = {}

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
        if date not in scatterplot_dictionary:

            # You create a new key\value pair on a dictionary by assigning a value to that key. If the key doesn't exist, it's added and points to that value. If it exists, the current value it points to is overwritten.
            scatterplot_dictionary[date] = {'One Way': 0, 'Duration': []}
        scatterplot_dictionary[date][row['Trip Route Category']] += 1
        # scatterplot_dictionary[duration] = scatterplot_dictionary[date]
        scatterplot_dictionary[date]['Duration'].append(row['Duration'])

    for dates in scatterplot_dictionary:
        # temp is to access the value of 'Duration'
        temp = scatterplot_dictionary[dates]['Duration']

        if temp:
            # Divide by 60 to convert minutes from seconds
            scatterplot_dictionary[dates]['Duration'] = (
                sum(temp)/len(temp)) / 60
        else:
            # If am excel box is blank set equal to 0 so the data is not disturbed
            scatterplot_dictionary[dates]['Duration'] = 0

    # scatterplot_dictionary format: {dates {One Way: value, Duration: value} }
    # The value(s) of "dates" is the inner dictionary
    return scatterplot_dictionary


def combination_data(rows):

    combinations_dictionary = {}

    for row in rows:

        # Creates a tuple that counts the number of each occuring combination of all possbillities
        key = (row['Trip Route Category'], row['Passholder Type'])

        if key not in combinations_dictionary:
            combinations_dictionary[key] = 0

        combinations_dictionary[key] += 1

    return combinations_dictionary


def combination_data2(rows):

    combinations_dictionary2 = {}

    for row in rows:

        # Creates a tuple that counts the number of each occuring combination of all possbillities
        key = (row['Trip Route Category'], row['Passholder Type'],
               "Plan Duration - {} day(s)".format(row['Plan Duration']))

        if row['Plan Duration'] == -1:
            continue

        if key not in combinations_dictionary2:
            combinations_dictionary2[key] = 0

        combinations_dictionary2[key] += 1

    return combinations_dictionary2


def combination_data3(rows):

    combinations_dictionary3 = {}

    for row in rows:

        # Creates a tuple that counts the number of each occuring combination of all possbillities
        key = (row['Passholder Type'],
               "Plan Duration - {} day(s)".format(row['Plan Duration']))

        if row['Plan Duration'] == -1:
            continue

        if key not in combinations_dictionary3:
            combinations_dictionary3[key] = 0

        combinations_dictionary3[key] += 1

    return combinations_dictionary3


def combination_data4(rows):

    combinations_dictionary4 = {}

    for row in rows:

        # Creates a tuple that counts the number of each occuring combination of all possbillities
        key = (row['Trip Route Category'],
               "Plan Duration - {} day(s)".format(row['Plan Duration']))

        if row['Plan Duration'] == -1:
            continue

        if key not in combinations_dictionary4:
            combinations_dictionary4[key] = 0

        combinations_dictionary4[key] += 1

    return combinations_dictionary4


def average_trip_time_data(rows):

    avg_trip_time_dictionary = {}

    for row in rows:

        trip_id = row['Trip ID']
        if trip_id == 0:
            continue

        # The Duration are the KEYS and the dictionary of {'One Way'} are the VALUES

        # If we encounter a Start Time for the first time, add 1 to Round Trip or One Way:
        if trip_id not in avg_trip_time_dictionary:

            # You create a new key\value pair on a dictionary by assigning a value to that key. If the key doesn't exist, it's added and points to that value. If it exists, the current value it points to is overwritten.
            avg_trip_time_dictionary[trip_id] = {'Duration': []}
        # avg_trip_time_dictionary[duration] = avg_trip_time_dictionary[date]
        avg_trip_time_dictionary[trip_id]['Duration'].append(row['Duration'])

    for trip_ids in avg_trip_time_dictionary:
        # temp is to access the value of 'Duration'
        temp = avg_trip_time_dictionary[trip_ids]['Duration']

        if temp:
            # Divide by 60 to convert minutes from seconds
            avg_trip_time_dictionary[trip_ids]['Duration'] = (sum(temp)/len(temp)) / 60
        else:
            # If am excel box is blank set equal to 0 so the data is not disturbed
            avg_trip_time_dictionary[trip_ids]['Duration'] = 0

    return avg_trip_time_dictionary


        



"""
Graphs Section
"""

# Data Visualizations total amount of monthly passes and flex passes each day


def regular_commuters_graph(passholder_types_dates):
    # Omitted Walk up because there are NOT using bike shares regularly

    passholder_types_dates = sorted(passholder_types_dates.items())

    layout = go.Layout(
        xaxis=dict(
            color='#fff',
            title='Date',
            zerolinecolor='rgb(255,255,255)',
            tickcolor='#fff'
        ),
        yaxis=dict(
            color='#fff',
            title='Passholder Types',
            zerolinecolor='rgb(255,255,255)',
            tickcolor='#fff'
        ),
        paper_bgcolor='#252830',
        plot_bgcolor='#252830',
        legend=dict(
            traceorder='normal',
            font=dict(
                color='#fff'
            ),
        )
    )

    fig = go.Figure(layout=layout)

    # Bar chart for Monthly Pass
    fig.add_bar(

        # k is short for "Key"
        x=[k for k, v in passholder_types_dates],

        # v is short for "Value"
        y=[v['Monthly Pass'] for k, v in passholder_types_dates],
        name='Monthly Pass'
    )

    # Bar chart for Flex Pass
    fig.add_bar(
        x=[k for k, v in passholder_types_dates],
        y=[v['Flex Pass'] for k, v in passholder_types_dates],
        name='Flex Pass'
    )

    # ply.sign(username, APIkey)
    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("Monthly-and-Flex-Pass.html",
         "w").write("<h1>My cool graph</h1>" + tls.get_embed(url))


# Data Visualizations for total amount of Round Trip (Trip Route) types and One Way (Trip Route) each day
def most_popular_trip_routes_graph(trip_route_dates):

    trip_route_dates = sorted(trip_route_dates.items())

    layout = go.Layout(
        xaxis=dict(
            color='#fff',
            title='Date',
            zerolinecolor='rgb(255,255,255)',
            tickcolor='#fff'
        ),
        yaxis=dict(
            color='#fff',
            title='Trip Routes',
            zerolinecolor='rgb(255,255,255)',
            tickcolor='#fff'
        ),
        paper_bgcolor='#252830',
        plot_bgcolor='#252830',
        title='Most Popular Trip Routes',
        legend=dict(
            traceorder='normal',
            font=dict(
                color='#fff'
            ),
        )
    )

    fig = go.Figure(layout=layout)

    # Bar chart for Round Trip
    fig.add_bar(
        # k is short for "Key"
        x=[k for k, v in trip_route_dates],
        # v is short for "Value"
        y=[v['Round Trip'] for k, v in trip_route_dates],
        name='RoundTrip'
    )

    # Bar chart for One Way
    fig.add_bar(
        x=[k for k, v in trip_route_dates],
        y=[v['One Way'] for k, v in trip_route_dates],
        name='One Way'
    )

    # ply.sign(username, APIkey)
    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("most-popular-trip-routes.html",
         "w").write("<h1>My cool graph</h1>" + tls.get_embed(url))


def scatterplot_graph(scatterplot_dictionary):

    scatterplot_data_for_graph = sorted(scatterplot_dictionary.items())

    layout = go.Layout(
        scene=dict(
            xaxis=dict(
                zerolinecolor='rgb(255,255,255)',
                gridcolor='rgb(255,255,255)',
                showbackground=True,
                title='Date',
            ),
            yaxis=dict(
                zerolinecolor='rgb(255,255,255)',
                gridcolor='rgb(255,255,255)',
                showbackground=True,
                title='One Way Trips',
                color='lightskyblue',
                tickcolor='lightskyblue',
            ),
            zaxis=dict(
                zerolinecolor='rgb(255,255,255)',
                gridcolor='rgb(255,255,255)',
                showbackground=True,
                title='Avg Duration',
                color='#D65076',
                tickcolor='#D65076',
            )
        ),
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),
        paper_bgcolor='#252830',
        plot_bgcolor='#252830',
    )

    fig = go.Figure(layout=layout)

    # k is short for "Key"
    # v is short for "Value"
    fig.add_scatter3d(

        # Date
        x=[k for k, v in scatterplot_data_for_graph],
        # One Way Trips
        y=[v['One Way'] for k, v in scatterplot_data_for_graph],
        # Duration (Minutes)
        z=[v['Duration'] for k, v in scatterplot_data_for_graph],
        # Graph accessories
        mode='markers',
        marker=dict(
            size=10,
            colorscale='Rainbow',
            # colorscale='Viridis',   # choose a colorscale
            opacity=0.8
        )
    )

    # import pdb;pdb.set_trace()
# fig.layout.title = 'ScatterPlot'
# ply.sign(username, APIkey)
    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("scatterplot.html", "w").write(
        "<h1>My cool graph</h1>" + tls.get_embed(url))


def combination_piechart(combinations_dictionary):

    data_combinations = sorted(combinations_dictionary.items())

    layout = go.Layout(
        xaxis=dict(
            color='#fff',
            zerolinecolor='rgb(255,255,255)',
            tickcolor='#fff'
        ),
        yaxis=dict(
            color='#fff',
            zerolinecolor='rgb(255,255,255)',
            tickcolor='#fff'
        ),
        paper_bgcolor='#252830',
        plot_bgcolor='#252830',
        title='Trip Route & Passholder Type Combinations',
        legend=dict(
            traceorder='normal',
            font=dict(
                color='#fff'
            ),
        )
    )

    fig = go.Figure(layout=layout)

    fig.add_pie(

        # Write combinations abbreviations later
        labels=["{} & {}".format(*k) for (k, v) in data_combinations],

        values=[v for (k, v) in data_combinations]
    )

    # ply.sign(username, APIkey)
    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("Trip-Route_and_Passholder-Type-Combinations.html",
         "w").write("<h1>My cool graph</h1>" + tls.get_embed(url))


def combination_piechart2(combinations_dictionary2):

    data_combinations = sorted(combinations_dictionary2.items())

    layout = go.Layout(
        xaxis=dict(
            color='#fff',
            zerolinecolor='rgb(255,255,255)',
            tickcolor='#fff'
        ),
        yaxis=dict(
            color='#fff',
            zerolinecolor='rgb(255,255,255)',
            tickcolor='#fff'
        ),
        paper_bgcolor='#252830',
        plot_bgcolor='#252830',
        title='Trip Route, Passholder Type, and Plan Durations Combinations',
        legend=dict(
            traceorder='normal',
            font=dict(
                color='#fff'
            ),
        )
    )

    fig = go.Figure(layout=layout)

    fig.add_pie(

        # Write combinations abbreviations later
        labels=["{}, {}, {}".format(*k) for (k, v) in data_combinations],

        values=[v for (k, v) in data_combinations]
    )

    # ply.sign(username, APIkey)
    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("Trip-Route_Passholder-Type_Plan-Duration-Combos.html",
         "w").write("<h1>My cool graph</h1>" + tls.get_embed(url))


def combination_piechart3(combinations_dictionary3):

    data_combinations = sorted(combinations_dictionary3.items())

    layout = go.Layout(
        xaxis=dict(
            color='#fff',
            zerolinecolor='rgb(255,255,255)',
            tickcolor='#fff'
        ),
        yaxis=dict(
            color='#fff',
            zerolinecolor='rgb(255,255,255)',
            tickcolor='#fff'
        ),
        paper_bgcolor='#252830',
        plot_bgcolor='#252830',
        title='Passholder Type & Plan Duration Combinations',
        legend=dict(
            traceorder='normal',
            font=dict(
                color='#fff'
            ),
        )
    )

    fig = go.Figure(layout=layout)

    fig.add_pie(

        # Write combinations abbreviations later
        labels=["{} & {}".format(*k) for (k, v) in data_combinations],

        values=[v for (k, v) in data_combinations]
    )

    # ply.sign(username, APIkey)
    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("Passholder-Type_and_Plan-Duration-Combinations.html",
         "w").write("<h1>My cool graph</h1>" + tls.get_embed(url))


def combination_piechart4(combinations_dictionary4):

    data_combinations = sorted(combinations_dictionary4.items())

    layout = go.Layout(
        xaxis=dict(
            color='#fff',
            zerolinecolor='rgb(255,255,255)',
            tickcolor='#fff'
        ),
        yaxis=dict(
            color='#fff',
            zerolinecolor='rgb(255,255,255)',
            tickcolor='#fff'
        ),
        paper_bgcolor='#252830',
        plot_bgcolor='#252830',
        title='Trip Routes & Plan Duration Combinations',
        legend=dict(
            traceorder='normal',
            font=dict(
                color='#fff'
            ),
        )
    )

    fig = go.Figure(layout=layout)

    fig.add_pie(

        # Write combinations abbreviations later
        labels=["{} & {}".format(*k) for (k, v) in data_combinations],

        values=[v for (k, v) in data_combinations]
    )

    # ply.sign(username, APIkey)
    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("Trip-Routes_and_Plan-Duration-Combinations.html",
         "w").write("<h1>My cool graph</h1>" + tls.get_embed(url))


def avg_trip_time_graph(avg_trip_time_dictionary):

    trip_time_averages = sorted(avg_trip_time_dictionary.items())

    x_values = [k for k, v in trip_time_averages]
    y_values = [v['Duration'] for k, v in trip_time_averages]

    layout = go.Layout(
        paper_bgcolor='#252830',
        plot_bgcolor='#252830',
    )


    fig = go.Figure(layout=layout)

    fig.add_table(

        #     # Trip ID
        # x=[k for k, v in trip_time_averages],

        #     # One Way Trips
        # y=[v['Duration'] for k, v in trip_time_averages],
        # # Graph accessories

        header=dict(values=['Trip ID', 'Average Duration(Minutes)'],
            line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
        cells=dict(values=[[x_values],
                        [y_values]],
             line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5
        )
            )

    # import pdb;pdb.set_trace()
# fig.layout.title = 'ScatterPlot'
# ply.sign(username, APIkey)
    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("Average-Trip-Time.html", "w").write(
        "<h1>My cool graph</h1>" + tls.get_embed(url))



def longitudes_and_latitudes_graph(rows):
    
    station_dict = {}
    trip_dict = {}
    max_counter = 1

    for row in rows:

        station_dict[ row['Starting Station ID'] ] = (row['Starting Station Latitude'], row['Starting Station Longitude'])

        key = (row['Starting Station ID'], row['Ending Station ID'])
        if key not in trip_dict:

            trip_dict[key] = [row['Starting Station Latitude'], row['Starting Station Longitude'], row['Ending Station Latitude'], row['Ending Station Longitude'], 0]

            # "+=1" for the counter i.e 0
        trip_dict[key][4]+=1
        max_counter = max(max_counter, trip_dict[key][4])



    layout = dict(
        title = 'Bike Share Paths',
        showlegend = False, 
        geo = dict(
            scope='usa',
            projection=dict( type='azimuthal equal area' ),
            showland = True,
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
        ),
    )
    

    stations = [ dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = [v[1] for k,v in station_dict.items()],
        lat = [v[0] for k,v in station_dict.items()],
        hoverinfo = 'text',
            # Will show Station ID on hover
        text = [k for k,v in station_dict.items()],
        mode = 'markers',
        marker = dict( 
            size=2, 
            color='rgb(255, 0, 0)',
            line = dict(
                width=3,
                color='rgba(68, 68, 68, 0)'
            )
        ))]

        # t is reffering to the built-in "sorted" tuple
    trip_dict =sorted(trip_dict.items(), key=(lambda t: -t[1][4]))
        
    bike_share_paths = []
    for (key, (st_lat, st_lon, end_lat, end_lon, counter)) in trip_dict[:50]:
        bike_share_paths.append(
        dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = [ st_lon, end_lon ],
            lat = [ st_lat, end_lat ],
            mode = 'lines',
            line = dict(
                width = 1,
                color = 'red',
            ),
            opacity = float(counter)/float(max_counter),
        )
    )

    # import pdb; pdb.set_trace()

    fig = go.Figure(data=stations + bike_share_paths, layout=layout)

    ply.sign_in('pnoonan32', open("PlotlyAPI.txt").read().strip())
    url = ply.plot(fig, auto_open=False)
    print(url)
    open("Bike-Share-Trip-Path.html", "w").write(
        "<h1>My cool graph</h1>" + tls.get_embed(url))

if __name__ == "__main__":
    x = main()
