# Getting Started

## Quick Start

1. **Install all dependencies**:
```bash
npm run install-all
```

2. **Start both frontend and backend**:
```bash
npm run dev
```

This will start:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Manual Start

### Backend (Python FastAPI)
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (React)
```bash
cd frontend
npm start
```

## Usage

1. Open http://localhost:3000 in your browser
2. Upload a website screenshot (PNG, JPG, SVG)
3. View the detailed AI analysis results

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## Example Analysis

The tool analyzes:
- **Layout**: CSS Grid/Flexbox structure, spacing, alignment
- **Colors**: Dominant colors with HEX codes and usage context
- **Typography**: Font families, sizes, weights, and text hierarchy
- **Interactive Elements**: Buttons, forms, inputs with styling
- **Assets**: Images, icons, and visual elements
- **Style Guide**: Design tokens and component patterns

## Requirements

- Node.js 18+
- Python 3.9+
- Tesseract OCR (installed automatically)

## Troubleshooting

- If backend fails to start, check Python dependencies: `pip install -r backend/requirements.txt`
- If frontend has styling issues, ensure Tailwind CSS is properly configured
- For image analysis errors, verify Tesseract installation: `tesseract --version`
