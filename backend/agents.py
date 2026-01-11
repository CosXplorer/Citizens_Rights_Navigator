import json
import os
from typing import TypedDict, Optional, Dict, Any

from langgraph.graph import StateGraph
from langdetect import detect
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


# =====================================================
# GEMINI LLM (LangChain Stable Wrapper)
# =====================================================
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    temperature=0.2
)


# =====================================================
# LOAD DATABASE
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "complete_30_database.json")

with open(DB_PATH, "r", encoding="utf-8") as f:
    KB = json.load(f)


# =====================================================
# LLM HELPERS
# =====================================================
def normalize_query(raw_query: str) -> str:
    """
    Normalize user query using LLM.
    Falls back safely if quota is exceeded.
    """

    prompt = (
        "You are a civic query normalizer.\n"
        "Rewrite the user's input into ONE clear grievance statement.\n"
        "Rules:\n"
        "- ONE sentence only\n"
        "- No advice\n"
        "- No steps\n"
        "- No laws\n\n"
        f"User input: {raw_query}"
    )

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        cleaned = response.content.strip()
        return cleaned if cleaned else raw_query
    except Exception as e:
        print("⚠️ Normalization failed, using raw query:", e)
        return raw_query


def detect_language(text: str) -> str:
    try:
        return "Hindi" if detect(text) == "hi" else "English"
    except:
        return "English"


def translate_text(text: str, target_language: str) -> str:
    if target_language == "English":
        return text

    prompt = (
        f"Translate the following text into {target_language}.\n"
        "Preserve meaning and formatting.\n"
        "Do NOT add or remove content.\n\n"
        f"Text:\n{text}"
    )

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    except:
        return text


# =====================================================
# FALLBACK LLM (WHEN KB FAILS)
# =====================================================
def fallback_llm_guidance(user_query: str, language: str) -> str:
    prompt = f"""
You are a Civic Guidance Assistant.

Citizen problem:
"{user_query}"

Your job:
1. Identify the likely department
2. Identify the grievance type
3. Suggest where the citizen should go
4. List required documents
5. Suggest the first step

STRICT RULES:
- Do NOT give legal advice
- Do NOT mention laws
- Do NOT invent schemes
- Be simple and safe

Format:

Department:
Grievance Type:
Where to Go:
Documents Needed:
What to Do First:
"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        answer = response.content.strip()
    except:
        answer = "Please visit https://pgportal.gov.in to file a general grievance."

    final = f"""
⚠️ This issue is not yet in our official grievance database.

Based on your description, here is general guidance:

{answer}

You may also try:
https://pgportal.gov.in

⚠️ This is NOT legal advice. This is general citizen guidance only.
"""

    if language == "Hindi":
        final = translate_text(final, "Hindi")

    return final


# =====================================================
# RULE-BASED CORE
# =====================================================
def detect_intent(query: str, kb):
    query = query.lower()
    for entry in kb:
        for kw in entry["keywords"]:
            if kw.lower() in query:
                return entry
    return None


def build_guidance(entry: dict, language: str):
    title = entry["title_hi"] if language == "Hindi" else entry["title"]

    steps = "\n".join([f"{i+1}. {s}" for i, s in enumerate(entry["steps"])])
    documents = "\n".join([f"- {d}" for d in entry["documents"]])
    escalation = "\n".join([f"- {e}" for e in entry["escalation_path"]])
    links = "\n".join(entry["official_links"])
    contacts = "\n".join(entry.get("contact_numbers", []))

    timeline = "\n".join(
        [f"{k.replace('_',' ').title()}: {v}" for k, v in entry["timeline"].items()]
    )

    return f"""
## 🏛 {title}

📄 **Description**  
{entry['description']}

---

### ✅ Step-by-Step Process
{steps}

---

### ⏳ Timelines
{timeline}

---

### 📁 Documents Required
{documents}

---

### 🚨 Escalation Path
{escalation}

---

### 🔗 Official Links
{links}

---

### ☎️ Helpline / Contact
{contacts}

---

⚠️ *This is NOT legal advice. This information is for citizen guidance only.*
"""


# =====================================================
# LANGGRAPH STATE
# =====================================================
class AgentState(TypedDict):
    raw_query: str
    query: str
    language: str
    kb_entry: Optional[Dict[str, Any]]
    response: str


# =====================================================
# LANGGRAPH AGENTS
# =====================================================
def language_agent(state: AgentState):
    state["language"] = detect_language(state["raw_query"])
    return state


def translate_input_agent(state: AgentState):
    state["query"] = (
        translate_text(state["raw_query"], "English")
        if state["language"] != "English"
        else state["raw_query"]
    )
    return state


def normalization_agent(state: AgentState):
    state["query"] = normalize_query(state["query"])
    return state


def intent_agent(state: AgentState):
    state["kb_entry"] = detect_intent(state["query"], KB)
    return state


def guidance_agent(state: AgentState):
    if state["kb_entry"]:
        state["response"] = build_guidance(
            state["kb_entry"],
            state["language"]
        )
    else:
        state["response"] = fallback_llm_guidance(
            state["query"],
            state["language"]
        )
    return state


def translate_output_agent(state: AgentState):
    if state["language"] != "English":
        state["response"] = translate_text(state["response"], state["language"])
    return state


# =====================================================
# BUILD LANGGRAPH PIPELINE
# =====================================================
graph = StateGraph(AgentState)

graph.add_node("language", language_agent)
graph.add_node("translate_input", translate_input_agent)
graph.add_node("normalize", normalization_agent)
graph.add_node("intent", intent_agent)
graph.add_node("guidance", guidance_agent)
graph.add_node("translate_output", translate_output_agent)

graph.set_entry_point("language")

graph.add_edge("language", "translate_input")
graph.add_edge("translate_input", "normalize")
graph.add_edge("normalize", "intent")
graph.add_edge("intent", "guidance")
graph.add_edge("guidance", "translate_output")

grievance_graph = graph.compile()
