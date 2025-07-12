from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from gpt_utils import generate_contract
from templates import nda_template
from formatter import clean_contract_text, format_contract, format_sections, is_contract_ready
from docx_exporter import export_to_docx, export_to_pdf
from rag_utils import retrieve_relevant_clauses

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

class ClauseInput(BaseModel):
    clause: str

@app.get("/")
async def home():
    return {"message": "Accordly API is live 🚀"}

@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        output = generate_contract(request.prompt)
        return {"contract": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ GPT generation failed: {str(e)}")

@app.post("/api/review-clause")
async def review_clause(data: ClauseInput):
    clause = data.clause.lower()
    if "termination" in clause and "notice" in clause:
        return {
            "result": "passed",
            "comment": "Clause includes proper notice period and termination procedures."
        }
    else:
        return {
            "result": "failed",
            "comment": "Missing termination or notice details."
        }

@app.get("/generate/nda")
async def generate_nda(
    company_1: str,
    company_2: str,
    scope: str,
    jurisdiction: str = "USA",
    effective_date: str = None
):
    try:
        rag_clauses = retrieve_relevant_clauses(scope, top_k=3)
        rag_text = "\n\n".join([c["text"] for c in rag_clauses])
        prompt = nda_template(company_1, company_2, scope, jurisdiction, effective_date, rag_text)

        raw_output = generate_contract(prompt)
        formatted_output = format_contract(raw_output)
        clauses = format_sections(formatted_output)
        is_ready = is_contract_ready(formatted_output)

        return {
            "prompt_used": prompt,
            "title": "NON-DISCLOSURE AGREEMENT",
            "contract": formatted_output,
            "clauses": clauses,
            "is_ready": is_ready,
            "effective_date": effective_date
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ NDA generation failed: {str(e)}")

@app.get("/export/nda-docx")
async def export_nda_docx(
    company_1: str,
    company_2: str,
    scope: str,
    jurisdiction: str = "USA",
    effective_date: str = None
):
    try:
        rag_clauses = retrieve_relevant_clauses(scope, top_k=3)
        rag_text = "\n\n".join([c["text"] for c in rag_clauses])
        prompt = nda_template(company_1, company_2, scope, jurisdiction, effective_date, rag_text)

        raw_output = generate_contract(prompt)
        cleaned_output = clean_contract_text(raw_output)
        formatted_output = format_contract(cleaned_output)

        file_path = export_to_docx("Non-Disclosure Agreement", formatted_output, company_1, company_2)

        return FileResponse(
            path=file_path,
            filename="Non-Disclosure-Agreement.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ DOCX export failed: {str(e)}")

@app.get("/export/nda-pdf")
async def export_nda_pdf(
    company_1: str,
    company_2: str,
    scope: str,
    jurisdiction: str = "USA",
    effective_date: str = None
):
    try:
        rag_clauses = retrieve_relevant_clauses(scope, top_k=3)
        rag_text = "\n\n".join([c["text"] for c in rag_clauses])
        prompt = nda_template(company_1, company_2, scope, jurisdiction, effective_date, rag_text)

        raw_output = generate_contract(prompt)
        cleaned_output = clean_contract_text(raw_output)
        formatted_output = format_contract(cleaned_output)

        pdf_path = export_to_pdf("Non-Disclosure Agreement", formatted_output, company_1, company_2)

        return FileResponse(
            path=pdf_path,
            filename="Non-Disclosure-Agreement.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ PDF export failed: {str(e)}")
