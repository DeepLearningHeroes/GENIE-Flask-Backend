from sense2vec import Sense2Vec
from utils import text_cleaner


def skill_finder(model, text):
    try:
        doc = model(text)
        doc = doc.ents
        skills = []
        for ent in doc:
            label = ent.label_
            if label == "Skills":
                skills.append(ent.text)
        return list(set(skills))
    except Exception as error:
        return error


def get_final_keywords(keywords, semantic_keywords):
    if len(semantic_keywords) == 0:
        return keywords
    for keyword in semantic_keywords:
        try:
            keywords.append(keyword)
        except Exception as error:
            print(error)
    return keywords


def get_semantically_related_keywords(keywords, similar_terms_per_keyword=5, semantically_related_keywords_count=5):
    try:
        keyword_mapping = dict()
        s2v = Sense2Vec().from_disk("C:\models\s2v")
        for keyword in keywords:
            try:
                most_similar = s2v.most_similar(
                    f"{keyword}|NOUN", n=similar_terms_per_keyword)
                if len(most_similar) == 0:
                    continue
                for similar in most_similar:
                    similar = (similar[0].split('|'))[0]
                    print(similar)
                    if similar in keywords:
                        continue

                    if len(keyword_mapping) == 0:
                        keyword_mapping[f"{similar}"] = 1

                    if len(keyword_mapping) != 0 and similar in keyword_mapping:
                        keyword_mapping[f"{similar}"] += 1

                    if len(keyword_mapping) != 0 and similar not in keyword_mapping:
                        keyword_mapping[f"{similar}"] = 1

            except Exception as error:
                print(error)
    except Exception as error:
        return {"error": str(error)}
    if len(keyword_mapping) == 0:
        return []
    sorted_keyword_mapping = {k: v for k, v in sorted(
        keyword_mapping.items(), reverse=True)}
    # remove this comment if u want to restrict the length of keywords returned
    # semantically_related_keywords = list(sorted_keyword_mapping.keys())[0:min(len(sorted_keyword_mapping),semantically_related_keywords_count)]
    semantically_related_keywords = list(set(sorted_keyword_mapping.keys()))
    for index in range(len(semantically_related_keywords)):
        semantically_related_keywords[index] = text_cleaner.cleanText(
            semantically_related_keywords[index])

    return semantically_related_keywords
