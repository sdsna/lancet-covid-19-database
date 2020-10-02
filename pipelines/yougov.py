import requests
import pandas
import demjson
from datetime import datetime
from time import gmtime, strftime

from helpers.normalize_date import normalize_date
from helpers.save_indicator import save_indicator
from helpers.normalize_country import normalize_country

# This request replicates the request made by the browser for the various
# charts displayed on the YouGov website.
url = "https://chartserver.live/server/yg/v4/data.js?x=987984"
request = requests.get(url)

# Convert the JS object contained in the response into a python dictionary
text = request.text
js_object = text[text.index("{") : text.rindex("}") + 1]
data_dict = demjson.decode(js_object)

# Map our indicator IDs to the title of the YouGov indicator
INDICATOR_MAP = {
    "fear_of_catching": "#1 YouGov COVID-19 tracker: fear of catching",
    "government_handling": "#2 YouGov COVID-19 tracker: government handling",
    "avoiding_crowded_places": "#3 YouGov COVID-19 behaviour changes tracker: Avoiding crowded public places",
    "wearing_mask_in_public": "#4 YouGov COVID-19 behaviour changes tracker: Wearing a face mask when in public places ",
    "avoiding_going_to_work": "#5 YouGov COVID-19 behaviour changes tracker: Avoiding going to work",
    "avoiding_raw_meat": "#6 YouGov COVID-19 behaviour changes tracker: Avoiding raw meat",
    "stopping_sending_children": "#7 YouGov COVID-19 behaviour changes tracker: Stopping sending children to child care or school",
    "improving_personal_hygiene": "#8 YouGov COVID-19 behaviour changes tracker: Improving personal hygiene",
    "refraining_from_touching_objects": "#9 YouGov COVID-19 behaviour changes tracker: Refraining from touching objects in public",
    "avoiding_contact_with_tourists": "#10 YouGov COVID-19 behaviour changes tracker: Avoiding physical contact with tourists",
    "support_stopping_flights_from_china": "#11 YouGov COVID-19 measures supported tracker: Stopping all flights coming into country from mainland China",
    "support_quarantine_flights_from_china": "#12 YouGov COVID-19 measures supported tracker: Quarantining all passengers on all flights coming into country from mainland China ",
    "support_stopping_international_flights": "#13 YouGov COVID-19 measures supported tracker: Stopping all inbound international flights from countries with confirmed cases of coronavirus",
    "support_quarantine_international_flights": "#14 YouGov COVID-19 measures supported tracker: Quarantining all inbound international flights from countries with confirmed cases of coronavirus",
    "support_quarantine_chinese_travellers": "#15 YouGov COVID-19 measures supported tracker: Quarantining all Chinese travellers currently in country",
    "support_quarantine_any_person": "#16 YouGov COVID-19 measures supported tracker: Quarantining anyone who has been in contact with a contaminated patient ",
    "support_quarantine_any_location": "#17 YouGov COVID-19 measures supported tracker: Quarantining any location in country that a contaminated patient has been in",
    "support_free_masks": "#18 YouGov COVID-19 measures supported tracker: Providing free masks for all people in country",
    "support_work_from_home": "#19 YouGov COVID-19 measures supported tracker: encourage working from home",
    "support_temporarily_close_schools": "#20 YouGov COVID-19 measures supported tracker: temporarily close schools",
    "support_cancel_large_events": "#21 YouGov COVID-19 measures supported tracker: cancel large events",
    "support_cancel_hospital_routines": "#22 YouGov COVID-19 measures supported tracker: cancel routine hospital procedures",
    "confidence_in_health_authorities": "#23 YouGov COVID-19 tracker: confidence in health authorities",
    "perceived_national_improvement": "#24 YouGov COVID-19 tracker: perceived national improvement",
    "perceived_global_improvement": "#25 YouGov COVID-19 tracker: perceived global improvement",
    "international_happiness": "#26 YouGov COVID-19 tracker: international happiness",
    # The following indicator is not shown on the YouGov website (#23 is shown
    # instead) and is thus not used:
    # 'confidence_in_health_authorities': '#27 YouGov COVID-19 tracker: confidence in health authorities',
    "personal_health_fears": "#28 YouGov COVID-19 tracker: personal health fears",
    "friends_and_family_health_fears": "#29 YouGov COVID-19 tracker: friends and family health fears",
    "finances_fears": "#30 YouGov COVID-19 tracker: finances fears",
    "job_loss_fears": "#31 YouGov COVID-19 tracker: job loss fears",
    "education_fears": "#32 YouGov COVID-19 tracker: education fears",
    "social_impact_fears": "#33 YouGov COVID-19 tracker: social impact fears",
    # The following two indicators are currently not being shown on the YouGov website
    # and are thus not used:
    # 'support_stopping_all_flights': '#34 YouGov COVID-19 measures supported tracker: stopping all inbound flights',
    # 'support_quarantine_all_flights': '#35 YouGov COVID-19 measures supported tracker: quarantining all inbound airline passengers',
}


def run_pipeline(indicator):
    # Find the chart series for this indicator
    chart_series = None
    # The YouGov label to look for
    needle = INDICATOR_MAP[indicator.replace("yougov_", "")]
    for id, object in data_dict.items():
        label = id.replace("chart_", "#") + " " + object["title"]
        if needle.lower() == label.lower():
            chart_series = object["chartSeries"]
            break

    # Convert the data in the dict into a pandas dataframe:
    # The series contains the country name and a data object
    # The data object is a list of data points in the format [timestamp, value]
    data = []
    for series in chart_series:
        for observation in series["data"]:
            data.append(
                {
                    "country": series["name"],
                    "date": strftime("%Y-%m-%d", gmtime(observation[0] / 1000)),
                    "value": observation[1],
                }
            )

    # Convert dict to dataframe
    dataset = pandas.DataFrame.from_dict(data)

    # Normalize countries
    dataset["iso_code"] = dataset["country"].apply(
        lambda country: normalize_country(country)
    )

    # Normalize date
    dataset["date"] = dataset["date"].apply(
        lambda date: normalize_date(date, "%Y-%m-%d")
    )

    # Rename the value column
    dataset = dataset.rename(columns={"value": indicator})

    # Create slice of data with country ID, date, and indicator
    dataset = dataset[["iso_code", "date", indicator]]

    save_indicator(indicator, dataset=dataset)
