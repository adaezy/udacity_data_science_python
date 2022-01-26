import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



#no max on sunday chicago february catch this
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter the name of city you want to analyze:").lower()
    while city not in CITY_DATA.keys():
        print("Incorrect inputs. Enter Chicago, New York City or Washington")
        city = input("Enter the name of city you want to analyze:").lower()


    # get user input for month (all, january, february, ... , june)
    months =  ['all','january', 'february', 'march', 'april', 'may', 'june']
    month = input("Enter the name of month you want to analyze:").lower()
    while month not in  months:
        month = input("Enter the name of month you want to analyze:").lower()



    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day= input("Enter the name of day you want to analyze:").lower()
    while day not in days:
        day = input("Enter the name of day you want to analyze:").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int

        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = days.index(day.lower()) + 1
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_months = most_common_value(df['month'])


    # display the most common day of week
    common_day = most_common_value(df['day_of_week'])
    
    

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = most_common_value(df['hour'])
    
    #visualize
    print("View histogram for frequency of hours")
    visualize_station(df['hour'])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return common_months,common_day,common_hour


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = most_common_value(df['Start Station'])
    

    # display most commonly used end station
    most_common_end = most_common_value(df['End Station'])
   

    # display most frequent combination of start station and end station trip
    merge_cols = df['Start Station'] + "," + df['End Station']
    most_common_pair = most_common_value(merge_cols)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return most_common_start ,most_common_end,most_common_pair


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_series = df['Trip Duration']
    if len(trip_series) == 0:
        total_travel_time  = "No Data Available"
        mean_travel_time = "No Data Available"
    else:
        total_travel_time = trip_series.sum()
        # display mean travel time
        mean_travel_time =trip_series.mean()
   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return total_travel_time, mean_travel_time


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #check and remove null values
    
    if len(df['User Type']) > 0:
        counts_user_types = drop_miss(df['User Type']).value_counts()
    else:
        counts_user_types = "No User Type in this data"


    # Display counts of gender
    try:
        if len(df['Gender']) > 0:
            counts_gender = drop_miss(df['Gender']).value_counts()
        else:
            counts_gender = "No Gender in this data"
    except:
        counts_gender = "No Gender Column in this data"

    # Display earliest, most recent, and most common year of birth
    try:
        if  len(df['Birth Year']) > 0:
            df['Birth Year'] = drop_miss(df['Birth Year'])
            most_recent_year_birth = df['Birth Year'].max()
            earliest_year_birth = df['Birth Year'].min()
            most_common_birth = most_common_value(df['Birth Year'])
        else:
            most_recent_year_birth = "No Birth Year in this data"
            earliest_year_birth = "No Birth Year in this data"
            most_common_birth = "No Birth Year in this data"
    except:
        most_recent_year_birth = "No Birth Year Data in this data"
        earliest_year_birth = "No Birth Year Data in this data"
        most_common_birth = "No Birth Year Data in this data"
        



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return counts_user_types,counts_gender,earliest_year_birth,most_recent_year_birth,most_common_birth

def show_raw_data(df):
    """
    This function displays raw inputs of the original dataframe
    :param df: This accepts the dataframe
    :return: Returns 5 lines of the dataframe as requested by the user.
    """
    see_data = input("Would you like to see 5 lines of the raw data? Enter yes or no.\n")
    if see_data.lower() == 'yes':
        ind_val = 0
        while see_data == 'yes' and ind_val < len(df):
            try:
                df_data = df[ind_val: ind_val+5]
                print(df_data)
            except:
                df_data = df[ind_val:]
                print(df_data)
            ind_val += 5
            see_data = input("Would you like to see 5 lines of the raw data? Enter yes or no.\n")

def most_common_value(series):
    """
    This function accepts a series and gives the most common item or items.
    :param series: Series
    :return: List of most common items
    """
    try:
        counts = series.value_counts()
    except:
        return "No data available"
    try:
        max_count = max(counts)
    except:
        return "No data available"
    most_common= counts[counts == max_count]
    most_common = most_common.index.tolist()
    return most_common

def display_time_statistics(time_data):
    """
    This function prints the values of the time statistics
    :param time_data: return values of a function
    :return: printed values
    """
    common_months,common_day,common_hour = time_data
    print("The common month in this data is\\are:")
    try:
        format_print_list(change_to_month(common_months))
    except:
        format_print_list(common_months)
    print("The common day in this data is\\are:")
    format_print_list(common_day)
    print("The common hour in this data is\\are:")
    format_print_list(common_hour)


