import pandas as pd
import numpy as np
import sys
import Subplot_Comparison_Graphs as cg
import matplotlib.pyplot as plt


def graph_binned_by_month(df_nasa, df_arm, df_tmy):
    """
    Graphs each of the data sets by month over a yearly time span.
    At this time I need to go back through and break apart a lot of these functions into separate functions.
    Will do so as soon as I have time.

    :param df_nasa: nasa POWER dataset
    :param df_arm: Arm dataset
    :param df_tmy: tmy dataset
    :return: returns nothing. Will output several graphs
    """
    unique_years_arm = np.unique(df_arm.date_time.dt.year)
    unique_years_nasa = np.unique(df_nasa["YEAR"].values)
    month_dict = {"01": 'January', "02": 'February', "03": 'March', "04": 'April', "05": 'May', "06": 'June',
                  "07": 'July', "08": 'August', "09": 'September', "10": 'October',
                  "11": 'November', "12": 'December'}

    pd_months = []
    difference_arm_nasa = []
    difference_tmy_nasa = []
    difference_tmy_arm = []
    month_names = []
    pd_y_min = 0
    pd_y_max = 0
    d_y_min_arm_nasa = 0
    d_y_max_arm_nasa = 0
    d_y_min_tmy_nasa = 0
    d_y_max_tmy_nasa = 0
    d_y_min_tmy_arm = 0
    d_y_max_tmy_arm = 0

    if not (bool(set(unique_years_arm).intersection(unique_years_nasa))):
        print(unique_years_arm)
        print(unique_years_nasa)
        print(type(unique_years_nasa[0]))
        print(type(unique_years_arm[0]))
        print("I do not have a year matchup")
        sys.exit(0)

    fig = plt.figure(figsize=(20, 20), facecolor='w')
    count = 1
    for m, mn in month_dict.items():
        if m == "01" or m == "12":
            print("JAN or DEC skipping")
            continue
        month_names.append(mn)

        df_nasa_month = df_nasa.loc[df_nasa["MO"] == int(m)]
        df_arm_month = df_arm.loc[df_arm.date_time.dt.month == int(m)]
        df_tmy_month = df_tmy.loc[df_tmy['month'] == m]

        unique_years_arm = np.unique(df_arm_month.date_time.dt.year.values)
        year_num = unique_years_arm.astype(np.int)

        nasa_sum_by_year = df_nasa_month.groupby("YEAR")["ALLSKY_SFC_SW_DWN"].sum().values
        arm_sum_by_year = df_arm_month.groupby(df_arm_month.date_time.dt.year).sum() / 1000
        arm_sum_by_year = arm_sum_by_year.transpose()
        arm_sum_by_year = arm_sum_by_year.values[0]
        tmy_value = df_tmy_month['GHI (W/m^2)'].sum() / 1000

        ax = plt.subplot(4, 4, count)
        cg.all_year_overview_single_month(
            year_num,
            arm_sum_by_year,
            nasa_sum_by_year,
            tmy_value,
            "Yearly overview of " + mn)
        count += 1

        arm_sums_by_year_values = np.array(arm_sum_by_year)
        nasa_sums_by_year_values = np.array(nasa_sum_by_year)
        percent_difference = ((arm_sums_by_year_values - nasa_sums_by_year_values) /
                              ((arm_sums_by_year_values + nasa_sums_by_year_values) / 2)) * 100
        pd_months.append(percent_difference)

        dif_min = np.amin(percent_difference)
        dif_max = np.amax(percent_difference)

        if dif_min < pd_y_min:
            pd_y_min = dif_min
        if dif_max > pd_y_max:
            pd_y_max = dif_max

        # Difference One
        difference = arm_sums_by_year_values - nasa_sums_by_year_values
        difference_arm_nasa.append(difference)

        dif_min = np.amin(difference)
        dif_max = np.amax(difference)

        if dif_min < d_y_min_arm_nasa:
            d_y_min_arm_nasa = dif_min
        if dif_max > d_y_max_arm_nasa:
            d_y_max_arm_nasa = dif_max

        # Difference Two
        difference = nasa_sums_by_year_values - tmy_value
        difference_tmy_nasa.append(difference)

        dif_min = np.amin(difference)
        dif_max = np.amax(difference)

        if dif_min < d_y_min_tmy_nasa:
            d_y_min_tmy_nasa = dif_min
        if dif_max > d_y_max_tmy_nasa:
            d_y_max_tmy_nasa = dif_max

        # Difference Three
        difference = arm_sums_by_year_values - tmy_value
        difference_tmy_arm.append(difference)

        dif_min = np.amin(difference)
        dif_max = np.amax(difference)

        if dif_min < d_y_min_tmy_arm:
            d_y_min_tmy_arm = dif_min
        if dif_max > d_y_max_tmy_arm:
            d_y_max_tmy_arm = dif_max

    plt.tight_layout()
    plt.savefig("binned_by_months/subplot.png")
    plt.show()

    print("Yearly overview")
    print("difference 12 months arm - nasa")
    cg.all_month_over_years(d_y_min_arm_nasa, d_y_max_arm_nasa, difference_arm_nasa,
                            month_names, unique_years_arm, "difference 12 months arm - nasa")

    print("difference 12 months nasa - tmy")
    cg.all_month_over_years(d_y_min_tmy_nasa, d_y_max_tmy_nasa, difference_tmy_nasa,
                            month_names, unique_years_arm, "difference 12 months nasa - tmy")

    print("difference 12 months arm -tmy")
    cg.all_month_over_years(d_y_min_tmy_arm, d_y_max_tmy_arm, difference_tmy_arm,
                            month_names, unique_years_arm, "difference 12 months arm -tmy")

    print("percent difference 12 months")
    cg.all_month_over_years(pd_y_min, pd_y_max, pd_months,
                            month_names, unique_years_arm, "percent difference 12 months")


