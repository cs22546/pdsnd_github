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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_list = ['chicago', 'new york city', 'washington']
        try:
            city = input('Please enter city name(chicago, new york city, washington): ').lower()
            if city in city_list:
                break
            else:
                print('Please enter valid city name')
        except:
            print('Please enter valid city name')

    # get user input for month (all, january, february, ... , june)
    while True:
        month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        try:
            month = input('Please enter month (all, january, february, ... , june): ').lower()
            if month in month_list:
                break
            else:
                print('Please enter valid month')
        except:
            print('Please enter valid month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        try:
            day = input('Please enter day of week (all, monday, tuesday, ... , sunday): ').lower()
            if day in day_list:
                break
            else:
                print('Please enter valid day of week')
        except:
            print('Please enter valid day of week')

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create month, day_of_week, hour column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    print('Most common month: ', df['month'].mode()[0])

    # display the most common day of week
    print('Most common day of week: ', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('Most common start hour: ', df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Start Station: ', df['Start Station'].mode()[0])


    # display most commonly used end station
    print('End Station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['start_end_duration'] = df['Start Station'] + ' <--> ' + df['End Station']
    start_end_duration = df['start_end_duration'].mode()[0]
    print('Most frequent combination of START <--> END station trip : ' + start_end_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total travel time: ', total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('Mean travel time: ', mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    cnt_user_types = df['User Type'].value_counts()
    print('Counts of user types: ', cnt_user_types)


    # Display counts of gender
    while True:
        try:
            cnt_gender = df['Gender'].value_counts()
            print('Counts of gender: ', cnt_gender)
            break
        except KeyError:
            print('There is no gender information')
            break

    # Display earliest, most recent, and most common year of birth
    while True:
        try:
            birth_earliest = df['Birth Year'].min()
            birth_recent = df['Birth Year'].max()
            birth_common = df['Birth Year'].mode()[0]
            print('Earliest year of birth: ', int(birth_earliest))
            print('Most recent year of birth: ', int(birth_recent))
            print('Common year of birth: ', int(birth_common))
            break
        except KeyError:
            print('There is no birth information')
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Display 5 lines of raw data until user answer no
        while True:
            display_raw = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            if display_raw.lower() == 'yes':
                print(df.head())
                continue
            elif display_raw.lower() == 'no':
               break

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
