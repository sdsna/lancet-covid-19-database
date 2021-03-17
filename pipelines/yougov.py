import requests
import pandas
from datetime import datetime
from time import gmtime, strftime

from helpers.normalize_date import normalize_date
from helpers.save_indicator import save_indicator
from helpers.normalize_country import normalize_country

# This is the Excel file with the data for the various YouGov charts
# Each tab contains one dataset
url = "https://docs.google.com/spreadsheets/export?id=1KukPUUcMVqQNDxW5qC-KSN2GyOG9xDovS_D5RQ8tq7E&exportFormat=xlsx"
request = requests.get(url)

# Map our indicator IDs to the title of the YouGov indicator
INDICATOR_MAP = {
    "fear_of_catching": "1 Fear",
    "government_handling": "2 Govt performance",
    "avoiding_crowded_places": "3 Avoid Public places",
    "wearing_mask_in_public": "4 Wear face mask",
    "avoiding_going_to_work": "5 Avoid work",
    "avoiding_raw_meat": "6 Avoid meat",
    "stopping_sending_children": "7 Stop school",
    "improving_personal_hygiene": "8 Improve hygiene",
    "refraining_from_touching_objects": "9 Avoid objects",
    "avoiding_contact_with_tourists": "10 Avoid tourists",
    "support_stopping_flights_from_china": "11 Stop all flights China",
    "support_quarantine_flights_from_china": "12 Quarantine All China",
    "support_stopping_international_flights": "13 Stop Inbound Flights",
    "support_quarantine_international_flights": "14 Quarantine Inbound Flights",
    "support_quarantine_chinese_travellers": "15 Quarantine Chinese traveller",
    "support_quarantine_any_person": "16 Quarantine Anyone",
    "support_quarantine_any_location": "17 Quarantine Any location",
    "support_free_masks": "18 Provide free masks",
    "support_work_from_home": "19 Working from home",
    "support_temporarily_close_schools": "20 Close schools",
    "support_cancel_large_events": "21 Cancel events",
    "support_cancel_hospital_routines": "22 Cancel hospital",
    "confidence_in_health_authorities": "23 Health Authorities",
    "perceived_national_improvement": "24 National Improvement",
    "perceived_global_improvement": "25 Global Improvement",
    "international_happiness": "26 Happiness",
    # The following indicator is not shown on the YouGov website (#23 is shown
    # instead) and is thus not used:
    # 'confidence_in_health_authorities': '#27 YouGov COVID-19 tracker: confidence in health authorities',
    "personal_health_fears": "28 Personal Health Fears",
    "friends_and_family_health_fears": "29 Friends Health Fears",
    "finances_fears": "30 Finance Fears",
    "job_loss_fears": "31 Job Loss Fears",
    "education_fears": "32 Education Fears",
    "social_impact_fears": "33 Social Impact Fears",
    # The following two indicators are currently not being shown on the YouGov website
    # and are thus not used:
    # 'support_stopping_all_flights': '#34 YouGov COVID-19 measures supported tracker: stopping all inbound flights',
    # 'support_quarantine_all_flights': '#35 YouGov COVID-19 measures supported tracker: quarantining all inbound airline passengers',
}


def run_pipeline(indicator):
    # The Excel sheet to use
    sheet = INDICATOR_MAP[indicator.replace("yougov_", "")]

    # Read dataframe
    dataset = pandas.read_excel(request.content, sheet_name=sheet, header=2)
    dataset = dataset.rename(columns={"Country/region": "country"})
    dataset = dataset.drop(columns=["region"])

    # Stack dates
    dataset = dataset.set_index("country")
    dataset = dataset.stack()
    dataset = dataset.reset_index()
    dataset = dataset.rename(columns={"level_1": "date", 0: "value"})

    # Normalize countries
    dataset["iso_code"] = dataset["country"].apply(
        lambda country: normalize_country(country)
    )

    # Normalize date
    # Drop any unnamed columns
    dataset["invalid_date"] = dataset["date"].apply(
        lambda date: type(date) == str and date.startswith("Unnamed")
    )
    dataset = dataset[dataset["invalid_date"] == False]
    dataset["date"] = dataset["date"].apply(
        lambda date: normalize_date(
            date if type(date) == str else date.strftime("%Y-%m-%d"), "%Y-%m-%d"
        )
    )

    # Rename the value column
    dataset = dataset.rename(columns={"value": indicator})

    # Create slice of data with country ID, date, and indicator
    dataset = dataset[["iso_code", "date", indicator]]

    save_indicator(indicator, dataset=dataset)
