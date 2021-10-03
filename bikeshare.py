import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington).

    city = ''
    while city not in ['chicago', 'new york city', 'washington']:
        city = input(
            'Choose one of the following cities to view bike share data (chicago, new york city, or washington), make sure to spell city name exactly as it is here: ').lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print('Invalid entry.')

    # Get user input for month (all, january, february, ... , june)
    month = ''
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        month = input('Enter the month or enter "all" for all months, spell out month name: ').lower()
        if month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print('Invalid entry')
    #Convert month string to integer.
    month_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
    if month != 'all':
        month = month_dict[month]
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
        day = input('Enter the day of the week or "all" for all days of the week: ').lower()
        if day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
            print('Invalid entry')

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

    #Load selected csv.
    df = pd.read_csv(CITY_DATA[city])


    #Convert 'Start Time' datatype to datetime and convert datetime elements to hour, day, and month.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Hour'] = df['Start Time'].dt.hour
    df['Day'] = df['Start Time'].dt.day_name()
    df['Month'] = df['Start Time'].dt.month

    #Convert month to integer datatype.
    if month != 'all':
        month = int(month)

    if month != 'all':
        df = df[df['Month'] == month]
    if day != 'all':
        df = df[df['Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    month_mode = df['Month'].mode()[0]
    month_list = ['January', 'February', 'March', 'April', 'May', 'June']
    print('The most popular month to rent a bike is {}.'.format(month_list[month_mode - 1]))

    # Display the most common day of week
    day_mode = df['Day'].mode()[0]
    print('The most popular day of the week to rent a bike is {}.'.format(day_mode))


    # Display the most common start hour
    hour_mode = df['Hour'].mode()[0]
    print('The most popular hour of the day to rent a bike is {}:00.'.format(hour_mode))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station_mode = df['Start Station'].mode()[0]
    print('The most popular starting station is {}.'.format(start_station_mode))

    # Display most commonly used end station
    end_station_mode = df['End Station'].mode()[0]
    print('The most popular ending station is {}.'.format(end_station_mode))

    # Display most frequent combination of start station and end station trip
    df['Combo'] = df['Start Station'] + ' and ' + df['End Station']
    combo_mode = df['Combo'].mode()[0]
    print('The most frequent combination of start and end stations is {}.'.format(combo_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    travel_time_sum = df['Trip Duration'].sum()
    print('Total travel time is {} seconds.'.format(travel_time_sum))


    # Display mean travel time
    travel_time_mean = df['Trip Duration'].mean()
    print('Average travel time is {} seconds.'.format(travel_time_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('These are the counts for user types:\n{}'.format(user_types_counts))
    if city == 'chicago' or city == 'new york city':
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print('There are the counts for gender:\n{}'.format(gender_counts))

        # Display earliest, most recent, and most common year of birth
        birth_min = int(df['Birth Year'].min())
        birth_max = int(df['Birth Year'].max())
        birth_mode = int(df['Birth Year'].mode())
        print('Earliest birth year: {}'.format(birth_min))
        print('Latest birth year: {}'.format(birth_max))
        print('Most common birth year: {}'.format(birth_mode))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_ask(df):
    """Asks to show 5 rows of data at a time"""
    response = 'yes'
    start_loc = 0
    end_loc = 4
    while response == 'yes':
        response = input('Would you like to see 5 rows of data? ("yes" or "no").').lower()
        if response == 'yes':
            for i in range((df.shape[0] // 5)):
                while response == 'yes':
                    print(df.iloc[start_loc:end_loc])
                    start_loc += 5
                    end_loc += 5
                    response = input('Would you like to see another 5 rows? ("yes" or "no")').lower()
        elif response == 'no':
            break
        elif response != 'yes' or response != 'no':
            print('Invalid entry')
            response = 'yes'
        else:
            continue




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        data_ask(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
