"""
Herramienta de Pruebas Lógicas con Reglas de Inferencia
FastAPI Application for logical argument validation and proof generation
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import List, Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from logic_processor import LogicProcessor
from models import ArgumentRequest, ValidationResult

# Initialize FastAPI app
app = FastAPI(
    title="Herramienta de Pruebas Lógicas",
    description="Aplicación para validación de argumentos y generación de pruebas deductivas",
    version="1.0.0"
)

print("✅ FastAPI app initialized successfully")
print(f"🔧 PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
print(f"🔑 GEMINI_API_KEY configured: {'Yes' if os.environ.get('GEMINI_API_KEY') else 'No'}")
print(f"🌐 PORT: {os.environ.get('PORT', '8080')}")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Setup static files (only if directory exists)
static_dir = Path("static")
if static_dir.exists() and static_dir.is_dir():
    app.mount("/static", StaticFiles(directory="static"), name="static")
    print("✅ Static files directory mounted")
else:
    print("⚠️ Static directory not found, skipping static files mounting")

# Initialize logic processor
try:
    logic_processor = LogicProcessor()
    print("✅ Logic processor initialized successfully")
except Exception as e:
    print(f"⚠️ Warning: Could not initialize logic processor: {e}")
    print("📝 The app will start but may not process arguments correctly")
    logic_processor = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, num_premises: int = 2, conclusion: str = ""):
    """
    Página principal con formulario para introducir argumentos
    """
    # Ensure minimum of 2 premises always
    num_premises = max(num_premises, 2)
    
    # Extract premise parameters from query string
    premises = []
    for i in range(num_premises):
        premise = request.query_params.get(f'premise_{i}', "")
        premises.append(premise)
    
    # Fill remaining premises with empty strings if needed
    while len(premises) < num_premises:
        premises.append("")
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "num_premises": num_premises,
            "premises": premises,
            "conclusion": conclusion
        }
    )

@app.post("/validate", response_class=HTMLResponse)
async def validate_argument(
    request: Request,
    premises: List[str] = Form(...),
    conclusion: str = Form(""),
    action: str = Form(...)
):
    """
    Procesa y valida el argumento lógico
    """
    conclusion = conclusion.strip() if conclusion else ""
    
    # Handle add premise action
    if action == "add_premise":
        # Keep ALL premises exactly as they are (including empty ones)
        # Convert single spaces back to empty strings (from frontend handling)
        premises_to_preserve = [p if p.strip() != '' else "" for p in premises] if premises else []
        
        # Use RedirectResponse to avoid staying on /validate URL
        import urllib.parse
        
        # Ensure we always have at least 2 premises, then add 1 more
        new_premises_count = max(len(premises_to_preserve) + 1, 2)
        
        # Create URL parameters to preserve state  
        params = {
            'num_premises': new_premises_count,
            'conclusion': conclusion
        }
        
        # Create the full list of premises with the new empty one
        all_premises = premises_to_preserve + [""]
        
        # Ensure we have at least 2 premises total
        while len(all_premises) < new_premises_count:
            all_premises.append("")
            
        # Add ALL premises as parameters
        for i, premise in enumerate(all_premises):
            params[f'premise_{i}'] = premise if premise else ""
            
        query_string = urllib.parse.urlencode(params)
        return RedirectResponse(url=f"/?{query_string}", status_code=302)
    
    # Validate input only for validation action
    if action == "validate":
        # Convert spaces back to empty strings (from frontend handling)
        premises_converted = [p if p.strip() != '' else "" for p in premises] if premises else []
        
        # Filter out empty premises only for validation logic
        filtered_premises = [p.strip() for p in premises_converted if p.strip()]
        
        # Validate: need at least 2 premises and a conclusion
        if len(filtered_premises) < 2 or not conclusion:
            # Preserve original premises (including empty ones) for display
            original_premises = [p if p else "" for p in premises_converted]
            error_message = []
            
            if len(filtered_premises) < 2:
                if len(filtered_premises) == 0:
                    error_message.append("al menos dos premisas válidas")
                elif len(filtered_premises) == 1:
                    error_message.append("al menos una premisa adicional (mínimo 2 premisas)")
            if not conclusion:
                error_message.append("una conclusión")
                
            error_text = f"Por favor, introduce {' y '.join(error_message)}."
            
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "num_premises": len(original_premises) if original_premises else 2,
                    "premises": original_premises if original_premises else ["", ""],
                    "conclusion": conclusion,
                    "error": error_text
                }
            )
        
        # Use filtered premises for processing
        premises = filtered_premises
    
    # Only process if action is validate (this should only happen after validation passes)
    if action == "validate":
        try:
            if logic_processor is None:
                raise Exception("Logic processor not initialized - check GEMINI_API_KEY")
            
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
    else:
        # If action is not validate, redirect to home
        return RedirectResponse(url="/", status_code=302)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "message": "Logic Proofs Tool is running",
        "port": os.environ.get("PORT", "8080"),
        "logic_processor": "initialized" if logic_processor else "not_initialized",
        "gemini_configured": bool(os.environ.get("GEMINI_API_KEY"))
    }

@app.get("/startup")
async def startup_check():
    """Simple startup check - no dependencies"""
    return {"status": "ok", "timestamp": "2025-09-25"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting server on port {port}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)