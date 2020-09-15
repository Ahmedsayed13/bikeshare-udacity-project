import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    print('Let\'s explore some US bikeshare data!')

    cities = ('chicago', 'new york city', 'washington')
    while True:
        city = input('\nWould you like to see data for Chicago ,or New York City, or Washington?\n').lower()
        if city in cities:
            print('\nYou Chose {}'.format(city))
            print('-'*25)
            #stop the loop if city matches
            break
        else:
            print('\nInvalid Input, choose on of the available cities')
            #continue looping if city mismatches
            continue

    months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    while True:
        month = input('\nWhich month would you like to filter by:January, February, March, April, May, or June? Enter "all" to apply no month filter.\n').lower()
        if month in months:
            print('\nYou Chose {} as month filter'.format(month))
            print('-'*33)
            #stop the loop of month matches
            break
        else:
            print('Invalid Input, choose on of the available months or all for no month filter.')
            #contine looping if month mismatches
            continue

   
    days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    while True:
        day = input('\nWhich day would you like to filter by:Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Enter "all" to apply no day filter.\n').lower()
        if day in days:
            print('\nYou Chose {} as day filter'.format(day))
            #stop the loop if day matches
            break
        else:
            print('Invalid Input,choose a day or all for no day filter.')
            #continue looping if day mismatches
            continue

    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # converts the Start Time column to datetime and creates new month and day of week columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filters by month if applicable and creates new dataframe
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filters by day of week if applicable and creates new dataframe
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    cm = df['month'].value_counts().idxmax()
    print('Most Common Month:', cm)

    # display the most common day of week
    cd = df['day_of_week'].value_counts().idxmax()
    print('Most Common Day of the week:', cd)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    ch = df['hour'].value_counts().idxmax()
    print('Most Common Hour:', ch)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    cs = df['Start Station'].value_counts().idxmax()
    print('Most commonly used start station:', cs)

    # display most commonly used end station
    ce = df['End Station'].value_counts().idxmax()
    print('Most commonly used end station:', ce)

    # display most frequent combination of start station and end station trip
    df['Frequent Trip'] = df['Start Station'] + ' to ' + df['End Station']
    ct = df['Frequent Trip'].value_counts().idxmax()
    print('Most common trip:', ct)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    tttm=total_travel_time/60
    print('Total travel time:', total_travel_time, 'seconds')
    print('Total travel time:',round(tttm,2),'minutes')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mttm=mean_travel_time/60
    print('Average travel time:', round(mean_travel_time,2), 'seconds')
    print('Average travel time:',round(mttm,2),'minutes')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    utc = df['User Type'].value_counts()
    print('User Type Count:\n',utc)

    # Display counts of gender
    try:
        # if there is gender column get its count
        gender_count = df['Gender'].value_counts()
        print('\nGender Count:\n', gender_count)
    except KeyError:
        # if there is no gender column like in washintgon print no data
        print('\nGender Count: No data available.')

    # Display earliest, most recent, and most common year of birth
    try:
        #if there is birth year column get the minimum value of it
        bmin = int(df['Birth Year'].min())
        print('\nEarliest year of birth:', bmin)
    except KeyError:
        # if data is not found print no data
        print('\nEarliest year of birth: No data available.')

    try:
        #if there is birth year column get the maximum value of it
        bmax = int(df['Birth Year'].max())
        print('Most recent year of birth:', bmax)
    except KeyError:
        # if data is not found print no data
        print('Most recent year of birth: No data available.')

    try:
        #if there is birth year column get the most common value of it
        bmode = int(df['Birth Year'].value_counts().idxmax())
        print('Most common year of birth:', bmode)
    except KeyError:
        # if data is not found print no data
        print('Most common year of birth: No data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays raw data 5 rows at a time, if requested."""

    show_data = input('\nWould you like to see 5 rows of raw data? yes or no:\n').lower()
    if show_data != 'no':
        i = 0
        while (i < df['Start Time'].count() and show_data != 'no'):
            print(df.iloc[i:i+5])
            i += 5
            more_data = input('\nWould you like to see 5 more rows of data? yes or no:\n').lower()
            if more_data != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
