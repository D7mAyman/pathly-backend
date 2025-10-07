from sqlalchemy import Column, Integer, String, Float, Date
from database import Base
from pydantic import BaseModel
from typing import List, Optional

# SQLAlchemy model for courses
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    rating = Column(Float)
    num_reviews = Column(Integer)
    num_published_lectures = Column(Integer)
    created = Column(Date)
    last_update_date = Column(Date)
    duration = Column(String)
    instructors_id = Column(String)
    image = Column(String)


# User profile model
class UserProfile(BaseModel):
    college: str
    department: str
    major: str
    skills: Optional[List[str]] = []
    # interests: Optional[List[str]] = []
    career_goal: Optional[str] = None


#-------------------------------------------------------------------1----------------------
# from sqlalchemy import Column, Integer, String, Float, Date
# from database import Base
# from pydantic import BaseModel
# from typing import List, Optional

# # SQLAlchemy model for courses
# class Course(Base):
#     __tablename__ = "courses"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     url = Column(String, nullable=False)
#     rating = Column(Float)
#     num_reviews = Column(Integer)
#     num_published_lectures = Column(Integer)
#     created = Column(Date)
#     last_update_date = Column(Date)
#     duration = Column(String)
#     instructors_id = Column(String)
#     image = Column(String)

# # # Pydantic model for user profile
# # class UserProfile(BaseModel):
# #     name: str
# #     specialization: str
# #     skills: List[str]
# #     certifications: List[str]
# #     interests: List[str]
# #     level: str
# #     career_goal: str

# class UserProfile(BaseModel):
#     college: str
#     department: str
#     major: str
#     skills: Optional[List[str]] = []   # ✅ skills optional (user chooses only what he already has)
#     # interests: Optional[List[str]] = []
#     career_goal: str









    #-------------------------------------------------------------------------------

# from sqlalchemy import Column, Integer, String, Float, Date
# from database import Base
# from pydantic import BaseModel
# from typing import List, Optional

# # SQLAlchemy model for courses
# class Course(Base):
#     __tablename__ = "courses"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     url = Column(String, nullable=False)
#     rating = Column(Float)
#     num_reviews = Column(Integer)
#     num_published_lectures = Column(Integer)
#     created = Column(Date)
#     last_update_date = Column(Date)
#     duration = Column(String)
#     instructors_id = Column(String)
#     image = Column(String)


# class UserProfile(BaseModel):
#     college: str
#     department: str
#     major: str



    #-------------------------------------------------------------------------------

    # # Pydantic model for user profile
# class UserProfile(BaseModel):
#     name: str
#     specialization: str
#     skills: List[str]
#     certifications: List[str]
#     interests: List[str]
#     level: str
#     career_goal: str