def graph_by_year(df_arm, df_nasa, df_tmy):
    unique_years_arm = np.unique(df_arm.date_time.dt.year.values)
    unique_years_nasa = np.unique(df_nasa["YEAR"].values)

    if not (bool(set(unique_years_arm).intersection(unique_years_nasa))):
        print(unique_years_arm)
        print(unique_years_nasa)
        print(type(unique_years_nasa[0]))
        print(type(unique_years_arm[0]))
        print("I do not have a year matchup")
        sys.exit(0)

    arm_yearly_sum = df_arm.groupby(df_arm.date_time.dt.year)['down_short_hemisp'].sum() / 1000
    nasa_yearly_sum = df_nasa.groupby("YEAR")["ALLSKY_SFC_SW_DWN"].sum()
    tmy_value = df_tmy['GHI (W/m^2)'].sum() / 1000
    year_num = unique_years_arm.astype(np.int)

    cg.yearly_overview(
        year_num,
        arm_yearly_sum.values,
        nasa_yearly_sum.values,
        tmy_value,
        "Yearly overview")

    arm_yearly_sum = np.array(arm_yearly_sum)
    nasa_yearly_sum = np.array(nasa_yearly_sum)
    percent_difference = ((arm_yearly_sum - nasa_yearly_sum) /
                          ((arm_yearly_sum + nasa_yearly_sum) / 2)) * 100

    cg.percent_difference(
        year_num,
        percent_difference,
        "Percentage difference Graph between Wonder and NASA POWER",
        "Month of the year",
        "graphed_by_year")

    fig = plt.figure(figsize=(20, 20), facecolor='w')
    count = 1
    for yc, yn in zip(unique_years_arm, unique_years_nasa):
        df_arm_month = df_arm.loc[df_arm.date_time.dt.year == yc]
        arm_months = np.unique(df_arm_month.date_time.dt.month)
        months_nasa = np.unique(df_nasa.loc[df_nasa["YEAR"] == yc, "MO"])

        if yc == 2011 or yc == 2018:
            continue

        if not (bool(set(arm_months).intersection(months_nasa))):
            print(arm_months)
            print(months_nasa)
            print(type(arm_months[0]))
            print(type(months_nasa[0]))
            print("I do not have a month match up at year " + str(yc))
            sys.exit(0)

        df_year_nasa = df_nasa[(df_nasa["YEAR"] == yc)]
        arm_year_sums = df_arm_month.groupby(df_arm_month.date_time.dt.month)['down_short_hemisp'].sum() / 1000
        nasa_monthly_sums = df_year_nasa.groupby("MO")["ALLSKY_SFC_SW_DWN"].sum()
        tmy_monthly_sums = df_tmy.groupby("month")['GHI (W/m^2)'].sum() / 1000

        ax = plt.subplot(4, 4, count)
        cg.graph_of_one_year(
            arm_months,
            arm_year_sums.values,
            nasa_monthly_sums.values,
            tmy_monthly_sums.values,
            str(yc))
        count += 1

    plt.tight_layout()
    plt.savefig("graphed_by_year/subplot.png")
    plt.show()



