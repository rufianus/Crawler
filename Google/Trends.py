
from Google.Cloud import MySQL
from pytrends.request import TrendReq
import numpy
import random
from datetime import datetime
import time


MySQL = MySQL("windows", "toraja", "asia-southeast1", "sql-toraja", "Delphi", "root", "RagnarTargaryen")


def group_every_5_searches(phrases_list_main, max_run):
    phrases_list_grouped = []
    request_ID = 0
    while request_ID < max_run:
        request_ID += 1
        if len(phrases_list_main) > 4:
            append_this = phrases_list_main[:4]
            append_this.insert(0, phrase_standard)
            phrases_list_grouped.append(append_this)
            del phrases_list_main[:4]
        elif len(phrases_list_main) <= 4:
            append_this = phrases_list_main
            append_this.insert(0, phrase_standard)
            phrases_list_grouped.append(append_this)
            break

    return phrases_list_grouped

username = "blembong"
password = "RagnarTargaryen"
access_type = "admin"
MySQL.Insert("gtrends_login", [username, password, access_type, datetime.now()],
           ["username", "password", "access_type", "record_creation_datetime"])

user_ID = 1
platform_source = "Shopee"
max_run = 1400
max_bulk_request_count = 20
minimum_standard_values_max_initial = 100
minimum_standard_values_max = 20
differential_data_span = 1
running_status = "QUEUEING"
running_scheduler_days = "NULL"
record_lastupdate_datetime = "NULL"

MySQL.Insert("gtrends_running_log",
           [user_ID, max_run, max_bulk_request_count, minimum_standard_values_max_initial, minimum_standard_values_max, differential_data_span,
            running_status, running_scheduler_days, datetime.now(), record_lastupdate_datetime],
           ["user_ID", "max_run", "max_bulk_request_count", "minimum_standard_values_max_initial", "minimum_standard_values_max",
            "differential_data_span", "running_status", "running_scheduler_days", "record_creation_datetime", "record_lastupdate_datetime"])


running_IDs_list = []
MySQL.Query_result = MySQL.Query("gtrends_running_log", ["running_ID"], "running_status = 'QUEUEING'")
for MySQL.Query_row in MySQL.Query_result: running_IDs_list.append(MySQL.Query_row.get("running_ID"))
running_ID = min(running_IDs_list)

MySQL.Update("gtrends_running_log",
           [["running_status", "RUNNING"], ["record_lastupdate_datetime", datetime.now()]],
           ("running_ID = " + str(running_ID)))

MySQL.Query_result = MySQL.Query("gtrends_running_log", ["*"], ("running_ID = " + str(running_ID)))
MySQL.Query_row = MySQL.Query_result[0]

max_run = MySQL.Query_row.get("max_run") # Protects Requests Limit
minimum_standard_values_max_initial = MySQL.Query_row.get("minimum_standard_values_max_initial")  # Minimum Mean Value of Standard
minimum_standard_values_max = MySQL.Query_row.get("minimum_standard_values_max")  # Minimum Mean Value of Standard
max_bulk_request_count = MySQL.Query_row.get("max_bulk_request_count")
differential_data_span = MySQL.Query_row.get("differential_data_span")


retry_reason = "NULL"
retry_state = True

