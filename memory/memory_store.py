memory_db = {}

def save_memory(user_id, text):
    if user_id not in memory_db:
        memory_db[user_id] = []
    memory_db[user_id].append(text)

def get_memory(user_id):
    return "\n".join(memory_db.get(user_id, []))