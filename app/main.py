"""
Herramienta de Pruebas Lógicas con Reglas de Inferencia
FastAPI Application for logical argument validation and proof generation
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List, Optional
import os
from pathlib import Path

from logic_processor import LogicProcessor
from models import ArgumentRequest, ValidationResult

# Initialize FastAPI app
app = FastAPI(
    title="Herramienta de Pruebas Lógicas",
    description="Aplicación para validación de argumentos y generación de pruebas deductivas",
    version="1.0.0"
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize logic processor
logic_processor = LogicProcessor()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, num_premises: int = 2):
    """
    Página principal con formulario para introducir argumentos
    """
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "num_premises": num_premises,
            "premises": [""] * num_premises,
            "conclusion": ""
        }
    )

@app.post("/validate", response_class=HTMLResponse)
async def validate_argument(
    request: Request,
    premises: List[str] = Form(...),
    conclusion: str = Form(...),
    action: str = Form(...)
):
    """
    Procesa y valida el argumento lógico
    """
    # Filter out empty premises
    premises = [p.strip() for p in premises if p.strip()]
    conclusion = conclusion.strip()
    
    # Handle add premise action
    if action == "add_premise":
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "num_premises": len(premises) + 1,
                "premises": premises + [""],
                "conclusion": conclusion
            }
        )
    
    # Validate input
    if not premises or not conclusion:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "num_premises": len(premises) if premises else 2,
                "premises": premises if premises else ["", ""],
                "conclusion": conclusion,
                "error": "Por favor, introduce al menos una premisa y una conclusión."
            }
        )
    
    try:
        # Process the argument
        argument_request = ArgumentRequest(premises=premises, conclusion=conclusion)
        result = await logic_processor.validate_argument(argument_request)
        
        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "premises": premises,
                "conclusion": conclusion,
                "result": result
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "num_premises": len(premises),
                "premises": premises,
                "conclusion": conclusion,
                "error": f"Error al procesar el argumento: {str(e)}"
            }
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "message": "Logic Proofs Tool is running",
        "port": os.environ.get("PORT", "8080"),
        "pythonpath": os.environ.get("PYTHONPATH", "Not set"),
        "gemini_configured": bool(os.environ.get("GEMINI_API_KEY"))
    }

@app.get("/startup")
async def startup_check():
    """Simple startup check - no dependencies"""
    return {"status": "ok", "timestamp": "2025-09-25"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Starting server on port {port}")
    print(f"🔧 Environment: {os.environ.get('PYTHONPATH', 'Not set')}")
    print(f"🔑 API Key configured: {'Yes' if os.environ.get('GEMINI_API_KEY') else 'No'}")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info",
        access_log=True,
        timeout_keep_alive=120
    )