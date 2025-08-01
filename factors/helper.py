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



    @classmethod
    def int_to_roman(cls, n: int) -> str:
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4, 1
        ]
        syms = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV", "I"
        ]
        roman = ''
        i = 0
        while n > 0:
            for _ in range(n // val[i]):
                roman += syms[i]
                n -= val[i]
            i += 1
        return roman

    @classmethod
    def build_report(cls, factor_list, image_type: str, base) -> list:
        report = []
        count = 1
        for factor in factor_list:
            data = {}

            if factor == "Career_Interest":
                factor_name = "Interest"
            else:
                factor_name = factor.replace("_", " ")
    
            roman_num = cls.int_to_roman(count)
            data["factor"] = f"{roman_num}. {factor_name}"
            data["path"] = f"charts/{factor}/{image_type}.png"
            data["footer"] = f"Exibit {base}.{count}"

            report.append(data)
            count += 1
        return report
    
    @classmethod
    def subject_acronyms(cls):
        SUBJECT_ACRONYMS = {
            "English": "En",
            "History": "Hi",
            "Philosophy": "Pl",
            "Political Science": "Po",
            "Fine Arts": "Fi",
            "Music": "Mu",
            "Home Science": "Ho",
            "Physical Education": "Pe",
            "Biology": "Bi",
            "Geography": "Ge",
            "Chemistry": "Ch",
            "Physics": "Ph",
            "Informatics Practices": "Ip",
            "Computer Science": "Cs",
            "Accountancy": "Ac",
            "Accounts": "Ac",
            "Business Studies": "Bs",
            "Mathematics": "Ma",
            "Maths": "Ma",
            "Economics": "Ec",
            "Legal Studies": "Le",
            "Sociology": "So",
            "Psychology": "Ps",
            "Hindi / Regional Language": "Hn"
        }
        return SUBJECT_ACRONYMS

    @classmethod
    def get_subject_mapped(cls, subjects):
        SUBJECT_ACRONYMS = cls.subject_acronyms()
        acronyms = [SUBJECT_ACRONYMS.get(subject) for subject in subjects if subject in SUBJECT_ACRONYMS]
        return "|".join(acronyms)


    @classmethod
    def map_subject_to_score(cls, subject_names, subject_score):
        data = {}
        for subject in subject_names:
            data[subject] = subject_score[subject]

        return data



    @classmethod
    def stream_reccomendation_function(cls, stream_data, subject_data):
        print("function is called")
        # print(json.dumps(stream_data, indent = 2))
        # print(json.dumps(subject_data, indent = 2))

        stream_scores = [
            ("Science", stream_data["Science"][0]["average_score"]),
            ("Commerce", stream_data["Commerce"][0]["average_score"]),
            ("Humanities", stream_data["Humanities"][0]["average_score"])
        ]

        # Sort streams by score in descending order
        ranked_streams = [stream for stream, _ in sorted(stream_scores, key=lambda x: x[1], reverse=True)]

        stream_reccomendation = {}

        stream_reccomendation["1"] = {
            "stream" : ranked_streams[0],
            "stream_score" : stream_data[ranked_streams[0]][0]["average_score"],
            "subject_mapping" : cls.get_subject_mapped(stream_data[ranked_streams[0]][0]["subjects"]),
            "recommendation_text" : "(Recommendation Stream - 1)",
            "subject_score" : cls.map_subject_to_score(stream_data[ranked_streams[0]][0]["subjects"], subject_data)
        }
        stream_reccomendation["2"] = {
            "stream" : ranked_streams[0],
            "stream_score" : stream_data[ranked_streams[0]][1]["average_score"],
            "subject_mapping" : cls.get_subject_mapped(stream_data[ranked_streams[0]][1]["subjects"]),
            "recommendation_text" : "(Recommendation Stream - 2)",
            "subject_score" : cls.map_subject_to_score(stream_data[ranked_streams[0]][1]["subjects"], subject_data)
        }
        stream_reccomendation["3"] = {
            "stream" : ranked_streams[1],
            "stream_score" : stream_data[ranked_streams[1]][0]["average_score"],
            "subject_mapping" : cls.get_subject_mapped(stream_data[ranked_streams[1]][0]["subjects"]),
            "recommendation_text" : "(Recommendation Stream - 3)",
            "subject_score" : cls.map_subject_to_score(stream_data[ranked_streams[1]][0]["subjects"], subject_data)
        }
        stream_reccomendation["4"] = {
            "stream" : ranked_streams[2],
            "stream_score" : stream_data[ranked_streams[2]][1]["average_score"],
            "subject_mapping" : cls.get_subject_mapped(stream_data[ranked_streams[2]][1]["subjects"]),
            "recommendation_text" : "(Challenging - Will need more work)",
            "subject_score" : cls.map_subject_to_score(stream_data[ranked_streams[2]][1]["subjects"], subject_data)
        }

        return stream_reccomendation
        
        
        # print(json.dumps(stream_reccomendation, indent = 2))

    @classmethod
    def clean_factor_data(cls, factors):
        result = {}
        for factor_name, traits in factors.items():
            trait_scores = {}
            for trait, scores in traits.items():
                if "user_score" in scores:
                    trait_scores[trait] = scores["user_score"]
            result[factor_name] = trait_scores
        return result