const API_URL = "https://2git8cdij7.execute-api.eu-west-3.amazonaws.com/prod";
const state = {
  questions: [],
  currentIndex: 0,
  score: 0,
  answered: false,
};

const questionTitle = document.getElementById('question-title');
const choicesEl = document.getElementById('choices');
const statusEl = document.getElementById('status');
const currentNumberEl = document.getElementById('current-number');
const totalNumberEl = document.getElementById('total-number');
const scoreEl = document.getElementById('score');
const nextBtn = document.getElementById('nextBtn');
const restartBtn = document.getElementById('restartBtn');

async function fetchQuiz() {
  try {
    const response = await fetch(`${API_URL}/quiz/questions?count=6`);
    const data = await response.json();
    state.questions = data.questions;
    state.currentIndex = 0;
    state.score = 0;
    state.answered = false;
    updateCounters();
    renderQuestion();
  } catch (error) {
    questionTitle.textContent = 'Impossible de charger le quiz.';
    statusEl.textContent = error.message;
    statusEl.className = 'status error';
  }
}

function updateCounters() {
  currentNumberEl.textContent = state.currentIndex + 1;
  totalNumberEl.textContent = state.questions.length;
  scoreEl.textContent = state.score;
}

function renderQuestion() {
  const question = state.questions[state.currentIndex];
  if (!question) {
    showFinalScreen();
    return;
  }

  questionTitle.textContent = question.text;
  statusEl.textContent = '';
  statusEl.className = 'status';
  nextBtn.classList.add('hidden');
  restartBtn.classList.add('hidden');
  state.answered = false;

  choicesEl.innerHTML = '';
  question.options.forEach((option) => {
    const button = document.createElement('button');
    button.className = 'btn choice';
    button.textContent = option.text;
    button.type = 'button';
    button.addEventListener('click', () => selectAnswer(question.id, option.id));
    choicesEl.appendChild(button);
  });

  updateCounters();
}

async function selectAnswer(questionId, answerId) {
  if (state.answered) return;
  state.answered = true;

  try {
    const response = await fetch(`${API_URL}/quiz/answer`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question_id: questionId, answer_id: answerId }),
    });
    const result = await response.json();

    const buttons = Array.from(document.querySelectorAll('.choice'));
    buttons.forEach((button, index) => {
      button.disabled = true;
      const optionId = state.questions[state.currentIndex].options[index].id;
      if (optionId === result.correct_answer_id) {
        button.classList.add('choice-correct');
      }
      if (optionId === answerId && !result.correct) {
        button.classList.add('choice-wrong');
      }
    });

    if (result.correct) {
      state.score += 1;
      statusEl.textContent = 'Bonne réponse ! ' + result.explanation;
      statusEl.className = 'status success';
    } else {
      statusEl.textContent = `Mauvaise réponse. La bonne réponse était : ${result.correct_answer_text}. ${result.explanation}`;
      statusEl.className = 'status error';
    }

    scoreEl.textContent = state.score;
    nextBtn.classList.remove('hidden');
    if (state.currentIndex === state.questions.length - 1) {
      nextBtn.textContent = 'Voir le score final';
    } else {
      nextBtn.textContent = 'Question suivante';
    }
  } catch (error) {
    statusEl.textContent = 'Erreur lors de la validation : ' + error.message;
    statusEl.className = 'status error';
    state.answered = false;
  }
}

function showFinalScreen() {
  questionTitle.textContent = 'Quiz terminé !';
  choicesEl.innerHTML = '';
  statusEl.textContent = `Ton score final est ${state.score} sur ${state.questions.length}.`;
  statusEl.className = 'status success';
  nextBtn.classList.add('hidden');
  restartBtn.classList.remove('hidden');
  currentNumberEl.textContent = state.questions.length;
}

function goToNextQuestion() {
  state.currentIndex += 1;
  if (state.currentIndex >= state.questions.length) {
    showFinalScreen();
  } else {
    renderQuestion();
  }
}

function restartQuiz() {
  fetchQuiz();
}

nextBtn.addEventListener('click', goToNextQuestion);
restartBtn.addEventListener('click', restartQuiz);

fetchQuiz();
