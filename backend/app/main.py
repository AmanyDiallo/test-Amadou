from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuizOption(BaseModel):
    id: str
    text: str


class QuizQuestion(BaseModel):
    id: str
    category: str
    text: str
    options: List[QuizOption]


class QuizQuestionsResponse(BaseModel):
    questions: List[QuizQuestion]


class QuizAnswerRequest(BaseModel):
    question_id: str
    answer_id: str


class QuizAnswerResponse(BaseModel):
    question_id: str
    selected_answer_id: str
    correct: bool
    correct_answer_id: str
    correct_answer_text: str
    explanation: str


QUESTIONS = [
    {
        "id": "q1",
        "category": "Ligue 1",
        "text": "Quel club a remporté le plus de titres en Ligue 1 ?",
        "options": [
            {"id": "a", "text": "Paris Saint-Germain"},
            {"id": "b", "text": "Olympique de Marseille"},
            {"id": "c", "text": "AS Monaco"},
            {"id": "d", "text": "Olympique Lyonnais"},
        ],
        "answer_id": "a",
        "explanation": "Paris Saint-Germain a remporté le plus de titres de Ligue 1, surtout depuis 2010.",
    },
    {
        "id": "q2",
        "category": "Liga",
        "text": "Quel joueur a gagné le plus de Ballons d'Or avec le Real Madrid ?",
        "options": [
            {"id": "a", "text": "Karim Benzema"},
            {"id": "b", "text": "Cristiano Ronaldo"},
            {"id": "c", "text": "Luka Modrić"},
            {"id": "d", "text": "Sergio Ramos"},
        ],
        "answer_id": "b",
        "explanation": "Cristiano Ronaldo a remporté cinq Ballons d'Or, dont quatre avec le Real Madrid.",
    },
    {
        "id": "q3",
        "category": "Premier League",
        "text": "Quel club a gagné le plus de titres de Premier League depuis 1992 ?",
        "options": [
            {"id": "a", "text": "Manchester United"},
            {"id": "b", "text": "Manchester City"},
            {"id": "c", "text": "Chelsea"},
            {"id": "d", "text": "Arsenal"},
        ],
        "answer_id": "a",
        "explanation": "Manchester United a obtenu le plus de titres de Premier League, en particulier sous Sir Alex Ferguson.",
    },
    {
        "id": "q4",
        "category": "Bundesliga",
        "text": "Quel club a remporté le plus grand nombre de titres de Bundesliga ?",
        "options": [
            {"id": "a", "text": "Borussia Dortmund"},
            {"id": "b", "text": "FC Bayern Munich"},
            {"id": "c", "text": "RB Leipzig"},
            {"id": "d", "text": "Bayer Leverkusen"},
        ],
        "answer_id": "b",
        "explanation": "Le Bayern Munich domine la Bundesliga avec de très nombreux titres.",
    },
    {
        "id": "q5",
        "category": "Serie A",
        "text": "Quel club italien possède le plus de Scudetti ?",
        "options": [
            {"id": "a", "text": "Juventus"},
            {"id": "b", "text": "AC Milan"},
            {"id": "c", "text": "Inter Milan"},
            {"id": "d", "text": "AS Roma"},
        ],
        "answer_id": "a",
        "explanation": "La Juventus est le club qui a remporté le plus de Scudetti.",
    },
    {
        "id": "q6",
        "category": "Champions League",
        "text": "Quel club a remporté le plus de Ligue des champions ?",
        "options": [
            {"id": "a", "text": "Real Madrid"},
            {"id": "b", "text": "AC Milan"},
            {"id": "c", "text": "Liverpool"},
            {"id": "d", "text": "FC Bayern Munich"},
        ],
        "answer_id": "a",
        "explanation": "Le Real Madrid est le club le plus titré en Ligue des champions.",
    },
]


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Lambda"}


@app.get("/quiz/questions", response_model=QuizQuestionsResponse)
def get_quiz_questions():
    return {"questions": [
        {
            "id": q["id"],
            "category": q["category"],
            "text": q["text"],
            "options": q["options"],
        }
        for q in QUESTIONS
    ]}


@app.post("/quiz/answer", response_model=QuizAnswerResponse)
def check_answer(payload: QuizAnswerRequest):
    question = next((q for q in QUESTIONS if q["id"] == payload.question_id), None)
    if question is None:
        raise HTTPException(status_code=404, detail="Question introuvable")

    correct_id = question["answer_id"]
    correct_option = next(opt for opt in question["options"] if opt["id"] == correct_id)
    answer_is_correct = payload.answer_id == correct_id

    return {
        "question_id": payload.question_id,
        "selected_answer_id": payload.answer_id,
        "correct": answer_is_correct,
        "correct_answer_id": correct_id,
        "correct_answer_text": correct_option["text"],
        "explanation": question["explanation"],
    }
