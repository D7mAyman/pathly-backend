# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from models import UserProfile
from courses_fetcher import search_courses
from recommender import generate_learning_path
# from skills_generator import generate_required_skills
from skills_generator import generate_combined_skills
from database import get_db

app = FastAPI(title='Smart Learning Recommender')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Smart Learning Recommender API is running"}

@app.post("/generate-skills")
def generate_skills(user: UserProfile):
    """Generate relevant skills for the given specialization & career goal"""
    if not user.major or not user.career_goal:
        return {"error": "Major and career_goal are required to generate skills"}
    skills = generate_combined_skills(user.major, user.career_goal)
    # skills = generate_required_skills(user.major, user.career_goal)

    return {"skills": skills}

@app.post("/recommend")
def recommend(user: UserProfile, db: Session = Depends(get_db)):
    keywords = []
    if user.college: keywords.append(user.college)
    if user.department: keywords.append(user.department)
    if user.major: keywords.append(user.major)
    if user.skills: keywords.extend(user.skills)
    # if user.interests: keywords.extend(user.interests)
    if user.career_goal: keywords.append(user.career_goal)

    courses = search_courses(keywords, limit=30)
    if not courses:
        return {"error": "No courses found for this profile"}

    courses_data = [dict(c) for c in courses]

    learning_path = generate_learning_path(user.dict(), courses_data)
    return {
        "user_profile": user.dict(),
        "recommended_courses": courses_data,
        "learning_path": learning_path,
    }

#----------------------------------------------1---------------

# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware
# from models import UserProfile, Course
# from courses_fetcher import search_courses
# from recommender import generate_learning_path
# from database import get_db
# from pydantic import BaseModel
# from openai import OpenAI
# import json
# import os

# # Init app
# app = FastAPI(title="Smart Learning Recommender")

# # Allow frontend (React) to access backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # you can restrict later e.g. ["http://localhost:3000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Request model for skills generation
# class SkillRequest(BaseModel):
#     specialization: str
#     career_goal: str


# @app.post("/generate-skills")
# def generate_skills(req: SkillRequest):
#     """Generate relevant skills based on specialization + career goal"""
#     prompt = f"""
#     You are an expert career advisor. 
#     Based on the following information, generate a list of essential skills:

#     Specialization: {req.specialization}
#     Career Goal: {req.career_goal}

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
#         max_tokens=500,
#     )

#     try:
#         skills = json.loads(response.choices[0].message.content)
#         return {"skills": skills}
#     except Exception:
#         return {"error": "Failed to parse GPT response"}


# @app.post("/recommend")
# def recommend(user: UserProfile, db: Session = Depends(get_db)):
#     """Generate learning path based on user profile + courses database"""
#     # Prepare keywords from user profile
#     keywords = []
#     if user.specialization:
#         keywords.append(user.specialization)
#     if user.career_goal:
#         keywords.append(user.career_goal)
#     if user.skills:
#         keywords.extend(user.skills)
#     if user.interests:
#         keywords.extend(user.interests)

#     # Search courses in DB
#     courses = search_courses(keywords, limit=30)
#     if not courses:
#         return {"error": "No courses found for this profile"}

#     # Convert courses to dicts
#     courses_data = [
#         {
#             "id": c.get("id"),
#             "title": c.get("title"),
#             "url": c.get("url"),
#             "rating": c.get("rating"),
#             "num_reviews": c.get("num_reviews"),
#             "num_published_lectures": c.get("num_published_lectures"),
#             "created": c.get("created"),
#             "last_update_date": c.get("last_update_date"),
#             "duration": c.get("duration"),
#             "instructors_id": c.get("instructors_id"),
#             "image": c.get("image"),
#         }
#         for c in courses
#     ]

#     # Generate personalized learning path
#     learning_path = generate_learning_path(user.dict(), courses_data)
#     return {
#         "user_profile": user.dict(),
#         "recommended_courses": courses_data,
#         "learning_path": learning_path,
#     }


#------------------------------------------------------------------------------

# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware  # <-- استيراد CORS
# from models import UserProfile, Course
# from courses_fetcher import search_courses
# from recommender import generate_learning_path
# from database import get_db

# app = FastAPI(title='Smart Learning Recommender')

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # أو ["http://localhost:3000"] إذا حاب تحدد المصدر
#     allow_credentials=True,
#     allow_methods=["*"],  # مهم عشان يسمح بطلبات OPTIONS
#     allow_headers=["*"],
# )

# @app.get('/health')
# def health_check():
#     return {'status': 'healthy', 'message': 'Smart Learning Recommender API is running'}

# @app.post('/test')
# def test_endpoint(user: UserProfile):
#     return {
#         'message': 'Data received successfully',
#         'user_data': user.dict(),
#         'skills_type': type(user.skills).__name__,
#         'interests_type': type(user.interests).__name__
#     }

