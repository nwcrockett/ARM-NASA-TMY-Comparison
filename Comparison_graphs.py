import matplotlib.pyplot as plt


def all_year_overview_single_month(year, arm_values, nasa_values, title):
    bar_width = 0.35
    ax = plt.axes()
    ax.bar(year, arm_values, bar_width, label="arm dataset radiation")
    ax.bar(year - bar_width, nasa_values, bar_width, label="NASA POWER radiation")
    ax.xaxis.set_major_locator(plt.MaxNLocator(4))
    ax.yaxis.set_major_locator(plt.MaxNLocator(4))
    ax.set_xlabel("year")
    ax.set_ylabel("kWh/m2/year")
    plt.legend()
    plt.title(title)
    plt.savefig("bined_by_months/Months/" + title)
    plt.show()


def percent_difference(x, y, title, x_label, location):
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel("%")
    plt.title(title)
    plt.savefig(location + title)
    plt.show()


def all_month_over_years(y_min, y_max, differences_by_month, month_names, years, title):
    plt.figure(figsize=(12, 12))
    plt.xlabel("Years")
    plt.ylabel("kWh/m2/year")
    plt.title(title)
    plt.ylim(y_min, y_max)
    for dif, name in zip(differences_by_month, month_names):
        plt.plot(years[0:13], dif[0:13], label=name)
    plt.legend()
    plt.savefig("bined_by_months/" + title)
    plt.show()


def yearly_overview(year, arm_values, nasa_values, title):
    bar_width = 0.35
    ax = plt.axes()
    ax.bar(year, arm_values, bar_width, label="arm dataset radiation")
    ax.bar(year - bar_width, nasa_values, bar_width, label="NASA POWER radiation")
    ax.xaxis.set_major_locator(plt.MaxNLocator(4))
    ax.yaxis.set_major_locator(plt.MaxNLocator(4))
    ax.set_xlabel("year")
    ax.set_ylabel("kWh/m2/year")
    plt.legend()
    plt.title(title)
    plt.savefig("graphs_by_year/" + title)
    plt.show()


def year_month_sums(months, arm_values, nasa_values, title):
    bar_width = 0.35
    plt.bar(months, arm_values, bar_width, label="arm radiation")
    plt.bar(months - bar_width, nasa_values, bar_width, label="NASA POWER radiation")
    plt.xlabel("Month of the year")
    plt.ylabel("kWh/m2/month")
    plt.legend()
    plt.title(title)
    plt.savefig("graphs_by_year/yearly_sums/" + title + ".png")
    plt.show()