def arm_data_setup_barrow(df_arm):
    """
    I have 4 data points for the date 2012-06-15. I cannot drop them since it is a time frame with 24 hour day light.
    first blank spot is at 2012-06-15 00:00:00 and 2012-06-15 00:30:00. The two nearby data points are
    2012-06-15 01:00:00 with 648.34198 and 2012-06-14 23:30:00 with 689.833984. I am doing a linear interrelation
    which means I input in 676.003316 to 2012-06-15 00:00:00 and 662.172648 to 2012-06-15 00:30:00.

    for 2012-06-15 23:00:00 and 2012-06-15 23:30:00 I input 667.3460083333333 and 665.6900026666667
    :param df_arm: arm data frame
    :return:
    """
    df_arm = df_arm.drop(columns=["Unnamed: 0"])
    df_arm.loc[12384, 'down_short_hemisp'] = 676.003316
    df_arm.loc[12385, 'down_short_hemisp'] = 662.172648
    df_arm.loc[12430, 'down_short_hemisp'] = 676.003316
    df_arm.loc[12431, 'down_short_hemisp'] = 662.172648
    df_arm["date_time"] = pd.to_datetime(df_arm["date_time"])
    df_arm_30 = df_arm.loc[df_arm.date_time.dt.minute == 30]
    df_arm_00 = df_arm.loc[df_arm.date_time.dt.minute == 0]
    df_arm_00 = df_arm_00.drop([61094])
    arm_averaged_values = (df_arm_30.down_short_hemisp.values + df_arm_00.down_short_hemisp.values) / 2
    df_arm_00['down_short_hemisp'] = arm_averaged_values
    df_arm_00.loc[df_arm_00['down_short_hemisp'] <= 0, 'down_short_hemisp'] = 0
    df_arm_00 = df_arm_00.groupby(df_arm_00.date_time.dt.date).sum()
    date = pd.to_datetime(df_arm_00.index)
    df_arm_00["date_time"] = date

    return df_arm_00


if __name__ == "__main__":
    df_arm = pd.read_csv("processed_arm_data.csv")
    df_arm = arm_data_setup_barrow(df_arm)
    df_nasa = pd.read_csv("barrow_nasa_power.csv", header=10)
    df_nasa.loc[df_nasa["ALLSKY_SFC_SW_DWN"] < 0, "ALLSKY_SFC_SW_DWN"] = 0
    df_tmy = pd.read_csv("Barrow tmy3.CSV", header=1)
    temp = df_tmy['Date (MM/DD/YYYY)'].str.split("/")
    df_tmy[["month", "day", "year"]] = pd.DataFrame(temp.values.tolist(), index=df_tmy.index)
    graph_binned_by_month(df_nasa, df_arm, df_tmy)
    graph_by_year(df_arm, df_nasa, df_tmy)
