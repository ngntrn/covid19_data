import gspread
from search import World_Spider, US_Spider

gc = gspread.service_account()

#open Google Sheet, create new worksheet to add world data
sheet = gc.open("COVID19 Data")
sheet.add_worksheet(title="World Data", rows="100", cols="20")
sheet = gc.open("COVID19 Data").worksheet("World Data")

#create dataframe to store data collected
df = World_Spider("https://www.worldometers.info/coronavirus/")
sheet.update([df.columns.values.tolist()] + df.values.tolist())

sheet2 = gc.open("COVID19 Data")
sheet2.add_worksheet(title="USA Data", rows="100", cols="20")
sheet2 = gc.open("COVID19 Data").worksheet("USA Data")

df2 = US_Spider("https://www.worldometers.info/coronavirus/country/us")
sheet2.update([df2.columns.values.tolist()] + df2.values.tolist())

