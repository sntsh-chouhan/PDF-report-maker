import json
from gpt_helper import points_about_element_in_factor_report

class HelperFunction():
    @classmethod
    def factor_helper(cls, user_id, factor, top_3_keys, user_report, meta_data):    
        top_3_interest = {}
        for i, key in enumerate(top_3_keys, start=1):
            gpt_data = points_about_element_in_factor_report(user_id, factor, key, user_report[key]["user_score"])

            if gpt_data is None:
                print("error at generating gpt data at user_id: ", user_id, f"factor: {factor} and at element: ", key)

            top_3_interest[str(i)] = {
                "name": key,
                "score": user_report[key]["user_score"],
                "avg_score" : user_report[key]["global_avg"],
                "small_text": meta_data.get(key, {}).get("small_text", ""),
                "big_text": meta_data.get(key, {}).get("big_text", ""),
                "people_like_you": meta_data.get(key, {}).get("people_like_you", ""),
                "job_for_you": meta_data.get(key, {}).get("job_for_you", ""),
                "small_image": meta_data.get(key, {}).get("small_image", ""),
                "big_image": meta_data.get(key, {}).get("big_image", ""),
                "key_desc": gpt_data["element_para"],
                "key_point": gpt_data["meaning_for_you"]
            }
        
        return top_3_interest

