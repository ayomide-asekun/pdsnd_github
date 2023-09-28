import time
import pandas as pd
import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv"
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print()

    while True:
        city = input("Enter a city: ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please enter New york city, Chicago or Washington")
    print()

    # get user input for month (all, january, february, ... , june)
    while True:
        print('Please enter "all" if your would like results from all months')
        month = input("What month would you like to explore: ").capitalize()

        if month in [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
            "All",
        ]:
            break
        else:
            print("Please enter a valid month")
    print()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('Please enter "all" if your would like results from all days of the week')
        day = input("What day would you like to explore: ").capitalize()

        if day in [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
            "All",
        ]:
            break
        else:
            print("Please enter a valid day")

    print("-" * 40)
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
    original_df = df.copy()

    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["Hour"] = df["Start Time"].dt.hour
    df["Day"] = df["Start Time"].dt.day_name()
    df["Month"] = df["Start Time"].dt.month_name()

    if month != "All":
        df = df[df["Month"] == month]

    if day != "All":
        df = df[df["Day"] == day]

    return {"new": df, "original": original_df}


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    time.sleep(3.5)

    print("\nCalculating The Most Frequent Times of Travel...")
    start_time = time.time()

    # display the most common month
    common_month = df["Month"].mode()[0]
    print(f"The most common month people rent bikes is: {common_month}")

    # display the most common day of week
    common_dow = df["Day"].mode()[0]
    print(f"People rent bikes the most on: {common_dow}")

    # display the most common start hour
    common_hour = df["Hour"].mode()[0]
    print(f"The most common hour of the day people rent bikes is: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    time.sleep(3.5)
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    pop_start = df["Start Station"].mode()[0]
    print(f"The most popular start station is {pop_start}")

    # display most commonly used end station
    pop_end = df["End Station"].mode()[0]
    print(f"The most popular end station is {pop_end}")

    # display most frequent combination of start station and end station trip
    df["StartEnd Station"] = df["Start Station"] + "mysep" + df["End Station"]
    max_pairings = df["StartEnd Station"].value_counts()[0]

    max_station_list = list()

    df_count_dict = df["StartEnd Station"].value_counts().to_dict().items()
    for key, value in df_count_dict:
        if value == max_pairings:
            most_start, most_end = key.split("mysep")
            max_station_list.append((most_start, most_end))

    for start, end in max_station_list:
        print(
            f"{max_pairings} rides originated at {start} station and terminated at {end} station"
        )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    time.sleep(3.5)
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    total_travel_minutes = round(total_travel_time / 60, 2)
    print(f"The total travel time is: {total_travel_minutes} minutes")

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    mean_travel_time = round(mean_travel_time, 2)
    print(f"The mean travel time is: {mean_travel_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    time.sleep(3.5)
    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_type_dict = df["User Type"].value_counts().to_dict()

    for key, value in user_type_dict.items():
        print(f"There are {value} {key}(s)")

    if "Gender" in df.columns:
        # Display counts of gender
        gender_dict = df["Gender"].value_counts().to_dict()

        for key, value in gender_dict.items():
            print(f"There are {value} {key}(s)")

    if "Birth Year" in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest = int(df["Birth Year"].min())
        print(f"The earliest birth year on record is: {earliest}")

        most_recent = int(df["Birth Year"].max())
        print(f"The most recent birth year on record is: {most_recent}")

        most_common = int(df["Birth Year"].mode()[0])
        print(f"The most common birth year on record is: {most_common}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)["new"]
        original_df = load_data(city, month, day)["original"]

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        loc_start = 0
        loc_end = 5

        view_data = input(
            "Would you like to view 5 rows of individual trip data? Enter yes or no? "
        ).lower()
        while True:
            if view_data == "yes" or loc_end == len(original_df) - 1:
                rows = original_df[loc_start:loc_end].iterrows()
                for row in rows:
                    print(row)
                    print()
                    time.sleep(2)

                loc_start += 5
                loc_end += 5

            else:
                break

            view_data = input("Would you like to view the next 5 rows of data?\n")

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
