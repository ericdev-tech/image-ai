# Image AI - Advanced Webpage Scanner & Analyzer

A powerful AI-driven web application that analyzes uploaded website screenshots and generates hyper-detailed, precise textual descriptions of UI designs. This tool enables perfect recreation of webpage layouts, colors, typography, and interactive elements.

## 🚀 Features

- **Image Upload & Analysis**: Support for PNG, JPG, SVG files
- **Layout Detection**: Semantic UI section analysis with CSS Grid/Flexbox mapping
- **Color Extraction**: Precise HEX/RGB color identification for all elements
- **Typography Analysis**: Font family, size, weight, and spacing detection
- **Interactive Elements**: Button, form, and input field state analysis
- **Asset Cataloging**: Image, icon, and SVG positioning with measurements
- **Style Guide Generation**: Automated design system extraction

## 🏗️ Architecture

### Frontend (React + TypeScript)
- Modern React 18 with TypeScript
- Tailwind CSS for styling
- File upload with drag & drop
- Real-time analysis results display
- Responsive design

### Backend (Python FastAPI)
- FastAPI for high-performance API
- OpenCV for computer vision
- Tesseract OCR for text extraction
- CNN models for layout recognition
- Color analysis algorithms

## 📋 Requirements

### Frontend
- Node.js 18+
- npm or yarn

### Backend
- Python 3.9+
- OpenCV
- Tesseract OCR
- PIL/Pillow
- FastAPI
- Uvicorn

## 🛠️ Installation

1. **Clone and setup**:
```bash
git clone <repository-url>
cd image-ai
npm run install-all
```

2. **Start development servers**:
```bash
npm run dev
```

This will start:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## 📁 Project Structure

```
image-ai/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── types/          # TypeScript types
│   │   └── utils/          # Utility functions
│   └── package.json
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Data models
│   │   └── services/       # Business logic
│   ├── main.py
│   └── requirements.txt
└── package.json            # Root package.json
```

## 🔧 API Endpoints

- `POST /api/analyze`: Upload and analyze image
- `GET /api/health`: Health check
- `GET /api/docs`: Swagger documentation

## 🎯 Usage

1. **Upload Image**: Drag & drop or select a website screenshot
2. **Analysis**: The AI processes the image using computer vision
3. **Results**: Get detailed breakdown of:
   - Layout structure
   - Color palette
   - Typography
   - Interactive elements
   - Assets and positioning
   - Global styles

## 🔍 Technical Details

The application uses advanced computer vision techniques:
- **Layout Detection**: CNN-based semantic segmentation
- **Color Extraction**: K-means clustering and histogram analysis
- **Text Recognition**: Tesseract OCR with preprocessing
- **Element Classification**: Custom trained models for UI components

## 🚀 Deployment

### Development
```bash
npm run dev
```

### Production
```bash
npm run build
# Deploy frontend to your hosting service
# Deploy backend to cloud platform (AWS, GCP, etc.)
```

## 📝 License

MIT License - see LICENSE file for details.