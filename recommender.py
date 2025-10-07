# recommender.py
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from job_market import get_high_demand_skills  # optional

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in .env")

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_learning_path(user_data: dict, courses: list):
    course_list = "\n".join([
        f"- {c['title']} ({c['url']}) ⭐ {c.get('rating', 'N/A')} | image: {c.get('image', '')}"
        for c in courses
    ])

    try:
        high_demand = get_high_demand_skills(keyword=user_data.get("career_goal"))
    except Exception:
        high_demand = []

    prompt = f"""
    You are an AI assistant specialized in creating **personalized learning paths**.
    Analyze the user profile and course data, then generate a **structured roadmap**.

    ## User Profile
    - College: {user_data.get('college')}
    - Department: {user_data.get('department')}
    - Major: {user_data.get('major')}
    - skills the user already knows: {user_data.get('skills')}
    - Career Goal: {user_data.get('career_goal')}

    ## Market Insight
    High-demand skills in the current job market:
    {high_demand}

    ## Available Courses
    {course_list}

    ## Task
    1. Select the most relevant courses based on career goal + missing skills + market demand.
    2. Avoid suggesting skills the user already knows.
    3. Arrange courses by difficulty (Beginner → Intermediate → Advanced).
    4. For each course, explain briefly why it’s important for the user.
    5. If duration info is missing, estimate based on level (e.g. 3h beginner, 6h intermediate, 10h advanced).

    ## Output format (return **valid JSON only**)
    [
      {{
        "step": 1,
        "title": "Course title",
        "url": "Course link",
        "duration": "X hours",
        "notes": "Why this course is useful",
        "image": "thumbnail"
      }}
    ]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1500
        )
        # نحاول نحلل JSON بشكل آمن
        return response.choices[0].message.content

    except json.JSONDecodeError:
        print("⚠️ Warning: GPT output is not valid JSON.")
        return []
    except Exception as e:
        print("Error generating learning path:", str(e))
        return []

# ---------------------------2----------------------
# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from job_market import get_high_demand_skills  # optional

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# if not OPENAI_API_KEY:
#     raise RuntimeError("OPENAI_API_KEY not set in .env")

# client = OpenAI(api_key=OPENAI_API_KEY)

# def generate_learning_path(user_data: dict, courses: list):
#     course_list = "\n".join([
#         f"- {c['title']} ({c['url']}) ⭐ {c.get('rating', 'N/A')} | image: {c.get('image', '')}"
#         for c in courses
#     ])

#     try:
#         high_demand = get_high_demand_skills()
#     except Exception:
#         high_demand = []

#     prompt = f"""
#     You are an AI assistant specialized in building **personalized learning paths** for students and professionals.
#     Analyze the user profile and available courses, then generate a **step-by-step roadmap**.

#     ## User Profile
#     - College: {user_data.get('college')}
#     - Department: {user_data.get('department')}
#     - Major: {user_data.get('major')}
#     - Current Skills: {user_data.get('skills')}
#     - Career Goal: {user_data.get('career_goal')}

#     ## Available Courses
#     {course_list}

#     ## Task
#     1. Select the most relevant courses based on career goal + skills gap + high demand skills.
#     2. Build a progressive learning path (Beginner → Intermediate → Advanced).
#     3. Explain briefly why each course is chosen.

#     ## Output Instructions
#     Return **ONLY valid JSON array**. Example:
#     [
#       {{
#         "step": 1,
#         "title": "Course title",
#         "url": "link",
#         "duration": "X hours",
#         "notes": "why important",
#         "image": "thumbnail"
#       }}
#     ]
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.5,
#         max_tokens=900
#     )

#     return response.choices[0].message.content



#-----------------------------------------------1----------------
# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from job_market import get_high_demand_skills  # إذا بتستعمل بيانات سوق العمل

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# if not OPENAI_API_KEY:
#     raise RuntimeError("OPENAI_API_KEY not set in .env")

