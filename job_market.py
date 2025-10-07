# import pandas as pd
# from pathlib import Path

# DATA_PATH = Path(__file__).parent / 'data' / 'job_market_skills.csv'

# def get_high_demand_skills():
#     df = pd.read_csv(DATA_PATH)
#     return df[df['demand_level'] == 'High']['skill'].tolist()
# job_market.py
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# تحميل مفاتيح API
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def get_high_demand_skills(country="us", keyword="software engineer", results_limit=15):
    """
    🔹 جلب المهارات المطلوبة من سوق العمل الحقيقي باستخدام Adzuna API
    """
    base_url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_limit,
        "what": keyword,
        "content-type": "application/json"
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"[Adzuna] ❌ فشل الاتصال بالكود: {response.status_code}")
            return []

        data = response.json()
        jobs = data.get("results", [])

        if not jobs:
            print("[Adzuna] ⚠️ لا توجد وظائف مطابقة.")
            return []

        descriptions = [job.get("description", "") for job in jobs]
        combined_text = " ".join(descriptions)

        print(f"[Adzuna] ✅ تم جلب {len(jobs)} وظيفة من سوق العمل ({country.upper()})")

        # تحليل النصوص لاستخراج المهارات المطلوبة
        return extract_skills_from_text(combined_text)

    except Exception as e:
        print(f"[Adzuna] ⚠️ خطأ أثناء جلب البيانات: {e}")
        return []


def extract_skills_from_text(job_descriptions_text):
    """
    🔹 تحليل نصوص الوظائف واستخراج المهارات باستخدام GPT
    """
    prompt = f"""
    Analyze the following job descriptions and list the top 15 most in-demand skills required for these jobs.
    Return only a valid Python list of skill names.

    Job Descriptions:
    {job_descriptions_text[:5000]}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    skills_text = response.choices[0].message.content.strip()
    try:
        skills_list = eval(skills_text)
        if isinstance(skills_list, list):
            return skills_list
        else:
            return [skills_text]
    except Exception:
        return [skills_text]


# # 🔹 fallback في حال فشل Adzuna
# def get_default_skills():
#     return [
#         "Python", "SQL", "Machine Learning", "Data Analysis",
#         "Communication", "Cloud Computing", "Problem Solving",
#         "Project Management", "APIs", "Teamwork"
#     ]


def get_skills(keyword="software engineer", country="us"):
    """
    🔹 واجهة موحدة تُرجع المهارات سواء من Adzuna أو قائمة افتراضية
    """
    print(f"\n🔍 البحث عن المهارات المطلوبة لـ '{keyword}' في سوق عمل {country.upper()}...")
    skills = get_high_demand_skills(country, keyword)
    if not skills:
        print("⚠️ لم يتم العثور على نتائج في Adzuna.")
        # skills = get_default_skills()

    print(f"✅ المهارات النهائية: {skills}")
    return skills


# ✅ للاختبار المحلي
if __name__ == "__main__":
    get_skills(keyword="AI", country="us")
