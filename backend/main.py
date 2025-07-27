from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import logging
from app.services.image_analyzer import ImageAnalyzer
from app.services.prompt_generator import PromptGenerator
from app.models.analysis_models import AnalysisResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Image AI - Advanced Webpage Scanner & Analyzer",
    description="AI-powered image analysis tool for website screenshots",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the image analyzer and prompt generator
analyzer = ImageAnalyzer()
prompt_generator = PromptGenerator()

class PromptGenerationRequest(BaseModel):
    analysis: dict

@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {"message": "Image AI Backend is running!", "status": "healthy"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Image AI API"}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze uploaded image and return detailed description
    
    Args:
        file: Uploaded image file (PNG, JPG, SVG)
        
    Returns:
        Detailed analysis including layout, colors, typography, etc.
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Please upload an image file (PNG, JPG, SVG)."
            )
        
        # Read file content
        content = await file.read()
        
        # Analyze the image
        analysis_result = await analyzer.analyze_image(content, file.filename)
        
        logger.info(f"Successfully analyzed image: {file.filename}")
        
        return analysis_result
        
    except Exception as e:
        logger.error(f"Error analyzing image {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing image: {str(e)}"
        )

@app.post("/api/generate-prompt", response_model=AnalysisResponse)
async def generate_prompt(request: PromptGenerationRequest):
    """
    Generate a comprehensive prompt from existing analysis data
    
    Args:
        request: Analysis data to generate prompt from
        
    Returns:
        Updated analysis with generated prompt
    """
    try:
        # Convert request data to AnalysisResponse
        analysis_data = request.analysis
        
        # Create AnalysisResponse object from the data
        analysis = AnalysisResponse(**analysis_data)
        
        # Generate the prompt
        generated_prompt = prompt_generator.generate_full_prompt(analysis)
        
        # Update the analysis with the generated prompt
        analysis.generated_prompt = generated_prompt
        
        logger.info("Successfully generated prompt")
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error generating prompt: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating prompt: {str(e)}"
        )

@app.get("/api/docs")
async def custom_docs():
    """Custom documentation endpoint"""
    return {
        "message": "Visit /docs for Swagger UI documentation",
        "swagger_ui": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
