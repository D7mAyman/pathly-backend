
# skills_generator.py
import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# -------------------------------------------
# 🔑 تحميل مفاتيح البيئة
# -------------------------------------------
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# -------------------------------------------
# 🔹 1. جلب أوصاف الوظائف من Adzuna
# -------------------------------------------
def get_job_descriptions(career_goal: str, country="us"):
    """
    جلب أوصاف الوظائف من Adzuna بناءً على الهدف المهني
    """
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": career_goal,
        "results_per_page": 10,
        "content-type": "application/json"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"[Adzuna] ❌ فشل في الاتصال (الكود: {response.status_code})")
            return []

        data = response.json()
        results = data.get("results", [])
        print(f"[Adzuna] ✅ تم جلب {len(results)} وظيفة من سوق العمل ({country.upper()})")

        return [r.get("description", "") for r in results if r.get("description")]
    except Exception as e:
        print(f"[Adzuna] ⚠️ خطأ أثناء الجلب: {e}")
        return []

# -------------------------------------------
# 🔹 2. تحليل النصوص واستخراج المهارات عبر GPT
# -------------------------------------------
def extract_skills_from_text(job_descriptions):
    combined_text = " ".join(job_descriptions)
    prompt = f"""
    Analyze the following real job descriptions and extract the most in-demand skills.
    Return ONLY a valid JSON with 3 categories:
    {{
      "foundation": ["skill1", "skill2"],
      "core": ["skill1", "skill2"],
      "advanced": ["skill1", "skill2"]
    }}

    Job Descriptions:
    {combined_text[:5000]}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    try:
        clean = response.choices[0].message.content.strip()
        clean = clean.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception as e:
        print("⚠️ خطأ في تحليل استجابة GPT:", e)
        return {"foundation": [], "core": [], "advanced": []}

# -------------------------------------------
# 🔹 3. توليد المهارات بناءً على تخصص المستخدم وهدفه
# -------------------------------------------
def generate_required_skills(specialization: str, career_goal: str):
    prompt = f"""
    You are an expert career advisor.
    Based on the following information, generate a list of essential skills:

    Specialization: {specialization}
    Career Goal: {career_goal}

    👉 Return the skills grouped into 3 categories:
    - Foundation Skills
    - Core Skills
    - Advanced / Specialized Skills

    ⚠️ IMPORTANT: Return valid JSON only:
    {{
      "foundation": ["skill1", "skill2"],
      "core": ["skill1", "skill2"],
      "advanced": ["skill1", "skill2"]
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=400,
    )

    try:
        clean = response.choices[0].message.content.strip()
        clean = clean.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception:
        return {"foundation": [], "core": [], "advanced": []}

# -------------------------------------------
# 🔹 4. دمج المهارات من Adzuna و GPT
# -------------------------------------------
def generate_combined_skills(specialization: str, career_goal: str, country="us"):
    """
    يجمع بين تحليل سوق العمل (Adzuna) والتحليل الذكي من GPT
    لإنتاج مهارات دقيقة ومخصصة للمستخدم.
    """
    print(f"\n🔍 تحليل سوق العمل لمجال: {career_goal}")

    # المهارات من سوق العمل
    job_descriptions = get_job_descriptions(career_goal, country)
    if job_descriptions:
        market_skills = extract_skills_from_text(job_descriptions)
    else:
        market_skills = {"foundation": [], "core": [], "advanced": []}

    # المهارات من GPT حسب التخصص
    ai_skills = generate_required_skills(specialization, career_goal)

    # دمج النتيجتين بدون تكرار
    combined = {
        "foundation": list(set(ai_skills["foundation"] + market_skills["foundation"])),
        "core": list(set(ai_skills["core"] + market_skills["core"])),
        "advanced": list(set(ai_skills["advanced"] + market_skills["advanced"]))
    }

    return combined

# -------------------------------------------
# 🔹 5. اختبار محلي (اختياري)
# -------------------------------------------
if __name__ == "__main__":
    result = generate_combined_skills("Computer Science", "Data Scientist")
    print("\n🧠 المهارات النهائية:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


#-----------------5-------------

# #skills_generator.py
# import os
# import json
# import requests
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# # تحميل المفاتيح من ملف .env
# ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
# ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# client = OpenAI(api_key=OPENAI_API_KEY)

# # -------------------------------------------
# # 🔹 جلب بيانات سوق العمل من Adzuna
# # -------------------------------------------
# def get_job_descriptions(career_goal: str, country="us"):
#     """
#     جلب أوصاف الوظائف من Adzuna بناءً على الهدف المهني
#     """
#     url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
#     params = {
#         "app_id": ADZUNA_APP_ID,
#         "app_key": ADZUNA_APP_KEY,
#         "what": career_goal,
#         "results_per_page": 10,
#         "content-type": "application/json"
#     }

#     try:
#         response = requests.get(url, params=params)
#         if response.status_code != 200:
#             print(f"[Adzuna] ❌ فشل في الاتصال (الكود: {response.status_code})")
#             return []

#         data = response.json()
#         results = data.get("results", [])
#         print(f"[Adzuna] ✅ تم جلب {len(results)} وظيفة من سوق العمل ({country.upper()})")

#         return [r.get("description", "") for r in results if r.get("description")]
#     except Exception as e:
#         print(f"[Adzuna] ⚠️ خطأ أثناء الجلب: {e}")
#         return []


# # -------------------------------------------
# # 🔹 تحليل النصوص واستخراج المهارات عبر GPT
# # -------------------------------------------
# def extract_skills_from_text(job_descriptions):
#     combined_text = " ".join(job_descriptions)
#     prompt = f"""
#     Analyze the following real job descriptions and extract the most in-demand skills.
#     Return ONLY a valid JSON with 3 categories:
#     {{
#       "foundation": ["skill1", "skill2"],
#       "core": ["skill1", "skill2"],
#       "advanced": ["skill1", "skill2"]
#     }}

#     Job Descriptions:
#     {combined_text[:5000]}
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.3,
#     )

#     try:
#         clean = response.choices[0].message.content.strip()
#         clean = clean.replace("```json", "").replace("```", "").strip()
#         return json.loads(clean)
#     except Exception as e:
#         print("⚠️ خطأ في تحليل استجابة GPT:", e)
#         return {
#             "foundation": [],
#             "core": [],
#             "advanced": []
#         }


# # -------------------------------------------
# # 🔹 دالة رئيسية تولد المهارات المطلوبة
# # -------------------------------------------
# def     (specialization: str, career_goal: str, country="us"):
#     """
#     الدالة الرئيسية: تجلب أوصاف الوظائف من Adzuna ثم تولد المهارات المطلوبة فعلاً.
#     """
#     print(f"\n🔍 تحليل سوق العمل لمجال: {career_goal}")
#     job_descriptions = get_job_descriptions(career_goal, country)

#     if not job_descriptions:
#         print("⚠️ لم يتم العثور على بيانات حقيقية. سيتم استخدام مجموعة افتراضية.")
#         return {
#             "foundation": ["Communication", "Teamwork", "Problem Solving"],
#             "core": ["Python", "SQL", "Machine Learning"],
#             "advanced": ["Deep Learning", "MLOps", "Cloud AI"]
#         }

#     return extract_skills_from_text(job_descriptions)


# # -------------------------------------------
# # ✅ للتجربة المحلية
# # -------------------------------------------
# if __name__ == "__main__":
#     result = generate_required_skills("Computer Science", "Data Scientist", country="us")
#     print("\n✅ المهارات المقترحة:\n", json.dumps(result, indent=2, ensure_ascii=False))

#--------------------------------4----------
# import os
# import requests
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# # تحميل المفاتيح من ملف .env
# ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
# ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# client = OpenAI(api_key=OPENAI_API_KEY)

# def get_high_demand_skills(country="us", keyword="software engineer", results_limit=10):
#     """
#     جلب المهارات المطلوبة من سوق العمل الحقيقي باستخدام Adzuna API
#     """
#     base_url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
#     params = {
#         "app_id": ADZUNA_APP_ID,
#         "app_key": ADZUNA_APP_KEY,
#         "results_per_page": results_limit,
#         "what": keyword,
#         "content-type": "application/json"
#     }

#     try:
#         response = requests.get(base_url, params=params)
#         if response.status_code != 200:
#             print(f"[Adzuna] ❌ فشل في الاتصال. الكود: {response.status_code}")
#             return []

#         data = response.json()
#         jobs = data.get("results", [])

#         if not jobs:
#             print("[Adzuna] ⚠️ لا توجد وظائف مطابقة.")
#             return []

#         descriptions = [job.get("description", "") for job in jobs]
#         combined_text = " ".join(descriptions)

#         print(f"[Adzuna] ✅ تم جلب {len(jobs)} وظيفة من سوق العمل ({country.upper()})")

#         # تمرير النص إلى GPT لتحليل المهارات
#         return extract_skills_from_text(combined_text)

#     except Exception as e:
#         print(f"[Adzuna] ⚠️ خطأ أثناء جلب البيانات: {e}")
#         return []

# def extract_skills_from_text(job_descriptions_text):
#     """
#     تحليل النصوص الوصفية للوظائف واستخراج المهارات المطلوبة باستخدام GPT
#     """
#     prompt = f"""
#     Analyze the following job descriptions and list the top 10 most in-demand skills required for these jobs.
#     Provide the answer as a simple Python list of skills only.

#     Job Descriptions:
#     {job_descriptions_text[:5000]}  # نحد النص لتجنب الطول الزائد
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.3
#     )

#     skills_text = response.choices[0].message.content.strip()
#     try:
#         skills_list = eval(skills_text)
#         if isinstance(skills_list, list):
#             return skills_list
#         else:
#             return [skills_text]
#     except:
#         return [skills_text]


# # 🔹 Fallback بسيط في حال فشل Adzuna
# def get_default_skills():
#     return [
#         "Python", "SQL", "Machine Learning", "Communication",
#         "Teamwork", "Data Analysis", "Cloud Computing",
#         "Problem Solving", "Project Management", "APIs"
#     ]


# def get_skills(keyword="software engineer", country="us"):
#     """
#     الواجهة النهائية: تستخدم Adzuna أولاً، وإذا فشل الاتصال أو لم توجد نتائج، تستخدم المهارات الافتراضية.
#     """
#     print(f"\n🔍 البحث عن المهارات المطلوبة لـ '{keyword}' في سوق عمل {country.upper()}...")
#     skills = get_high_demand_skills(country, keyword)
#     if not skills:
#         print("⚠️ لم يتم العثور على نتائج في Adzuna. سيتم استخدام مهارات افتراضية.")
#         skills = get_default_skills()

#     print(f"✅ المهارات النهائية: {skills}")
#     return skills


# # ✅ للتجربة المباشرة
# if __name__ == "__main__":
#     get_skills(keyword="data scientist", country="us")


# -------الاسااااسسسيي---------------------------------------3----
# skills_generator.py

# import os
# import json
# import requests
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
# ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")


# def get_job_descriptions(career_goal: str, country="us"):
#     """جلب بيانات الوظائف من Adzuna API"""
#     url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
#     params = {
#         "app_id": ADZUNA_APP_ID,
#         "app_key": ADZUNA_APP_KEY,
#         "what": career_goal,
#         "results_per_page": 10,
#         "content-type": "application/json"
#     }
#     response = requests.get(url, params=params)
#     # print("🔍 Adzuna raw response:", response.status_code, response.text[:500])
#     data = response.json()
#     results = data.get("results", [])
#     return [r.get("description", "") for r in results if r.get("description")]


# def generate_required_skills(specialization: str, career_goal: str):
#     """تحليل سوق العمل + توليد المهارات المطلوبة فعلاً"""
#     job_descriptions = get_job_descriptions(career_goal)

#     if job_descriptions:
#         joined_desc = "\n\n".join(job_descriptions[:5])
#         job_data_section = f"### Real job descriptions for {career_goal}:\n{joined_desc}"
#     else:
#         job_data_section = "No real job data found. Use general knowledge instead."

#     prompt = f"""
#     You are an expert AI career advisor.

#     Based on the specialization and career goal below,
#     analyze the real job descriptions (if provided)
#     and generate a list of **essential and trending skills** required.

#     Specialization: {specialization}
#     Career Goal: {career_goal}

#     {job_data_section}

#     Group the results into 3 categories:
#     - Foundation Skills
#     - Core Skills
#     - Advanced / Specialized Skills

#     ⚠️ Return ONLY valid JSON in this format:
#     {{
#       "foundation": ["skill1", "skill2"],
#       "core": ["skill1", "skill2"],
#       "advanced": ["skill1", "skill2"]
#     }}
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.3,
#         max_tokens=500,
#     )

#     try:
#         clean = response.choices[0].message.content.strip()
#         clean = clean.replace("```json", "").replace("```", "").strip()
#         return json.loads(clean)
#     except Exception as e:
#         print("Error parsing GPT response:", e)
#         return {
#             "foundation": [],
#             "core": [],
#             "advanced": []
#         }


#------------------2----------------

# import os
# import json
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def generate_required_skills(specialization: str, career_goal: str):
#     prompt = f"""
#     You are an expert career advisor.
#     Based on the following information, generate a list of essential skills:

#     Specialization: {specialization}
#     Career Goal: {career_goal}

#     👉 Return the skills grouped into 3 categories:
#     - Foundation Skills
#     - Core Skills
#     - Advanced / Specialized Skills

#     ⚠️ IMPORTANT: Return valid JSON only:
#     {{
#       "foundation": ["skill1", "skill2"],
#       "core": ["skill1", "skill2"],
#       "advanced": ["skill1", "skill2"]
#     }}
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.3,
#         max_tokens=400,
#     )

#     try:
#         return json.loads(response.choices[0].message.content)
#     except Exception:
#         return {
#             "foundation": [],
#             "core": [],
#             "advanced": []
#         }
