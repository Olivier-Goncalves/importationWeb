import requests
import json
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta

startDate = "18/04/22"
duration = 10
testPD = pd.Series(pd.date_range(startDate, freq="D", periods=duration))
dateDebutObject = dt.strptime(startDate, "%d/%m/%y")
date = dateDebutObject
donneesFinales = dict.fromkeys(testPD)
valeurDonnees = []


for i in range(duration):
    date = date + timedelta(days=1)
    url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/dts_table_1?filter=record_date:gt:{},account_type:eq:Treasury%20General%20Account%20(TGA)%20Closing%20Balance".format(
        date.strftime("20%y-%m-%d")
    )
    response_API = requests.get(url)
    data = response_API.text
    parse_json = json.loads(data)
    global_data = parse_json["data"]
    valeurDonnees.append(global_data[0]["open_today_bal"])
    donneesFinales[testPD[i]] = global_data[0]["open_today_bal"]


donneesAExporte = pd.Series(donneesFinales)
donneesAExporte.to_csv("testOut.csv", index=True)
