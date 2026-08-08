import random

from fastapi import FastAPI, HTTPException, Query
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
    {
        "id": "q7",
        "category": "Ligue 1",
        "text": "Quel entraîneur a remporté le plus de titres de champion de France ?",
        "options": [
            {"id": "a", "text": "Zinedine Zidane"},
            {"id": "b", "text": "Pep Guardiola"},
            {"id": "c", "text": "Carlo Ancelotti"},
            {"id": "d", "text": "Laurent Blanc"},
        ],
        "answer_id": "d",
        "explanation": "Laurent Blanc a remporté plusieurs titres de champion de France avec le PSG.",
    },
    {
        "id": "q8",
        "category": "Liga",
        "text": "Quel club a un surnom de 'Los Blancos' ?",
        "options": [
            {"id": "a", "text": "FC Barcelone"},
            {"id": "b", "text": "Atlético Madrid"},
            {"id": "c", "text": "Real Madrid"},
            {"id": "d", "text": "Valence CF"},
        ],
        "answer_id": "c",
        "explanation": "Real Madrid est surnommé 'Los Blancos' en raison de son maillot blanc.",
    },
    {
        "id": "q9",
        "category": "Premier League",
        "text": "Quel joueur détient le record du plus grand nombre de buts en Premier League ?",
        "options": [
            {"id": "a", "text": "Harry Kane"},
            {"id": "b", "text": "Alan Shearer"},
            {"id": "c", "text": "Wayne Rooney"},
            {"id": "d", "text": "Sergio Agüero"},
        ],
        "answer_id": "b",
        "explanation": "Alan Shearer détient le record de buts en Premier League.",
    },
    {
        "id": "q10",
        "category": "Bundesliga",
        "text": "Quelle équipe a remporté la Bundesliga en 2023 ?",
        "options": [
            {"id": "a", "text": "RB Leipzig"},
            {"id": "b", "text": "Bayern Munich"},
            {"id": "c", "text": "Borussia Dortmund"},
            {"id": "d", "text": "Eintracht Francfort"},
        ],
        "answer_id": "b",
        "explanation": "Le Bayern Munich a remporté la Bundesliga en 2023.",
    },
    {
        "id": "q11",
        "category": "Serie A",
        "text": "Quel joueur a remporté le Golden Boot de Serie A avec 36 buts en 2019-2020 ?",
        "options": [
            {"id": "a", "text": "Cristiano Ronaldo"},
            {"id": "b", "text": "Ciro Immobile"},
            {"id": "c", "text": "Lautaro Martínez"},
            {"id": "d", "text": "Paulo Dybala"},
        ],
        "answer_id": "b",
        "explanation": "Ciro Immobile a marqué 36 buts en Serie A en 2019-2020.",
    },
    {
        "id": "q12",
        "category": "Champions League",
        "text": "Quel joueur a remporté le plus de Ligue des champions en tant que joueur ?",
        "options": [
            {"id": "a", "text": "Cristiano Ronaldo"},
            {"id": "b", "text": "Lionel Messi"},
            {"id": "c", "text": "Paco Gento"},
            {"id": "d", "text": "Karim Benzema"},
        ],
        "answer_id": "c",
        "explanation": "Paco Gento détient le record de victoires en Ligue des champions avec 6 titres.",
    },
]


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Lambda"}


@app.get("/quiz/questions", response_model=QuizQuestionsResponse)
def get_quiz_questions(count: int = Query(4, ge=1, le=len(QUESTIONS))):
    sampled = random.sample(QUESTIONS, min(count, len(QUESTIONS)))
    questions = []
    for q in sampled:
        options = q["options"].copy()
        random.shuffle(options)
        questions.append({
            "id": q["id"],
            "category": q["category"],
            "text": q["text"],
            "options": options,
        })
    random.shuffle(questions)
    return {"questions": questions}


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