# client = OpenAI(api_key=OPENAI_API_KEY)  # نمرر المفتاح هنا

# def generate_learning_path(user_data: dict, courses: list):
#     course_list = "\n".join([
#         f"- {c['title']} ({c['url']}) ⭐ {c.get('rating', 'N/A')} | image: {c.get('image', '')}"
#         for c in courses
#     ])

#     try:
#         high_demand = get_high_demand_skills()
#     except Exception:
#         high_demand = []



#     prompt = f"""
#     You are an AI assistant specialized in creating **personalized learning paths**. 
#     Unlike generic paths, you must **start from the user’s current skill level** and avoid repeating what the user already knows.

#     ---

#     ## User Profile
#     - College: {user_data.get('college')}
#     - Department: {user_data.get('department')}
#     - Major: {user_data.get('major')}
#     - Current Skills (baseline knowledge): {user_data.get('skills')}
#     - Interests: {user_data.get('interests')}
#     - Career Goal: {user_data.get('career_goal')}

#     ---

#     ## Available Courses
#     {course_list}

#     ---

#     ## Task
#     1. Select only the **most relevant courses** from the list:  
#     - Start from the **next level above the user’s current skills** (skip beginner content if user already has those skills).  
#     - Prioritize alignment with **career goal** and **skills gap**.  
#     - Cover **in-demand skills** for the target career.  
#     - Exclude duplicate, redundant, or irrelevant courses.  

#     2. Build a **step-by-step roadmap**:  
#     - Order courses progressively: from **the user’s current level → advanced level**.  
#     - Each step = exactly one course.  
#     - Ensure logical sequencing and practical progression toward the career goal.  

#     3. For each step, explain briefly why this course is chosen and how it helps the user move forward.  

#     ---

#     ## Output Instructions
#     Return the result as **ONLY a valid JSON array** (no extra text).
#     Each item must include:
#     - step (integer, sequence number)  
#     - title (string, course name)  
#     - url (string, course link if available)  
#     - duration (string, e.g., "6 weeks", "10 hours")  
#     - notes (string, reason why this course is important, focusing on progression beyond current skills)  
#     - image (string, course thumbnail if available)

#     ---
#     """

#     # استدعاء GPT
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.6,   # ضبط أقل عشان يكون منطقي أكثر
#         max_tokens=900
#     )