def display_station_statistics(station_data):
    """
    This function prints the values of the station statistics
    :param station_data: return values of a function
    :return: printed values
    """
    most_common_start, most_common_end, most_common_pair = station_data
    print("The common start station in this data is\\are:")
    format_print_list(most_common_start)
    print("The common end station in this data is\\are:")
    format_print_list(most_common_end)
    print("The common station start and end pair in this data is\\are:")
    format_print_list( most_common_pair)

def display_trip_duration_statistics(trip_duration_data):
    """
    This function prints the values of the trip duration statistics
    :param trip_duration_data: return values of a function
    :return: printed values
    """
    total_travel_time, mean_travel_time = trip_duration_data
    total_travel_time = check_srt_int(total_travel_time)
    mean_travel_time = check_srt_int(mean_travel_time)
    print("The total travel time is: ",total_travel_time)
    
    print("The mean travel time is: ",mean_travel_time)
    

def display_user_statistics(user_data):
    """
     This function prints the values of the display user statistics
    :param user_data: return values of a function
    :return: printed values
    """
    counts_user_types, counts_gender, earliest_year_birth, most_recent_year_birth, most_common_birth = user_data

    if isinstance(counts_user_types,str):
        print("The count of user types are:",counts_user_types)
    else:
        print("The count of user types are:" )
        format_print_list(counts_user_types)


    if isinstance(counts_gender, str):
        counts_gender = counts_gender
        print("The count of genders are:",counts_gender)
    else:
        print("The count of genders are:")
        format_print_list(counts_gender)

    if isinstance(earliest_year_birth, str):
        print("The earliest year birth is:",earliest_year_birth)
    else:
        print("The earliest year birth is:",check_srt_int(earliest_year_birth))

    if isinstance(most_recent_year_birth,str):
        print("The most recent year birth is:", most_recent_year_birth)
    else:
        print("The most recent year birth is:", check_srt_int(most_recent_year_birth))

    if isinstance(most_common_birth,str):
        most_common_birth  = most_common_birth
        print("The most common year of birth is\\are:",most_common_birth)
    else:
        print("The most common year of birth is\\are:")
        format_print_list(most_common_birth)


def check_srt_int(value):
    """
    Checks the type of value
    :return: returns either a string or an int based on type
    """
    if isinstance(value,str):
        value = value 
    elif np.isnan(value):
        value = "No values available"
    else:
        value = int(value)
    return value

def format_print_list(given_list):
    """
    Accepts a list and formats and print values
    :param given_list: List of values
    :return: formatted output
    """
    
    if isinstance(given_list, pd.Series):
        for i,v in enumerate(given_list):
            print("("+str(i+1)+") " + str(given_list.index[i]), v)
    elif isinstance(given_list,str):
        print(given_list)
    elif isinstance(given_list[0],str):
        for i,v in enumerate(given_list):
            print("("+str(i+1)+")",v)
    else:
        for i,v  in enumerate(given_list):
            print("("+str(i+1)+")",int(v))


def change_to_month(month_num):
    """
    change months to dict
    :param month_num: takes a list of months in numerical format
    :return: returns the months in real names of the month.
    """
    months_dict = {}
    months_list =[]
    for i,v in enumerate(months):
        months_dict[i] = v
    for i in month_num:
        #print(i)
        #print(months_dict[i-1])
        months_list.append(months_dict[i-1])
    return months_list


def drop_miss(df):
    """For dropping missing rows in series"""
    df = df.dropna()
    df = df.reset_index(drop=True)
    return df


def visualize_station(data):
    plt.hist(data)
    plt.title("Histogram of Frequency Hours Of Bike Use in a Day")
    plt.xlabel("Hours")
    plt.ylabel("Frequency")
    plt.show()
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #Add columns available
        import pprint
        
        print("These are the columns in dataset:")
        for i in df.columns[1:]:
            pprint.pprint(i)
        
        show_raw_data(df)
        display_time_statistics(time_stats(df))
        display_station_statistics(station_stats(df))
        display_trip_duration_statistics(trip_duration_stats(df))
        display_user_statistics(user_stats(df))



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
