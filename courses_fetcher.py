# courses_fetcher.py
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, future=True)

def search_courses(keywords: list, limit=20):
    """Search courses by keywords (matches title). Returns list of dicts."""
    if not keywords:
        return []
    patterns = [f"%{k}%" for k in keywords if k.strip()]

    # build simple OR query for title only (لان description و platform مش موجودين)
    clauses = []
    params = {}
    for i, p in enumerate(patterns):
        clauses.append(f"title ILIKE :p{i}")
        params[f"p{i}"] = p

    where_clause = " OR ".join(clauses)
    sql = text(f"""
        SELECT id, title, url, rating, num_reviews, num_published_lectures,
               created, last_update_date, duration, instructors_id, image
        FROM courses
        WHERE {where_clause}
        LIMIT :limit
    """)
    params['limit'] = limit

    with engine.connect() as conn:
        res = conn.execute(sql, params).fetchall()
    return [dict(row._mapping) for row in res]

# import openai
# import numpy as np
# from database import get_supabase_client

# def cosine_similarity(vec1, vec2):
#     return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# def get_embedding(text):
#     response = openai.embeddings.create(
#         model="text-embedding-3-small",
#         input=text
#     )
#     return response.data[0].embedding

# def search_courses_with_embeddings(user_profile, limit=20):
#     client = get_supabase_client()

#     # ولد embedding للمستخدم
#     profile_text = " ".join(user_profile.get("skills", []) +
#                             user_profile.get("interests", []) +
#                             [user_profile.get("specialization", "")] +
#                             [user_profile.get("career_goal", "")])
#     user_emb = np.array(get_embedding(profile_text))

#     # استرجع الكورسات + embeddings
#     data = client.table("courses").select("id, title, url, rating, num_reviews, duration, image, embedding").limit(200).execute()
#     courses = data.data or []

#     scored_courses = []
#     for c in courses:
#         course_emb = np.array(c.get("embedding"))
#         if course_emb is None:
#             continue

#         similarity = cosine_similarity(user_emb, course_emb)

#         # أضف وزن إضافي
#         rating = c.get("rating") or 0
#         reviews = c.get("num_reviews") or 0
#         score = similarity * 10 + rating * 0.5 + min(reviews / 1000, 5)

#         c["match_score"] = round(score, 3)
#         scored_courses.append(c)

#     scored_courses.sort(key=lambda x: x["match_score"], reverse=True)
#     return scored_courses[:limit]
