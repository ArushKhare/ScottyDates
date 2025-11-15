# backend/main.py

from datetime import timedelta
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .db import Base, engine, SessionLocal
from . import models, schemas, auth, ai

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TartanDate API",
    version="0.1.0",
)

# CORS so your Vite frontend can talk to this backend
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins + ["*"],  # keep * for dev convenience
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Dependency: DB session --------------------------------------------------


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Auth routes -------------------------------------------------------------


@app.post("/auth/register", response_model=schemas.UserOut)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_pw = auth.get_password_hash(user_in.password)
    user = models.User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_pw,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# NOTE: don't use schemas.Token since it doesn't exist; just return a dict
@app.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.UserOut)
def read_current_user(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


# --- Profile routes ----------------------------------------------------------


@app.post("/profile", response_model=schemas.ProfileOut)
def upsert_profile(
    profile_in: schemas.ProfileCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    profile = (
        db.query(models.Profile)
        .filter(models.Profile.user_id == current_user.id)
        .first()
    )
    if profile is None:
        profile = models.Profile(
            user_id=current_user.id,
        )

    profile.age = profile_in.age
    profile.gender = profile_in.gender
    profile.major = profile_in.major
    profile.class_year = profile_in.class_year
    profile.campus = profile_in.campus
    profile.bio = profile_in.bio
    # interests: assume a simple comma-separated string in DB
    profile.interests = ",".join(profile_in.interests or [])

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@app.get("/profile/me", response_model=schemas.ProfileOut)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    profile = (
        db.query(models.Profile)
        .filter(models.Profile.user_id == current_user.id)
        .first()
    )
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile


# --- Matching routes ---------------------------------------------------------
# NOTE: no response_model here; we construct a JSON list manually


@app.get("/matches")
def get_matches(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Return AI-scored matches for the current user as:
    [
      {
        "profile": <ProfileOut dict>,
        "score": <float>
      },
      ...
    ]
    """
    my_profile = (
        db.query(models.Profile)
        .filter(models.Profile.user_id == current_user.id)
        .first()
    )
    if my_profile is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must create a profile first",
        )

    # Fetch other profiles (same campus by default)
    others = (
        db.query(models.Profile)
        .filter(models.Profile.user_id != current_user.id)
        .filter(models.Profile.campus == my_profile.campus)
        .all()
    )

    results = []
    for p in others:
        try:
            score = ai.score_match(my_profile, p)
        except Exception:
            # Fail open with a simple fallback
            score = 50.0

        # Use your existing ProfileOut schema to serialize the profile
        try:
            p_out = schemas.ProfileOut.from_orm(p)
        except Exception:
            # If from_orm fails (e.g., missing config), fall back to a minimal dict
            p_out = {
                "user_id": p.user_id,
                "age": p.age,
                "gender": p.gender,
                "major": p.major,
                "class_year": p.class_year,
                "campus": p.campus,
                "bio": p.bio,
            }

        results.append(
            {
                "profile": p_out,
                "score": score,
            }
        )

    # Sort by score descending
    results.sort(key=lambda m: m["score"], reverse=True)
    return results


# --- Messaging routes --------------------------------------------------------


@app.post("/messages", response_model=schemas.MessageOut)
def send_message(
    message_in: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Create a message from current_user -> to_user_id.
    """
    # Make sure recipient exists
    other = db.query(models.User).filter(models.User.id == message_in.to_user_id).first()
    if other is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found",
        )

    msg = models.Message(
        from_user_id=current_user.id,
        to_user_id=message_in.to_user_id,
        text=message_in.text,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@app.get(
    "/messages/thread/{other_user_id}",
    response_model=List[schemas.MessageOut],
)
def get_thread(
    other_user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Get the conversation between current_user and other_user_id.
    """
    msgs = (
        db.query(models.Message)
        .filter(
            (
                (models.Message.from_user_id == current_user.id)
                & (models.Message.to_user_id == other_user_id)
            )
            | (
                (models.Message.from_user_id == other_user_id)
                & (models.Message.to_user_id == current_user.id)
            )
        )
        .order_by(models.Message.created_at.asc())
        .all()
    )
    return msgs


# --- AI chat helper ----------------------------------------------------------
# NOTE: no response_model here; we return a plain dict with summary & openers


@app.get("/ai/chat-helper/{other_user_id}")
def chat_helper(
    other_user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Use Gemini to:
      - Summarize the other user's profile + interests
      - Suggest 2–3 lines you can say next in the chat

    Returns:
    {
      "summary": "...",
      "openers": ["...", "...", ...]
    }
    """
    my_profile = (
        db.query(models.Profile)
        .filter(models.Profile.user_id == current_user.id)
        .first()
    )
    other_profile = (
        db.query(models.Profile)
        .filter(models.Profile.user_id == other_user_id)
        .first()
    )
    if other_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Other user's profile not found",
        )

    # Load recent messages in this thread
    msgs = (
        db.query(models.Message)
        .filter(
            (
                (models.Message.from_user_id == current_user.id)
                & (models.Message.to_user_id == other_user_id)
            )
            | (
                (models.Message.from_user_id == other_user_id)
                & (models.Message.to_user_id == current_user.id)
            )
        )
        .order_by(models.Message.created_at.asc())
        .all()
    )

    try:
        summary, openers = ai.summarize_and_suggest(
            my_profile=my_profile,
            other_profile=other_profile,
            messages=msgs,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI error: {e}",
        )

    return {"summary": summary, "openers": openers}
