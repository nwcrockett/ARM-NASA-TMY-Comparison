import pandas as pd
import numpy as np
import sys
import Comparison_graphs as cg


def graph_bined_by_month(df_nasa, df_arm):
    """

    :param df_nasa:
    :param df_arm:
    :return:
    """
    unique_years_arm = np.unique(df_arm.date_time.dt.year)
    unique_years_nasa = np.unique(df_nasa["YEAR"].values)
    month_dict = {"01": 'January', "02": 'February', "03": 'March', "04": 'April', "05": 'May', "06": 'June',
                  "07": 'July', "08": 'August', "09": 'September', "10": 'October',
                  "11": 'November', "12": 'December'}

    pd_months = []
    difference_months = []
    month_names = []
    pd_y_min = 0
    pd_y_max = 0
    d_y_min = 0
    d_y_max = 0

    if not (bool(set(unique_years_arm).intersection(unique_years_nasa))):
        print(unique_years_arm)
        print(unique_years_nasa)
        print(type(unique_years_nasa[0]))
        print(type(unique_years_arm[0]))
        print("I do not have a year matchup")
        sys.exit(0)

    for m, mn in month_dict.items():
        if m == "01" or m == "12":
            print("JAN or DEC skipping")
            continue
        month_names.append(mn)

        df_nasa_month = df_nasa.loc[df_nasa["MO"] == int(m)]
        df_arm_month = df_arm.loc[df_arm.date_time.dt.month == int(m)]

        unique_years_arm = np.unique(df_arm_month.date_time.dt.year.values)
        year_num = unique_years_arm.astype(np.int)

        nasa_sum_by_year = df_nasa_month.groupby("YEAR")["ALLSKY_SFC_SW_DWN"].sum().values
        arm_sum_by_year = df_arm_month.groupby(df_arm_month.date_time.dt.year).sum() / 1000
        arm_sum_by_year = arm_sum_by_year.transpose()
        arm_sum_by_year = arm_sum_by_year.values[0]
        cg.all_year_overview_single_month(
            year_num,
            arm_sum_by_year,
            nasa_sum_by_year,
            "Yearly overview of " + mn)

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

        difference = arm_sums_by_year_values - nasa_sums_by_year_values
        difference_months.append(difference)

        dif_min = np.amin(difference)
        dif_max = np.amax(difference)

        if dif_min < d_y_min:
            d_y_min = dif_min
        if dif_max > d_y_max:
            d_y_max = dif_max

        print()
        print("Percent difference average without absolute value " + mn + " " + str(np.average(percent_difference)))
        print()

        cg.percent_difference(
            year_num,
            percent_difference,
            "% difference between Wonder and NASA POWER for " + mn,
            "year",
            "bined_by_months/percent_difference/")

    print("YEARly overview")
    cg.all_month_over_years(d_y_min, d_y_max, difference_months,
                            month_names, year_num, "difference 12 months")

    cg.all_month_over_years(pd_y_min, pd_y_max, pd_months,
                            month_names, year_num, "percent difference 12 months")



def graph_by_year(df_arm, df_nasa):
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
    year_num = unique_years_arm.astype(np.int)

    cg.yearly_overview(
        year_num,
        arm_yearly_sum.values,
        nasa_yearly_sum.values,
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
        "Graphs_chosen_nasa")

    for yc, yn in zip(unique_years_arm, unique_years_nasa):
        df_arm_month = df_arm.loc[df_arm.date_time.dt.year == yc]
        arm_months = np.unique(df_arm_month.date_time.dt.month)
        months_nasa = np.unique(df_nasa.loc[df_nasa["YEAR"] == yc, "MO"])

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

        print(str(yc))
        print(arm_months)
        print(arm_year_sums.values)
        print(nasa_monthly_sums.values)
        print()

        cg.year_month_sums(
            arm_months,
            arm_year_sums.values,
            nasa_monthly_sums.values,
            str(yc))

        arm_monthly_sums = np.array(arm_year_sums.values)
        nasa_monthly_sums = np.array(nasa_monthly_sums)
        percent_difference = (np.abs(arm_monthly_sums - nasa_monthly_sums) /
                              ((arm_monthly_sums + nasa_monthly_sums) / 2)) * 100

        cg.percent_difference(
            arm_months,
            percent_difference,
            str(yc) + " Percentage difference Graph between Wonder and NASA POWER",
            "Month of the year", "graphs_by_year/percent_difference/")


def arm_data_setup(df_arm):
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
    df_arm = arm_data_setup(df_arm)
    df_nasa = pd.read_csv("barrow_nasa_power.csv", header=10)
    df_nasa.loc[df_nasa["ALLSKY_SFC_SW_DWN"] < 0, "ALLSKY_SFC_SW_DWN"] = 0
    # graph_bined_by_month(df_nasa, df_arm)
    graph_by_year(df_arm, df_nasa)
