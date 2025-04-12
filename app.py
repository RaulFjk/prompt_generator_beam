import os
import yaml
import json
from typing import Optional, List
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import openai

# This project uses an AI-agent-like architecture which is not yet finished. This is only a prototype.
# This project uses only gpt-4o 
# ALL THE PROMPTS USED HERE CAN BE ACCESSED AND REVIEWED IN THE CONFIG FOLDER. EACH PROMPT IS INCLUDED IN AN YAML FILE

load_dotenv()

# FastAPI App
app = FastAPI(title="Data Extraction Prompt Generator", version="2.0.0")

# openai.api_key = os.getenv("OPENAI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://promptgenerator-challenge.netlify.app"],  # For making some local tests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read config files (YAML) into memory
def load_yaml_content(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["text"]

META_PROMPT_TEXT = load_yaml_content("config/meta_prompt.yaml")
DOC_CLASS_PROMPT_TEXT = load_yaml_content("config/doc_classification.yaml")
INVOICE_CHECK_TEXT = load_yaml_content("config/invoice_check.yaml")
SUPPORT_TICKET_CHECK_TEXT = load_yaml_content("config/support_ticket_check.yaml")
EMAIL_CHECK_TEXT = load_yaml_content("config/email_check.yaml")
LEGAL_DOC_CHECK_TEXT = load_yaml_content("config/legal_doc_check.yaml")

# Pydantic Models
class GeneratePromptRequest(BaseModel):
    api_key: str
    extraction_task: str
    doc_type: Optional[str] = None

class GeneratePromptResponse(BaseModel):
    final_prompt: str
    identified_doc_type: str
    check_result: Optional[str] = None  # e.g. "Pass" or "Fail"
    check_reason: Optional[str] = None  # explanation
    adjusted_prompt: Optional[str] = None  # the partially fixed prompt if "Fail"

class ExtractionTaskRequest(BaseModel):
    extraction_task: str
    doc_type: Optional[str] = None

class ExtractionTaskResponse(BaseModel):
    final_prompt: str
    identified_doc_type: str
    check_result: Optional[str] = None  # e.g. "Pass" or "Fail"
    check_reason: Optional[str] = None  # explanation

class TestExtractionRequest(BaseModel):
    final_prompt: str
    file_content: str

class TestExtractionResponse(BaseModel):
    extraction_result: str



# Helper LLM Calls - These are supposed to be the tools of the agent. In a finished app they will have to be setup as real tools that the agent can access.
def classify_document_type(extraction_task: str) -> str:
    """
    Call the OpenAI Responses API with the doc_classification.yaml prompt.
    If more than 99% sure, returns 'invoice', 'email', 'support ticket', 'legal doc'
    Otherwise returns 'unknown'.
    """
    input_messages = [
        {
            "role": "system",
            "content": DOC_CLASS_PROMPT_TEXT.replace("{extraction_task}", extraction_task)
        }
    ]

    response = openai.responses.create(
        model="gpt-4o",
        input=input_messages,
        store=False
    )
    # The model should reply with just the doc type or "unknown"
    doc_type_raw = response.output_text.strip().lower()
    # Validate if it's one of the known types or not
    known_types = ["invoice", "email", "support ticket", "legal doc", "unknown"]
    if doc_type_raw in known_types:
        return doc_type_raw
    # If the answer is something else, we treat it as "unknown"
    return "unknown"


def generate_final_prompt(api_key: str, extraction_task: str) -> str:
    """
    Use the meta_prompt.yaml text as system instructions
    with user content as the extraction task.
    Returns the intial-prompt which can become the final prompt if not adjusted by the tools.
    """
    # 1) Set user's own OpenAI API key. IT IS NOT STORED ANYWHERE BUT ONLY USED AT RUNTIME WITH EACH REQUEST.

    user_api_key = api_key.strip()
    if not user_api_key:
        raise HTTPException(status_code=400, detail="Invalid OpenAI API key")

    openai.api_key = user_api_key

    user_task = extraction_task


    input_messages = [
        {"role": "system", "content": META_PROMPT_TEXT},
        {"role": "user", "content": f"Task: {user_task}"}
    ]

    print(META_PROMPT_TEXT)

    response = openai.responses.create(
        model="gpt-4o",
        input=input_messages,
        store=False
    )

    final_prompt = response.output_text.strip()
    return final_prompt


def domain_check_llm_call(
    doc_type: str,
    extraction_prompt: str,
    user_request: str
) -> (str, str):
    """
    Calls the specialized domain check (which can also fix the prompt).
    Returns (check_result, check_reason, adjusted_prompt). These parameters will be then useful during any debugging process.
    """
    if doc_type == "invoice":
        check_prompt = INVOICE_CHECK_TEXT
    elif doc_type == "email":
        check_prompt = EMAIL_CHECK_TEXT
    elif doc_type == "support ticket":
        check_prompt = SUPPORT_TICKET_CHECK_TEXT
    elif doc_type == "legal doc":
        check_prompt = LEGAL_DOC_CHECK_TEXT
    else:
        #At the moment edge use cases are ignored but can be included along the way.
        return ("NotNeeded", "No domain check for unknown doc type")

    # Fill placeholders
    check_prompt_filled = check_prompt.replace("{user_request}", user_request)\
                                      .replace("{extraction_prompt}", extraction_prompt)

    input_messages = [
        {"role": "system", "content": check_prompt_filled}
    ]

    response = openai.responses.create(
        model="gpt-4o",
        input=input_messages,
        store=False
    )

    result_text = response.output_text.strip()
    # Expected JSON: {"status": "...", "explanation": "...", "adjustedPrompt": "..."}
    # "status" and "explanation" help us debugg errors in the backend.
    try:
        data = json.loads(result_text)
        status = data.get("status", "Fail")
        explanation = data.get("explanation", "No explanation.")
        adjusted = data.get("adjustedPrompt", extraction_prompt)
    except:
        # If parse fails, treat it as "Fail"
        status = "Fail"
        explanation = f"Could not parse JSON from domain tool: {result_text}"
        adjusted = extraction_prompt

    return (status, explanation, adjusted)


def test_extraction_llm_call(final_prompt: str, file_content: str) -> str:
    """
    Local test function: feed the final system prompt + the actual file_content to GPT-4o
    to see what extraction result it returns. 
    """

    input_messages = [
        {"role": "system", "content": final_prompt},
        {"role": "user", "content": file_content}
    ]

    response = openai.responses.create(
        model="gpt-4o",
        input=input_messages,
        store=False
    )
    return response.output_text


########################
# FastAPI Endpoints
########################

@app.post("/generate_prompt", response_model=GeneratePromptResponse)
def generate_prompt_endpoint(payload: GeneratePromptRequest):
    """
    1) Try to infer doc type from user's task.
    2) Generate initial prompt with meta prompt.
    3) If doc type recognized, then domain check + fix if "Fail".
    4) Return final (meaning the initially created prompt) or adjusted prompt (fixed by the tools) in response.
    """

    # NOT USED ANYMORE. doc_type is irrelevant. Code must be cleaned. A) Determine doc type
    # identified_doc_type = "unknown"
    # if payload.doc_type:
    #     # If user already provides doc_type, we trust it. 
    #     # Or we could also double-check with classification if you prefer.
    #     identified_doc_type = payload.doc_type.lower()
    # else:
        # call classification logic
    classification = classify_document_type(payload.extraction_task)
    identified_doc_type = classification

    # B) Generate final prompt
    final_prompt = generate_final_prompt(payload.api_key, payload.extraction_task)

    # C) If doc type is one of the known, call domain check
    # check_result = None
    # check_reason = None
    known_types = ["invoice", "email", "support ticket", "legal doc"]
    check_result = "NotNeeded"
    check_reason = None
    adjusted_prompt = None

    if identified_doc_type in known_types:
        (check_result, check_reason, possible_fix) = domain_check_llm_call(
            doc_type=identified_doc_type,
            extraction_prompt=final_prompt,
            user_request=payload.extraction_task
        )

        # If "Fail", adopt the partially fixed prompt
        if check_result == "Fail":
            adjusted_prompt = possible_fix
            final_prompt = possible_fix
        elif check_result == "Pass":
            adjusted_prompt = None
        # otherwise "Fail", "Pass", or "NotNeeded" is returned from the domain tool
    else:
        check_result = "NotNeeded"
        check_reason = "Doc type is unknown or not in recognized list."

    return GeneratePromptResponse(
        final_prompt=final_prompt,
        identified_doc_type=identified_doc_type,
        check_result=check_result,
        check_reason=check_reason,
        adjusted_prompt=adjusted_prompt
    )

    # if identified_doc_type in known_types:
    #     (check_result, check_reason, possible_fix) = domain_check_llm_call(
    #         doc_type=identified_doc_type, #NOT USED ANYMORE
    #         extraction_prompt=final_prompt,
    #         user_request=payload.extraction_task
    #     )
    # else:
    #     check_result = "NotNeeded"
    #     check_reason = "Doc type is unknown or below 99% confidence. No domain check."

    # return GeneratePromptResponse(
    #     final_prompt=final_prompt,
    #     identified_doc_type=identified_doc_type,
    #     check_result=check_result,
    #     check_reason=check_reason
    # )


@app.post("/test_extraction", response_model=TestExtractionResponse)
def test_extraction_endpoint(payload: TestExtractionRequest):
    """
    Provide the final_prompt (from /generate_prompt) 
    plus some sample file_content to see how GPT-4o performs real extraction. It is only an endpoint used for testing purposes.
    """
    extraction_result = test_extraction_llm_call(payload.final_prompt, payload.file_content)
    return TestExtractionResponse(extraction_result=extraction_result)


# Endpoint to list all available routes
@app.get("/", response_model=List[dict])
def get_all_routes():
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "name": route.name,
            "methods": list(route.methods)
        })
    return routes


# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
