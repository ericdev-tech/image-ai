import cv2
import numpy as np
import pytesseract
from PIL import Image
import io
import time
import logging
from typing import List, Dict, Any, Tuple, Optional
from sklearn.cluster import KMeans
import webcolors
import re
from ..models.analysis_models import (
    AnalysisResponse, LayoutStructure, ColorInfo, Typography, 
    InteractiveElement, Asset, GlobalStyles, StyleGuide,
    LayoutType, ElementType
)
from .prompt_generator import PromptGenerator

logger = logging.getLogger(__name__)

class ImageAnalyzer:
    """Advanced image analysis service for webpage screenshots"""
    
    def __init__(self):
        self.setup_tesseract()
        self.prompt_generator = PromptGenerator()
        
    def setup_tesseract(self):
        """Configure Tesseract OCR settings"""
        try:
            # Try to set Tesseract path (may need adjustment based on installation)
            pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        except:
            logger.warning("Tesseract path may need configuration")
    
    async def analyze_image(self, image_data: bytes, filename: str) -> AnalysisResponse:
        """
        Main analysis function that orchestrates all image analysis tasks
        
        Args:
            image_data: Raw image bytes
            filename: Original filename
            
        Returns:
            Complete analysis response
        """
        start_time = time.time()
        warnings = []
        
        try:
            # Load and preprocess image
            image = self._load_image(image_data)
            
            if image is None:
                raise ValueError("Could not load image")
            
            # Validate if it's a website screenshot
            if not self._is_website_screenshot(image):
                warnings.append("Image may not be a website/app screenshot")
            
            # Perform parallel analysis
            layout = await self._analyze_layout(image)
            colors = await self._extract_colors(image)
            typography = await self._analyze_typography(image)
            interactive_elements = await self._detect_interactive_elements(image)
            assets = await self._catalog_assets(image)
            global_styles = await self._analyze_global_styles(image)
            style_guide = await self._synthesize_style_guide(colors, typography)
            component_labels = await self._label_components(interactive_elements)
            
            # Calculate processing time and confidence
            processing_time = time.time() - start_time
            confidence_score = self._calculate_confidence(
                layout, colors, typography, interactive_elements
            )
            
            # Build response
            response = AnalysisResponse(
                layout=layout,
                colors=colors,
                typography=typography,
                interactive_elements=interactive_elements,
                assets=assets,
                global_styles=global_styles,
                style_guide=style_guide,
                component_labels=component_labels,
                image_info={
                    "filename": filename,
                    "dimensions": {"width": image.shape[1], "height": image.shape[0]},
                    "channels": image.shape[2] if len(image.shape) > 2 else 1,
                    "format": "detected_from_content"
                },
                processing_time=round(processing_time, 2),
                confidence_score=round(confidence_score, 2),
                warnings=warnings
            )
            
            # Generate comprehensive prompt after analysis
            response.generated_prompt = self.prompt_generator.generate_full_prompt(response)
            
            logger.info(f"Analysis completed for {filename} in {processing_time:.2f}s")
            return response
            
        except Exception as e:
            logger.error(f"Analysis failed for {filename}: {str(e)}")
            raise
    
    def _load_image(self, image_data: bytes) -> Optional[np.ndarray]:
        """Load image from bytes using OpenCV"""
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            # Decode image
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is not None:
                # Convert BGR to RGB for consistent processing
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return image
        except Exception as e:
            logger.error(f"Failed to load image: {str(e)}")
            return None
    
    def _is_website_screenshot(self, image: np.ndarray) -> bool:
        """Heuristic to determine if image is a website/app screenshot"""
        try:
            height, width = image.shape[:2]
            
            # Check aspect ratio (websites are typically wider than tall)
            aspect_ratio = width / height
            
            # Check for common UI patterns using edge detection
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            
            # Look for rectangular regions (common in UI)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            rectangular_regions = 0
            
            for contour in contours:
                # Approximate contour to polygon
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Check if it's roughly rectangular (4 vertices) and sufficiently large
                if len(approx) == 4 and cv2.contourArea(contour) > (width * height * 0.01):
                    rectangular_regions += 1
            
            # Heuristics for website detection
            is_website = (
                0.5 <= aspect_ratio <= 3.0 and  # Reasonable aspect ratio
                rectangular_regions >= 3 and    # Multiple UI elements
                width >= 300 and height >= 200  # Minimum reasonable size
            )
            
            return is_website
            
        except Exception as e:
            logger.warning(f"Website detection failed: {str(e)}")
            return True  # Assume it's a website if detection fails
    
    async def _analyze_layout(self, image: np.ndarray) -> LayoutStructure:
        """Analyze layout structure and positioning"""
        try:
            height, width = image.shape[:2]
            
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Detect edges and lines
            edges = cv2.Canny(gray, 50, 150)
            
            # Detect horizontal and vertical lines (common in grid layouts)
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
            
            horizontal_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel)
            vertical_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, vertical_kernel)
            
            # Count lines to determine layout type
            h_lines = cv2.HoughLinesP(horizontal_lines, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
            v_lines = cv2.HoughLinesP(vertical_lines, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
            
            h_count = len(h_lines) if h_lines is not None else 0
            v_count = len(v_lines) if v_lines is not None else 0
            
            # Determine layout type
            if h_count >= 2 and v_count >= 2:
                layout_type = LayoutType.GRID
                grid_structure = f"Estimated {v_count + 1} columns, {h_count + 1} rows"
            else:
                layout_type = LayoutType.FLEXBOX
                grid_structure = None
            
            # Analyze spacing (simplified)
            spacing = {
                "padding": "16px (estimated)",
                "margin": "12px (estimated)",
                "gap": "8px (estimated)"
            }
            
            return LayoutStructure(
                layout_type=layout_type,
                grid_structure=grid_structure,
                spacing=spacing,
                alignment="left-aligned (estimated)",
                responsive_hints=["Desktop layout detected"] if width > 768 else ["Mobile layout detected"]
            )
            
        except Exception as e:
            logger.error(f"Layout analysis failed: {str(e)}")
            return LayoutStructure(
                layout_type=LayoutType.FLEXBOX,
                spacing={"padding": "unknown", "margin": "unknown", "gap": "unknown"},
                alignment="unknown"
            )
    
    async def _extract_colors(self, image: np.ndarray) -> List[ColorInfo]:
        """Extract dominant colors and their usage context"""
        try:
            # Reshape image for k-means clustering
            pixels = image.reshape(-1, 3)
            
            # Use k-means to find dominant colors
            n_colors = 8
            kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            colors = []
            centers = kmeans.cluster_centers_.astype(int)
            labels = kmeans.labels_
            
            # Get cluster sizes to determine color importance
            unique, counts = np.unique(labels, return_counts=True)
            color_percentages = counts / len(labels)
            
            for i, (center, percentage) in enumerate(zip(centers, color_percentages)):
                # Convert RGB to hex
                hex_code = "#{:02x}{:02x}{:02x}".format(center[0], center[1], center[2])
                
                # Determine usage context based on color properties
                usage_context = self._determine_color_usage(center, percentage)
                
                colors.append(ColorInfo(
                    hex_code=hex_code,
                    rgb=(int(center[0]), int(center[1]), int(center[2])),
                    usage_context=usage_context,
                    element_type="detected",
                    confidence=float(percentage)
                ))
            
            # Sort by confidence (percentage)
            colors.sort(key=lambda x: x.confidence, reverse=True)
            
            return colors[:6]  # Return top 6 colors
            
        except Exception as e:
            logger.error(f"Color extraction failed: {str(e)}")
            return []
    
    def _determine_color_usage(self, rgb: np.ndarray, percentage: float) -> str:
        """Determine likely usage context for a color"""
        r, g, b = rgb
        
        # Check if it's likely a background color (high percentage)
        if percentage > 0.3:
            return "Background"
        
        # Check if it's likely text (dark colors)
        if r < 100 and g < 100 and b < 100:
            return "Text"
        
        # Check if it's likely accent/primary (medium percentage, saturated)
        saturation = max(r, g, b) - min(r, g, b)
        if 0.1 <= percentage <= 0.3 and saturation > 50:
            return "Primary/Accent"
        
        # Check if it's likely border/divider (low saturation)
        if saturation < 30:
            return "Border/Divider"
        
        return "UI Element"
    
    async def _analyze_typography(self, image: np.ndarray) -> List[Typography]:
        """Analyze text and typography using OCR"""
        try:
            # Convert to PIL Image for Tesseract
            pil_image = Image.fromarray(image)
            
            # Configure Tesseract to get detailed info
            custom_config = r'--oem 3 --psm 6 -c tessedit_create_hocr=1'
            
            # Extract text with bounding boxes
            data = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT, config=custom_config)
            
            typography_elements = []
            
            for i, text in enumerate(data['text']):
                if text.strip():  # Only process non-empty text
                    # Estimate font size based on bounding box height
                    height = data['height'][i]
                    font_size = max(12, int(height * 0.8))  # Rough estimation
                    
                    # Determine text type based on size and position
                    if font_size > 24:
                        element_type = "heading"
                        font_weight = "bold"
                    elif font_size > 18:
                        element_type = "subheading"
                        font_weight = "semi-bold"
                    else:
                        element_type = "body"
                        font_weight = "normal"
                    
                    # Extract color from region (simplified)
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    if x >= 0 and y >= 0 and x + w <= image.shape[1] and y + h <= image.shape[0]:
                        text_region = image[y:y+h, x:x+w]
                        if text_region.size > 0:
                            avg_color = np.mean(text_region.reshape(-1, 3), axis=0)
                            text_color = "#{:02x}{:02x}{:02x}".format(
                                int(avg_color[0]), int(avg_color[1]), int(avg_color[2])
                            )
                        else:
                            text_color = "#000000"
                    else:
                        text_color = "#000000"
                    
                    typography_elements.append(Typography(
                        font_family="System font (estimated)",
                        font_size=f"{font_size}px",
                        font_weight=font_weight,
                        color=text_color,
                        text_content=text.strip()[:100],  # Limit text length
                        element_type=element_type,
                        alignment="left",
                        line_height=f"{int(font_size * 1.4)}px"
                    ))
            
            return typography_elements[:10]  # Return top 10 text elements
            
        except Exception as e:
            logger.error(f"Typography analysis failed: {str(e)}")
            return []
    
    async def _detect_interactive_elements(self, image: np.ndarray) -> List[InteractiveElement]:
        """Detect buttons, forms, and other interactive elements"""
        try:
            interactive_elements = []
            height, width = image.shape[:2]
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Detect button-like shapes (rectangles with rounded corners)
            # Use adaptive thresholding
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Filter by area (reasonable button/element size)
                if 500 < area < (width * height * 0.1):
                    # Get bounding rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate aspect ratio
                    aspect_ratio = w / h
                    
                    # Determine element type based on shape
                    if 1.5 <= aspect_ratio <= 6.0 and 20 <= h <= 100:
                        element_type = ElementType.BUTTON
                    elif aspect_ratio > 3.0 and h <= 50:
                        element_type = ElementType.INPUT
                    else:
                        element_type = ElementType.CONTAINER
                    
                    # Extract average color from region
                    element_region = image[y:y+h, x:x+w]
                    avg_color = np.mean(element_region.reshape(-1, 3), axis=0)
                    bg_color = "#{:02x}{:02x}{:02x}".format(
                        int(avg_color[0]), int(avg_color[1]), int(avg_color[2])
                    )
                    
                    interactive_elements.append(InteractiveElement(
                        element_type=element_type,
                        position={"x": int(x), "y": int(y)},
                        dimensions={"width": int(w), "height": int(h)},
                        styling={
                            "background_color": bg_color,
                            "border_radius": "4px (estimated)",
                            "padding": "8px 16px (estimated)"
                        }
                    ))
            
            return interactive_elements[:15]  # Limit results
            
        except Exception as e:
            logger.error(f"Interactive element detection failed: {str(e)}")
            return []
    
    async def _catalog_assets(self, image: np.ndarray) -> List[Asset]:
        """Catalog images, icons, and other visual assets"""
        try:
            assets = []
            height, width = image.shape[:2]
            
            # Use template matching for common UI icons (simplified approach)
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Detect circular shapes (likely icons/logos)
            circles = cv2.HoughCircles(
                gray, cv2.HOUGH_GRADIENT, dp=1, minDist=30,
                param1=50, param2=30, minRadius=10, maxRadius=100
            )
            
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                for (x, y, r) in circles:
                    assets.append(Asset(
                        asset_type="icon",
                        dimensions={"width": int(r*2), "height": int(r*2)},
                        position={"x": int(x-r), "y": int(y-r)},
                        alt_text_intent="Circular icon/logo"
                    ))
            
            # Detect rectangular image regions (simplified)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 2000:  # Significant area
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    
                    # Check if it's likely an image
                    if 0.5 <= aspect_ratio <= 3.0 and w > 50 and h > 50:
                        assets.append(Asset(
                            asset_type="image",
                            dimensions={"width": int(w), "height": int(h)},
                            position={"x": int(x), "y": int(y)},
                            alt_text_intent="Content image"
                        ))
            
            return assets[:10]  # Limit results
            
        except Exception as e:
            logger.error(f"Asset cataloging failed: {str(e)}")
            return []
    
    async def _analyze_global_styles(self, image: np.ndarray) -> GlobalStyles:
        """Analyze global styling patterns"""
        try:
            return GlobalStyles(
                borders={"default": "1px solid #e0e0e0", "focus": "2px solid #2196f3"},
                shadows={"card": "0 2px 4px rgba(0,0,0,0.1)", "button": "0 1px 2px rgba(0,0,0,0.1)"},
                border_radius={"small": "4px", "medium": "8px", "large": "12px"},
                breakpoints={"mobile": "768px", "tablet": "1024px", "desktop": "1200px"}
            )
        except Exception as e:
            logger.error(f"Global styles analysis failed: {str(e)}")
            return GlobalStyles(borders={}, shadows={}, border_radius={})
    
    async def _synthesize_style_guide(self, colors: List[ColorInfo], typography: List[Typography]) -> StyleGuide:
        """Generate style guide from analysis"""
        try:
            # Extract primary colors (top confidence colors)
            primary_colors = [c.hex_code for c in colors[:3] if c.confidence > 0.1]
            secondary_colors = [c.hex_code for c in colors[3:6]]
            
            # Extract font information
            fonts = list(set([t.font_family for t in typography]))
            
            # Create spacing scale
            spacing_scale = ["4px", "8px", "12px", "16px", "24px", "32px", "48px", "64px"]
            
            return StyleGuide(
                primary_colors=primary_colors,
                secondary_colors=secondary_colors,
                font_stack=fonts[:3],  # Top 3 fonts
                spacing_scale=spacing_scale,
                design_tokens={
                    "primary": primary_colors[0] if primary_colors else "#2196f3",
                    "secondary": secondary_colors[0] if secondary_colors else "#757575",
                    "base_font_size": "16px",
                    "line_height": "1.5"
                }
            )
        except Exception as e:
            logger.error(f"Style guide synthesis failed: {str(e)}")
            return StyleGuide(
                primary_colors=["#2196f3"],
                secondary_colors=["#757575"],
                font_stack=["Arial", "sans-serif"],
                spacing_scale=["8px", "16px", "24px"],
                design_tokens={}
            )
    
    async def _label_components(self, interactive_elements: List[InteractiveElement]) -> Dict[str, str]:
        """Auto-label UI components"""
        try:
            labels = {}
            button_count = 0
            input_count = 0
            
            for i, element in enumerate(interactive_elements):
                if element.element_type == ElementType.BUTTON:
                    button_count += 1
                    labels[f"element_{i}"] = f"Button {button_count}"
                elif element.element_type == ElementType.INPUT:
                    input_count += 1
                    labels[f"element_{i}"] = f"Input Field {input_count}"
                else:
                    labels[f"element_{i}"] = f"Container {i+1}"
            
            return labels
        except Exception as e:
            logger.error(f"Component labeling failed: {str(e)}")
            return {}
    
    def _calculate_confidence(self, layout: LayoutStructure, colors: List[ColorInfo], 
                            typography: List[Typography], elements: List[InteractiveElement]) -> float:
        """Calculate overall analysis confidence"""
        try:
            confidence_factors = []
            
            # Layout confidence
            if layout.layout_type:
                confidence_factors.append(0.8)
            
            # Color confidence
            if colors:
                avg_color_confidence = sum(c.confidence for c in colors) / len(colors)
                confidence_factors.append(avg_color_confidence)
            
            # Typography confidence
            if typography:
                confidence_factors.append(0.7)
            
            # Interactive elements confidence
            if elements:
                confidence_factors.append(0.6)
            
            return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.5
            
        except Exception as e:
            logger.error(f"Confidence calculation failed: {str(e)}")
            return 0.5