#     return response.choices[0].message.content


    # prompt = f"""
    # You are an AI assistant specialized in building **personalized learning paths** for students and professionals. 
    # Your goal is to analyze the user profile and the available course list, then generate a **step-by-step roadmap** that bridges the gap between current skills and the career goal.

    # ---

    # ## User Profile
    # - College: {user_data.get('college')}
    # - Department: {user_data.get('department')}
    # - Major: {user_data.get('major')}
    # - Current Skills: {user_data.get('skills')}
    # - Interests: {user_data.get('interests')}
    # - Career Goal: {user_data.get('career_goal')}

    # ---

    # ## Available Courses
    # {course_list}

    # ---

    # ## Task
    # 1. Select the **most relevant courses** from the provided list.  
    # - Highest priority: alignment with **career goal**.  
    # - Next priority: filling **skills gap**.  
    # - Then: covering **in-demand market skills**.  
    # - Exclude redundant, duplicate, or irrelevant courses.  

    # 2. Build a **progressive learning path**:  
    # - Order courses from **Beginner → Intermediate → Advanced**.  
    # - Each step = one course only.  
    # - Ensure logical sequencing and practical progression.  

    # 3. For each step, provide useful notes such as why the course is chosen, how it connects to the previous step, and how it helps achieve the career goal.

    # ---

    # ## Output Instructions
    # Return the result as **ONLY a valid JSON array** (no extra text).
    # Each item in the array must include the following fields:

    # - step (integer, sequence number)  
    # - title (string, course name)  
    # - url (string, course link if available)  
    # - duration (string, e.g., "6 weeks", "10 hours")  
    # - notes (string, short explanation of why this course is important)  
    # - image (string, course thumbnail if available)

    # ---
    # """


    # prompt = f"""
    # You are an AI assistant that builds personalized learning paths for students.

    # ## User Profile
    # - College: {user_data.get('college')}
    # - Department: {user_data.get('department')}
    # - major: {user_data.get('major')}

    # ## Available Courses
    # {course_list}

    # ---

    # ### Task
    # 1. Select the most relevant courses for the chosen specialization.
    # 2. Build a progressive learning path (beginner → advanced).
    # 3. Avoid redundancy and irrelevant courses.

    # ---

    # ### Output Instructions
    # Return ONLY a valid JSON array.
    # Each item must have:
    # - step
    # - title
    # - url
    # - duration
    # - notes
    # - image
    # """



    # prompt = f"""
    # You are an AI assistant that builds personalized learning paths for students and professionals.

    # ## User Profile
    # - College: {user_data.get('college')}
    # - Department: {user_data.get('department')}
    # - major: {user_data.get('major')}
    # - skills: {user_data.get('skills')}
    # - interests: {user_data.get('interests')}
    # - career_goal: {user_data.get('career_goal')}

    # ## Available Courses
    # {course_list}

    # ---

    # ### Task
    # # 1. Select the most relevant courses from the list above.  
    # # - Prioritize alignment with **career goal**, **skills gap**, and **high-demand skills**.  
    # # - Ensure logical progression: from beginner → intermediate → advanced.  
    # # - Avoid redundant or irrelevant courses.  

    # # 2. Build a **step-by-step learning path** (roadmap).  
    # # - Each step should include exactly one course.  
    # # - Keep the sequence progressive and practical.  

    # 1. Select the most relevant courses for the chosen college, department, major, skills, interests, and career goal.
    # 2. Build a progressive learning path (beginner → advanced).
    # 3. Avoid redundancy and irrelevant courses.

    # ---

    # ### Output Instructions
    # Return ONLY a valid JSON array.
    # Each item must have:
    # - step
    # - title
    # - url
    # - duration
    # - notes
    # - image
    # """





    # prompt = f"""
    # You are an AI assistant that builds **personalized learning paths** for students and professionals.

    # ## User Profile
    # - Name: {user_data.get('name')}
    # - Specialization: {user_data.get('specialization')}
    # - Skills: {', '.join(user_data.get('skills', []))}
    # - Certifications: {', '.join(user_data.get('certifications', []))}
    # - Interests: {', '.join(user_data.get('interests', []))}
    # - Experience Level: {user_data.get('level')}
    # - Career Goal: {user_data.get('career_goal')}

    # ## Available Courses (from our database)
    # {course_list}

    # ## High-Demand Skills in the Job Market
    # {', '.join(high_demand)}

    # ---

    # ### 🎯 Task
    # 1. Select the most relevant courses from the list above.  
    # - Prioritize alignment with **career goal**, **skills gap**, and **high-demand skills**.  
    # - Ensure logical progression: from beginner → intermediate → advanced.  
    # - Avoid redundant or irrelevant courses.  

    # 2. Build a **step-by-step learning path** (roadmap).  
    # - Each step should include exactly one course.  
    # - Keep the sequence progressive and practical.  

    # ---

    # ### ⚠️ Output Instructions (VERY IMPORTANT)
    # - Return the result as a **valid JSON array ONLY** (no extra text, no markdown).  
    # - Each item in the array MUST follow this format:

    # [
    # {{
    #     "step": 1,
    #     "title": "Course Title",
    #     "url": "https://...",
    #     "duration": "10h 30m",
    #     "notes": "Why this course is important / what it covers",
    #     "image": "https://..."
    # }}
    # ]
    # """

    


# Generate a step-by-step personalized learning path using ONLY the available courses.
#     Prioritize courses teaching high-demand skills. Include recommended order, approximate durations, and progression notes.