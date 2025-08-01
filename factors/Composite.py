import os
import json

from renderer import prompt_all_pages_composite_report
from gpt_helper import streat_overview
from gpt_helper import stream_recomendation_depth_explanation
from gpt_helper import stream_intrest_alinment_explanation
from gpt_helper import subject_stream_analysis
from gpt_helper import get_report_summary
from gpt_helper import get_comparision_summary

from factors.helper import HelperFunction

def make_composite_component(user_id, user_detail, user_report):
    print("hello from Composite")
    with open("data/factor/Aptitude.json") as f:
        meta_data = json.load(f)

    with open("data/new_data.json") as f:
        data = json.load(f)

    # factor_list = [
    #     "Career_Interest",
    #     "Aptitude",
    #     "Personality",
    #     "Learning_Style",
    #     "Basic_Values",
    #     "Work_Style",
    #     "Emotional_Intelligence",
    # ]
    # common_report = HelperFunction.build_report(factor_list, "common", 2)
    # comperitive_bar_report = HelperFunction.build_report(factor_list, "comperitive_bar", 3)

    # cleaned_factor_data = HelperFunction.clean_factor_data(user_report["factors"])
    # print("Data cleaned for comparitive report")

    # print("getting data for summary on page 4")
    # report_summary = get_report_summary(user_id, cleaned_factor_data)

    # print("getting data for summary on page 6")
    # comparision_summary = get_comparision_summary(user_id, user_report["factors"])

    # stream_reccomendation = HelperFunction.stream_reccomendation_function(user_report["streams"], user_report["subjects"])

    # print("getting stream overview points")
    # stream_overview_text = streat_overview(user_id, stream_reccomendation)

    # print("getting subject_stream_analysis data")
    # subject_stream_analysis_data = subject_stream_analysis(user_id, stream_reccomendation, cleaned_factor_data)

    # data = {
    #     "page_1": {
    #         "index": "8",
    #         "model_part_1": "Stream",
    #         "model_part_2": "Recommendation",
    #         "Factor": "Initial Report",
    #         "description": """Initial Data Driven 7-Factor Model Analysis of Your Strengths and
    #                 Preferences for Tailored Stream Recommendations.""",
    #         "background_image": "images/cover/Aptitude.png",
    #         "factors": [
    #             "Interest",
    #             "Aptitude",
    #             "Personality",
    #             "Learning Styles",
    #             "Basic Values",
    #             "Work Style",
    #             "Emotional Intelligence",
    #             "Stream Recommendation",
    #         ],  # pass all factors in array only
    #         "user_detail": user_detail,
    #         "report" : "final"

    #     },
    #     "page_4" : {
    #         "title" : "2. Summary Report",
    #         "paragraph" : report_summary["one line summary"],
    #         "data" : common_report,
    #         "page_no." : "4",
    #         "page_display" : "3"

    #     },
    #     "page_5" : {
    #         "data" : {
    #             "head" : {
    #                 "title": "Overview",
    #                 "content" : report_summary["overview"]
    #             },
    #             "factor" : report_summary["factor"],
    #             "our_overview_of_you" : report_summary["our_overview_of_you"]
    #         },
    #         "page_no." : "5",
    #         "page_display" : "4"
    #     },
    #     "page_6" : {
    #         "title" : "2. Summary Report",
    #         "paragraph" : comparision_summary["one line summary"],
    #         "note" : """*Note: The average, minimum, and maximum scores are
    #                 computed based on global student data for this test.""",
    #         "data": comperitive_bar_report,
    #         "page_no.": "6",
    #         "page_display": "5",
    #     },
    #     "page_7" : {
    #         "data" : {
    #             "head" : {
    #                 "title": "Overview",
    #                 "content" : comparision_summary["Benchmarking Your Strengths"]
    #             },
    #             "factor" : comparision_summary["factor"],
    #             "our_overview_of_you" : comparision_summary["Our View of You"]
    #         },
    #         "page_no." : "7",
    #         "page_display" : "6",
    #     },
    #     "page_8" : {
    #         "data" : stream_reccomendation,
    #         "points" : stream_overview_text,
    #         "page_no." : "7",
    #         "page_display" : "8",
    #     },
    #     "page_9" : {
    #         "stream" : stream_reccomendation["1"]["stream"],
    #         "title" : "5. Subject and Stream Recommendation Analysis",
    #         "sub_title" : f"Stream Recommendation 1 & 2 : ",
    #         "top_image" : f"images/subjects/{stream_reccomendation['1']['stream']}.png",
    #         "meta_data" : [
    #             stream_reccomendation["1"],
    #             stream_reccomendation["2"]
    #         ],
    #         "data" : stream_recomendation_depth_explanation(user_id, {"1" : stream_reccomendation["1"] , "2" : stream_reccomendation["2"]}, cleaned_factor_data, "Best Suit", 9),
    #         "page_no." : "7",
    #         "page_display" : "9",
    #     },
    #     "page_10" : {
    #         "data" : stream_intrest_alinment_explanation(user_id, {'1' : stream_reccomendation['1'] , '2' : stream_reccomendation['2']}, cleaned_factor_data['Career Interest'], 10),
    #         "page_no.": "10",
    #         "page_display": "10"
    #     },
    #     "page_11":{
    #         "stream" : stream_reccomendation["3"]["stream"],
    #         "title" : "5. Subject and Stream Recommendation Analysis",
    #         "sub_title" : f"Stream Recommendation 3 : ",
    #         "top_image": f"images/subjects/{stream_reccomendation['3']['stream']}.png",
    #         "meta_data" : [
    #             stream_reccomendation["3"]
    #         ],
    #         "data" : stream_recomendation_depth_explanation(user_id, {"3" : stream_reccomendation["3"]}, cleaned_factor_data, "Can try", 11),
    #         "page_no." : "11",
    #         "page_display" : "11",
    #     },
    #     "page_12" : {
    #         "data" : stream_intrest_alinment_explanation(user_id, {"3" : stream_reccomendation["3"]}, cleaned_factor_data["Career Interest"], 12),
    #         "page_no." : "12",
    #         "page_display" : "12"
    #     },
    #     "page_13":{
    #         "stream" : stream_reccomendation["4"]["stream"],
    #         "title" : "5. Subject and Stream Recommendation Analysis",
    #         "sub_title" : f"Stream Recommendation 4 : ",
    #         "top_image": f"images/subjects/{stream_reccomendation['1']['stream']}.png",
    #         "meta_data" : [
    #             stream_reccomendation["4"]
    #         ],
    #         "data" : stream_recomendation_depth_explanation(user_id, {"4" : stream_reccomendation["4"]}, cleaned_factor_data, "Should Ignore", 13),
    #         "page_no." : "13",
    #         "page_display" : "13",
    #     },
    #     "page_14" : {
    #         "data" : stream_intrest_alinment_explanation(user_id, {"4" : stream_reccomendation["4"]}, cleaned_factor_data["Career Interest"], 14),
    #         "page_no." : "14",
    #         "page_display" : "14"
    #     },
    #     "page_15":{
    #         "heading" : "4. Subject and Stream Recommendation Analysis",
    #         "paragraph" : """Your stream recommendations are the outcome of a structured, evidence-based evaluation that
    #                 integrates multiple dimensions of your profile—aptitude scores, interest alignment, professional
    #                 values, emotional drivers, and preferred learning style. Each component was assigned a weight as
    #                 per our proprietary economic model, and their intersection revealed the most optimal academic
    #                 paths for you.
    #                 """,
    #         "points" : subject_stream_analysis_data["data"][:4],
    #         "page_no." : "14",
    #         "page_display" : "14"
    #     },
    #     "page_16":{
    #         "points": subject_stream_analysis_data["data"][4:],
    #         "table" : subject_stream_analysis_data["table"],
    #         "Conclusion" : subject_stream_analysis_data["Conclusion"],
    #         "page_no." : "15",
    #         "page_display" : "15"
    #     },
    #     "page_17" : {
    #         "heading": "Detailed Breakdown of Compatibility Scores for All Class 11 Subject Combinations",
    #         "paragraph": "This graph visualizes the compatibility scores for different subject combinations in Class 11, with scores ranging from the highest to the lowest. Each bar represents a combination, and the colors transition from green to red based on the score, providing an intuitive comparison of various streams and their alignment with student profiles",
    #         "image": "charts/Stream_Comparison/stream.png",
    #         "page_no." : "18",
    #         "page_display" : "17"
    #     }
    # }
    # print(f"\033[92m Data for page 9: \033[0m")
    # print(json.dumps(data["page_9"], indent= 2))
    # print(f"\033[92m Data for page 15: \033[0m")
    # print(json.dumps(data["page_15"], indent= 2))
    # print(f"\033[92m Data for page 16: \033[0m")
    # print(json.dumps(data["page_16"], indent= 2))
    # print(f"\033[92m Data: \033[0m")
    # print(json.dumps(data, indent= 2))

    with open("data/new_data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("hi from bellow")
    
    prompt_all_pages_composite_report(user_id, "Composite", data)
