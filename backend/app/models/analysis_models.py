from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class ElementType(str, Enum):
    """Types of UI elements that can be detected"""
    HEADER = "header"
    NAVBAR = "navbar"
    SIDEBAR = "sidebar"
    FOOTER = "footer"
    BUTTON = "button"
    INPUT = "input"
    FORM = "form"
    CARD = "card"
    IMAGE = "image"
    TEXT = "text"
    ICON = "icon"
    CONTAINER = "container"

class LayoutType(str, Enum):
    """CSS layout types"""
    FLEXBOX = "flexbox"
    GRID = "grid"
    BLOCK = "block"
    INLINE = "inline"
    ABSOLUTE = "absolute"
    RELATIVE = "relative"

class ColorInfo(BaseModel):
    """Color information with context"""
    hex_code: str
    rgb: tuple[int, int, int]
    usage_context: str
    element_type: str
    confidence: float = 0.0

class Typography(BaseModel):
    """Typography information"""
    font_family: str
    font_size: str
    font_weight: str
    color: str
    text_content: str
    element_type: str
    alignment: str
    line_height: Optional[str] = None
    letter_spacing: Optional[str] = None

class InteractiveElement(BaseModel):
    """Interactive UI element details"""
    element_type: ElementType
    position: Dict[str, Any]
    dimensions: Dict[str, Any]
    styling: Dict[str, Any]
    states: Optional[Dict[str, Any]] = None
    text_content: Optional[str] = None

class Asset(BaseModel):
    """Image, icon, or SVG asset information"""
    asset_type: str
    dimensions: Dict[str, int]
    position: Dict[str, Any]
    alt_text_intent: Optional[str] = None
    file_format: Optional[str] = None

class LayoutStructure(BaseModel):
    """Layout structure information"""
    layout_type: LayoutType
    grid_structure: Optional[str] = None
    flexbox_properties: Optional[Dict[str, Any]] = None
    spacing: Dict[str, str]
    alignment: str
    responsive_hints: Optional[List[str]] = None

class GlobalStyles(BaseModel):
    """Global styling information"""
    borders: Dict[str, str]
    shadows: Dict[str, str]
    border_radius: Dict[str, str]
    breakpoints: Optional[Dict[str, str]] = None
    css_variables: Optional[Dict[str, str]] = None

class StyleGuide(BaseModel):
    """Extracted style guide"""
    primary_colors: List[str]
    secondary_colors: List[str]
    font_stack: List[str]
    spacing_scale: List[str]
    design_tokens: Dict[str, Any]

class GeneratedPrompt(BaseModel):
    """Generated markdown prompt for recreating the design"""
    title: str
    description: str
    full_prompt: str
    sections: Dict[str, str]
    metadata: Dict[str, Any]

class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    # Core analysis sections
    layout: LayoutStructure
    colors: List[ColorInfo]
    typography: List[Typography]
    interactive_elements: List[InteractiveElement]
    assets: List[Asset]
    global_styles: GlobalStyles
    
    # Advanced features
    style_guide: StyleGuide
    component_labels: Dict[str, str]
    generated_prompt: Optional[GeneratedPrompt] = None
    
    # Metadata
    image_info: Dict[str, Any]
    processing_time: float
    confidence_score: float
    warnings: List[str] = []
    
    # Raw analysis data for debugging
    raw_data: Optional[Dict[str, Any]] = None

class AnalysisRequest(BaseModel):
    """Analysis request parameters"""
    filename: str
    include_raw_data: bool = False
    confidence_threshold: float = 0.7
    analysis_depth: str = "detailed"  # "basic", "detailed", "comprehensive"