for bulk_request_count in range(1, (max_bulk_request_count + 1)):
    print(bulk_request_count)
    try:

        with open("list_acara_tv_ns.txt", "r") as file:
            phrases_list_main = list(set(file.read().split("\n")))
        if "" in phrases_list_main: phrases_list_main.remove("")

        if retry_reason != "New Standard":
            random.shuffle(phrases_list_main)
            phrase_standard = phrases_list_main[0]

        pytrends = TrendReq(hl='en-US', tz=360)

        phrases_list_grouped = group_every_5_searches(phrases_list_main, max_run)

        candidate_standards = []

        request_ID = 0
        for phrases_list in phrases_list_grouped:
            if retry_state is True and request_ID != 0: break
            elif retry_state is False or request_ID == 0:
                request_ID += 1
                print("request_ID: ", request_ID, "|", phrases_list, "| retry_state: ", retry_state)

                try_count = 0
                skip_state = False
                while try_count < 2 and skip_state is False:
                    try_count += 1
                    try:
                        pytrends.build_payload(phrases_list, cat=0, timeframe='today 3-m', geo='ID', gprop='')
                        pytrends_data_frame = pytrends.interest_over_time()

                        phrase_index = 0

                        standard_values_list = []

                        for phrase in phrases_list:

                            print("phrase: ", phrase)

                            fetched_column = pytrends_data_frame[phrase]
                            values_list = fetched_column.values.tolist()

                            values_mean = numpy.mean(values_list)
                            if values_mean < 0.0001: values_mean = 0.0001

                            if phrase_index == 0:
                                standard_values_list = values_list
                                standard_values_max = max(standard_values_list)
                                if request_ID == 1:
                                    if standard_values_max >= minimum_standard_values_max_initial: retry_state = False
                                    elif standard_values_max < minimum_standard_values_max_initial:
                                        retry_state = True
                                        skip_state = True
                                        retry_reason = "minimum standard values max initial"
                                        retry_documentation = "Initiating retry due to: " + retry_reason
                                        print(retry_documentation)
                                        MySQL.Insert("gtrends_extracts",
                                                   [running_ID, bulk_request_count, retry_documentation, datetime.now()],
                                                   ["running_ID", "bulk_request_count", "phrase_standard", "record_creation_datetime"])
                                        break
                                elif request_ID > 1:
                                    if standard_values_max >= minimum_standard_values_max: retry_state = False
                                    elif standard_values_max < minimum_standard_values_max:
                                        retry_state = True
                                        skip_state = True
                                        retry_reason = "minimum standard values max"
                                        retry_documentation = "Initiating retry due to: " + retry_reason
                                        print(retry_documentation)
                                        MySQL.Insert("gtrends_extracts",
                                                   [running_ID, bulk_request_count, retry_documentation, datetime.now()],
                                                   ["running_ID", "bulk_request_count", "phrase_standard", "record_creation_datetime"])
                                        break

                            if 100 in values_list: phrase_has_100 = "YES"
                            elif 100 not in values_list: phrase_has_100 = "NO"

                            values_count = len(values_list)
                            value_index = 0
                            value_differentials_list = []
                            while value_index < (values_count - differential_data_span):
                                value_differential = values_list[value_index + differential_data_span] - values_list[value_index]
                                value_differentials_list.append(value_differential)
                                value_index += differential_data_span

                            index_list = []
                            value_ID = 0
                            for value in values_list:
                                value_ID += 1
                                index_list.append(value_ID)
                            linear_trend = numpy.polyfit(index_list, values_list, 1).tolist()
                            linear_trend_m = linear_trend[0]
                            linear_trend_c = linear_trend[1]

                            phrase_index += 1

                            if phrase_has_100 == "YES" and phrase != phrase_standard:
                                index_of_100 = values_list.index(100)
                                standard_max_value = max(standard_values_list)
                                standard_index_of_100 = standard_values_list.index(standard_max_value)
                                ratio = values_list[index_of_100] / standard_values_list[standard_index_of_100]
                                candidate_standards.append([phrase, ratio])

                            MySQL.Insert("gtrends_extracts",
                                       [running_ID, bulk_request_count, request_ID, phrase_standard, phrase, phrase_has_100, values_mean,
                                        linear_trend_m, linear_trend_c, datetime.now()],
                                       ["running_ID", "bulk_request_count", "request_ID", "phrase_standard", "phrase", "phrase_has_100",
                                        "values_mean", "linear_trend_m", "linear_trend_c", "record_creation_datetime"])

                            SQL_command = "SELECT MAX(extract_ID) FROM gtrends_extracts"
                            MySQL.Cursor.execute(SQL_command)
                            MySQL.Query_result = MySQL.Cursor.fetchone()
                            MySQL.Connection.commit()
                            extract_ID = MySQL.Query_result.get("MAX(extract_ID)")

                            for value in values_list:
                                MySQL.Insert("gtrends_extracts_values",
                                           [extract_ID, phrase, value, datetime.now()],
                                           ["extract_ID", "phrase", "value", "record_creation_datetime"])
                            for differential_value in value_differentials_list:
                                MySQL.Insert("gtrends_extracts_differential",
                                           [extract_ID, phrase, differential_value, datetime.now()],
                                           ["extract_ID", "phrase", "differential_value", "record_creation_datetime"])

                            if value_differentials_list != []:

                                differential_pattern_count = 1
                                differential_end_to_end_value = value_differentials_list[0]
                                last_differential_pattern_type = "NULL"
                                differential_pattern_type = "NULL"
                                next_differential_pattern_type = "NULL"

                                while value_differentials_list != []:

                                    if value_differentials_list[0] > 0: differential_pattern_type = "Incremental"
                                    elif value_differentials_list[0] < 0: differential_pattern_type = "Decremental"
                                    elif value_differentials_list[0] == 0: differential_pattern_type = "Flat"

                                    if differential_pattern_type == last_differential_pattern_type:
                                        differential_pattern_count += 1
                                        differential_end_to_end_value += value_differentials_list[0]
                                    elif differential_pattern_type != last_differential_pattern_type:
                                        differential_pattern_count = 1
                                        differential_end_to_end_value = value_differentials_list[0]

                                    value_differentials_list_count = len(value_differentials_list)
                                    if value_differentials_list_count > 1:
                                        if value_differentials_list[1] > 0: next_differential_pattern_type = "Incremental"
                                        elif value_differentials_list[1] < 0: next_differential_pattern_type = "Decremental"
                                        elif value_differentials_list[1] == 0: next_differential_pattern_type = "Flat"

                                    if value_differentials_list_count <= 1 or differential_pattern_type != next_differential_pattern_type:
                                        MySQL.Insert("gtrends_extracts_differential_pattern",
                                                   [extract_ID, phrase, differential_pattern_type, differential_pattern_count, differential_end_to_end_value, datetime.now()],
                                                   ["extract_ID", "phrase", "differential_pattern_type", "differential_pattern_count", "differential_end_to_end_value", "record_creation_datetime"])

                                    last_differential_pattern_type = differential_pattern_type
                                    del value_differentials_list[0]

                        break

                    except Exception as e:
                        print(e)
                        print("Failed: trying again ...")
                        retry_state = True
                        retry_reason = "inside loop error"
                        print("Initiating retry due to: " + retry_reason)
                        time.sleep(60)

        if candidate_standards != []:
            retry_state = True
            retry_reason = "New Standard"
            retry_documentation = "Initiating retry due to: " + retry_reason
            print(retry_documentation)
            MySQL.Insert("gtrends_extracts",
                       [running_ID, bulk_request_count, retry_documentation, datetime.now()],
                       ["running_ID", "bulk_request_count", "phrase_standard", "record_creation_datetime"])

            candidate_standards.sort(key=lambda candidate_list: float(candidate_list[1]), reverse=True)
            phrase_standard = candidate_standards[0][0]
        elif candidate_standards == [] and retry_state is not True: break

    except Exception as e:
        print("ERROR: ", e)
        if bulk_request_count < (max_bulk_request_count - 1): time.sleep(60)

MySQL.Update("gtrends_running_log",
           [["running_status", "RUNNING"], ["record_lastupdate_datetime", datetime.now()]],
           ("running_ID = " + str(running_ID)))
time.sleep(5)