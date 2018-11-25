import urllib
import csv
import requests
import time


'''

'''


def get_the_csv_url(lat, lon, start_time, end_time):

    url = "https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py" \
          "?request=execute&identifier=SinglePoint&parameters=ALLSKY_SFC_SW_DWN&startDate=" + str(start_time) \
          + "&endDate=" + str(end_time) + \
          "&userCommunity=SSE&tempAverage=DAILY&outputList=JSON,CSV&lat=" + str(lat) + \
          "&lon=" + str(lon) + "&user=anonymous"
    csv_url = ""
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            if "\"csv\":" in row[0]:
                temp = row[0].split("\"")
                csv_url = temp[3]

    return csv_url


def output_new_nasa_csv_file(new_filename, csv_url):
    response = urllib.request.urlopen(csv_url)
    html = response.read()
    with open(new_filename, 'wb') as f:
        f.write(html)


lat = 71.2905
lon = -156.788
start = 20111001
# end = time.strftime("%Y%m%d")
end = 20180930
csv_url = get_the_csv_url(lat, lon, start, end)
output_new_nasa_csv_file("barrow_nasa_power.csv", csv_url)

