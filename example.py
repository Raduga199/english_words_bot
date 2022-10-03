import gspread

gc = gspread.oauth(
    credentials_filename=r"C:\Users\NASTYA\AppData\Roaming\gspread\credentials.json"
)

sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1XJdOEXyi24SkWr45N7QZgfF0AhxjHWpB46tRbvt8s3I/edit#gid=490512256")

print(sh.sheet1.get_all_values())
