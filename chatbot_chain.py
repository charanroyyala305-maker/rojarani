import json
import time
from ollama import Client

MODEL = "tinydolphin"
client = Client()

# 🔹 Load patient data
with open("patient_data.json", "r") as file:
    patient_data = json.load(file)


def get_condition(user_input):
    """Check if user input matches any known condition"""
    for condition, info in patient_data.items():
        if condition.lower() in user_input.lower():
            return {
                "condition": condition,
                "medicines": info.get("medicines", []),
                "dosage": info.get("dosage", ""),
                "storage": info.get("storage", ""),
                "advice": info.get("advice", "")
            }
    return None


def generate_ai_response(user_input):
    """Get an AI-generated health explanation and 3 short care tips"""
    start_time = time.time()
    prompt = f"""
    You are a friendly medical assistant.
    The user said: "{user_input}".
    Provide:
    1. A short explanation of the possible illness.
    2. 3 simple care or prevention tips in bullet points.
    """

    try:
        response = client.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a trusted AI health assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        end_time = time.time()
        elapsed = round(end_time - start_time, 2)

        # ✅ Safe content extraction
        if isinstance(response, dict):
            if "message" in response and isinstance(response["message"], dict):
                content = response["message"].get("content", "")
            elif "messages" in response:
                content = response["messages"][-1].get("content", "")
            else:
                content = str(response)
        else:
            content = str(response)

        return content, elapsed

    except Exception as e:
        return f"⚠ Error generating response: {e}", 0


if __name__ == "_main_":
    print(get_condition("I have fever"))