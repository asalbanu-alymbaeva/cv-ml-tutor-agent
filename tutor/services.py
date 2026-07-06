import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def call_agent(system_prompt, user_message):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=800,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"AI xizmatida xatolik yuz berdi: {e}")


# --- AGENT 1: topic-planner ---
PLANNER_PROMPT = """
Sen Computer Vision va Machine Learning bo'yicha kontent rejalashtiruvchi mutaxassissan.
Talaba savolini tahlil qil va quyidagilarni aniqla:
1. Mavzu va kichik mavzu (masalan: CNN > pooling layer)
2. Talabaning bilim darajasi (savoldan taxmin qil: boshlang'ich/o'rta)
3. Tushuntirish uchun 2-3 ta kalit nuqta
Natijani qisqa, tuzilgan formatda ber (oddiy matn ro'yxat, JSON emas).
"""

# --- AGENT 2: tutor-explainer ---
EXPLAINER_PROMPT = """
Sen tajribali Computer Vision/ML o'qituvchisan.
Senga savol va reja berilgan. Shu reja asosida:
1. Tushunchani sodda tilda, real misol bilan tushuntir
2. Agar mos bo'lsa, kichik analogiya ishlat
3. 150-200 so'z atrofida yoz, haddan tashqari uzun yozma
"""

# --- AGENT 3: quiz-reviewer ---
REVIEWER_PROMPT = """
Sen sifat nazoratchi muharrirsan.
Senga tayyor tushuntirish berilgan. Vazifang:
1. Texnik xatoliklarni tuzat
2. Ortiqcha murakkab qismlarni soddalashtir
3. Oxiriga aynan shu mavzu bo'yicha 1 ta tekshiruv savoli (mini-quiz) qo'sh
Natijani nashrga tayyor holda, Markdown formatida qaytar.
"""


def get_tutor_response(user_question):
    plan = call_agent(PLANNER_PROMPT, user_question)
    draft = call_agent(EXPLAINER_PROMPT, f"Savol: {user_question}\n\nReja:\n{plan}")
    final = call_agent(REVIEWER_PROMPT, draft)
    return {"plan": plan, "draft": draft, "final": final}