# @app.post('/recommend')
# def recommend(user: UserProfile, db: Session = Depends(get_db)):
#     # prepare keywords from user data
#     # keywords = []
#     # keywords.extend(user.skills or [])
#     # keywords.extend(user.interests or [])
#     # if user.specialization:
#     #     keywords.append(user.specialization)
#     # if user.career_goal:
#     #     keywords.append(user.career_goal)
#     keywords = []
#     if user.college:
#         keywords.append(user.college)
#     if user.department:
#         keywords.append(user.department)
#     if user.major:
#         keywords.append(user.major)
#     if user.skills:
#         keywords.extend(user.skills)
#     if user.interests:
#         keywords.extend(user.interests)
#     if user.career_goal:
#         keywords.append(user.career_goal)

#     # search courses from Supabase DB
#     courses = search_courses(keywords, limit=30)

#     if not courses:
#         return {'error': 'No courses found for this profile'}

#     # convert SQLAlchemy objects to dict
#     courses_data = [
#         {
#             "id": c.get('id'),
#             "title": c.get('title'),
#             "url": c.get('url'),
#             "rating": c.get('rating'),
#             "num_reviews": c.get('num_reviews'),
#             "num_published_lectures": c.get('num_published_lectures'),
#             "created": c.get('created'),
#             "last_update_date": c.get('last_update_date'),
#             "duration": c.get('duration'),
#             "instructors_id": c.get('instructors_id'),
#             "image": c.get('image'),
#         }
#         for c in courses
#     ]

#     # generate learning path
#     learning_path = generate_learning_path(user.dict(), courses_data)
#     return {
#         'user_profile': user.dict(),
#         'recommended_courses': courses_data,
#         'learning_path': learning_path
#     }





# -----------------------------------------------------------------------------

# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware  # <-- استيراد CORS
# from models import UserProfile, Course
# from courses_fetcher import search_courses
# from recommender import generate_learning_path
# from database import get_db

# app = FastAPI(title='Smart Learning Recommender')

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # أو ["http://localhost:3000"] إذا حاب تحدد المصدر
#     allow_credentials=True,
#     allow_methods=["*"],  # مهم عشان يسمح بطلبات OPTIONS
#     allow_headers=["*"],
# )

# @app.post('/recommend')
# def recommend(user: UserProfile, db: Session = Depends(get_db)):
#     # prepare keywords from user data
#     # keywords = []
#     # keywords.extend(user.skills or [])
#     # keywords.extend(user.interests or [])
#     # if user.specialization:
#     #     keywords.append(user.specialization)
#     # if user.career_goal:
#     #     keywords.append(user.career_goal)
#     keywords = []
#     if user.college:
#         keywords.append(user.college)
#     if user.department:
#         keywords.append(user.department)
#     if user.major:
#         keywords.append(user.major)

#     # search courses from Supabase DB
#     courses = search_courses(keywords, limit=30)

#     if not courses:
#         return {'error': 'No courses found for this profile'}

#     # convert SQLAlchemy objects to dict
#     courses_data = [
#         {
#             "id": c.get('id'),
#             "title": c.get('title'),
#             "url": c.get('url'),
#             "rating": c.get('rating'),
#             "num_reviews": c.get('num_reviews'),
#             "num_published_lectures": c.get('num_published_lectures'),
#             "created": c.get('created'),
#             "last_update_date": c.get('last_update_date'),
#             "duration": c.get('duration'),
#             "instructors_id": c.get('instructors_id'),
#             "image": c.get('image'),
#         }
#         for c in courses
#     ]

#     # generate learning path
#     learning_path = generate_learning_path(user.dict(), courses_data)
#     return {
#         'user_profile': user.dict(),
#         'recommended_courses': courses_data,
#         'learning_path': learning_path
#     }









#------------------------------------------------------------------------------





# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# from models import UserProfile
# from courses_fetcher import search_courses_with_embeddings
# from recommender import generate_learning_path
# from database import get_db

# app = FastAPI(title="Smart Learning Recommender (Embeddings)")

# @app.post("/recommend")
# def recommend(user: UserProfile, db: Session = Depends(get_db)):
#     # ابحث بالكورسات باستخدام Embeddings
#     courses = search_courses_with_embeddings(user.dict(), limit=50)
#     if not courses:
#         return {"error": "No courses found for this profile"}

#     # خذ أفضل 10 فقط
#     top_courses = courses[:10]

#     # JSON output
#     courses_data = [
#         {
#             "id": c.get("id"),
#             "title": c.get("title"),
#             "url": c.get("url"),
#             "rating": c.get("rating"),
#             "num_reviews": c.get("num_reviews"),
#             "duration": c.get("duration"),
#             "image": c.get("image"),
#             "match_score": c.get("match_score"),
#         }
#         for c in top_courses
#     ]

#     # بناء خطة تعلم
#     learning_path = generate_learning_path(user.dict(), courses_data)

#     return {
#         "user_profile": user.dict(),
#         "recommended_courses": courses_data,
#         "learning_path": learning_path,
#     }
