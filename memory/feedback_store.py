feedback_db = []

def save_feedback(pergunta, resposta, avaliacao):
    feedback_db.append({
        "pergunta": pergunta,
        "resposta": resposta,
        "avaliacao": avaliacao
    })

def get_positive_feedbacks():
    return [f for f in feedback_db if f["avaliacao"] == "like"]