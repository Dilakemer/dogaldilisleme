import difflib
import json
import os
def find_similar_question(user_question: str, questions_list: list, threshold=0.6):
    user_question = user_question.lower()
    best_match = None
    highest_ratio = 0

    for q in questions_list:
        ratio = difflib.SequenceMatcher(None, user_question, q.lower()).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = q

    if highest_ratio >= threshold:
        return best_match, highest_ratio
    return None, 0

def load_questions():
    path = os.path.join(os.path.dirname(__file__), '../data/questions.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)