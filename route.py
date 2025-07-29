from fastapi import APIRouter, Request
from lib.agents import chat_agent, assignment_agent, summarizer_agent, collector_agent, course_suggestor_agent
from lib.prompts import system_prompts

router = APIRouter()

# === General Chat ===
@router.post("/chat")
async def chat(request: Request):
    body = await request.json()
    return chat_agent.handle(body)

@router.post("/summarize")
async def summarize(request: Request):
    body = await request.json()
    return summarizer_agent.handle(body)

# === Coding & Dev Tools ===
@router.post("/code/gen")
async def generate_code(request: Request):
    body = await request.json()
    return code_agent.generate_code(body)

@router.post("/code/debug")
async def debug_code(request: Request):
    body = await request.json()
    return code_agent.debug_code(body)

# === Prompt Utilities ===
@router.get("/prompt/{type}")   
def get_prompt(type: str):
    return {"prompt": system_prompts.get_prompt(type)}

# === Q&A / Retrieval ===
@router.post("/qa")
async def question_answer(request: Request):
    body = await request.json()
    return chat_agent.answer_with_context(body)

# === Writing Tools ===
@router.post("/write/article")
async def write_article(request: Request):
    body = await request.json()
    return chat_agent.write_article(body)

@router.post("/write/email")
async def write_email(request: Request):
    body = await request.json()
    return chat_agent.write_email(body)

# === Agents ===
@router.post("/agent/task")
async def run_task_agent(request: Request):
    body = await request.json()
    return chat_agent.task_agent(body)

@router.post("/agent/memory")
async def memory_agent(request: Request):
    body = await request.json()
    return chat_agent.memory_agent(body)

# === Utility Tools ===
@router.post("/utils/translate")
async def translate(request: Request):
    body = await request.json()
    return chat_agent.translate(body)

@router.post("/utils/grammar")
async def grammar_check(request: Request):
    body = await request.json()
    return chat_agent.grammar_check(body)

@router.post("/utils/tone")
async def tone_shift(request: Request):
    body = await request.json()
    return chat_agent.tone_shift(body)

# === Multimodal ===
@router.post("/vision/analyze")
async def vision_analyze(request: Request):
    body = await request.json()
    return chat_agent.analyze_image(body)

# === Code Explanation ===
@router.post("/code/explain")
async def explain_code(request: Request):
    body = await request.json()
    return code_agent.explain_code(body)

# === Document Tools ===
@router.post("/doc/structure")
async def doc_structure(request: Request):
    body = await request.json()
    return chat_agent.doc_structure(body)

@router.post("/doc/expand")
async def doc_expand(request: Request):
    body = await request.json()
    return chat_agent.doc_expand(body)

# === Roleplay / Persona Chat ===
@router.post("/chat/roleplay")
async def roleplay_chat(request: Request):
    body = await request.json()
    return chat_agent.roleplay(body)

# === Custom Route Hook ===
@router.post("/custom")
async def custom_route(request: Request):
    body = await request.json()
    return llm_initializer(body)


#specialized for PAN-SEA hackathons

# === Assignment Tools ===
@router.post("/assignments/track")
async def track_assignments(request: Request):
    body = await request.json()
    return assignment_agent.track(body)

@router.post("/grading/auto")
async def automated_grading(request: Request):
    body = await request.json()
    return assignment_agent.grade(body)

# === Info Collector ===
@router.post("/collector/info")
async def collect_user_info(request: Request):
    body = await request.json()
    return collector_agent.collect_user_info(body)

@router.post("/collector/course")
async def collect_course_info(request: Request):
    body = await request.json()
    return collector_agent.collect_course_info(body)

# === Lesson Plan ===
@router.post("/lesson/plan")
async def lesson_plan(request: Request):
    body = await request.json()
    return chat_agent.generate_lesson_plan(body)

# === Course Suggestion ===
@router.post("/suggest/course")
async def course_suggestion(request: Request):
    body = await request.json()
    return course_suggestor_agent.suggest(body)
