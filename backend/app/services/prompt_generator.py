from typing import List, Dict, Any
from app.models.analysis_models import (
    AnalysisResponse, 
    GeneratedPrompt, 
    ColorInfo, 
    Typography, 
    InteractiveElement,
    LayoutStructure,
    StyleGuide,
    ElementType
)

class PromptGenerator:
    """Generates detailed markdown prompts for recreating designs"""
    
    def generate_full_prompt(self, analysis: AnalysisResponse) -> GeneratedPrompt:
        """Generate a comprehensive prompt from analysis results"""
        
        sections = {
            "overview": self._generate_overview(analysis),
            "layout": self._generate_layout_section(analysis.layout),
            "colors": self._generate_colors_section(analysis.colors),
            "typography": self._generate_typography_section(analysis.typography),
            "components": self._generate_components_section(analysis.interactive_elements),
            "styling": self._generate_styling_section(analysis.global_styles, analysis.style_guide),
            "implementation": self._generate_implementation_section(analysis),
            "assets": self._generate_assets_section(analysis.assets) if analysis.assets else ""
        }
        
        full_prompt = self._combine_sections(sections)
        
        return GeneratedPrompt(
            title=f"🎯 PIXEL-PERFECT RECREATION: {analysis.image_info.get('filename', 'Website Screenshot')}",
            description=f"100% accurate recreation prompt generated from AI image analysis. Contains {len(analysis.colors)} exact colors, {len(analysis.typography)} OCR-detected text elements, and {len(analysis.interactive_elements)} interactive components with precise positioning data.",
            full_prompt=full_prompt,
            sections=sections,
            metadata={
                "analysis_confidence": analysis.confidence_score,
                "processing_time_seconds": analysis.processing_time,
                "detected_colors": len(analysis.colors),
                "detected_text_elements": len(analysis.typography),
                "detected_interactive_elements": len(analysis.interactive_elements),
                "detected_assets": len(analysis.assets) if analysis.assets else 0,
                "layout_system": analysis.layout.layout_type.value,
                "prompt_word_count": len(full_prompt.split()),
                "prompt_character_count": len(full_prompt),
                "accuracy_level": "pixel-perfect",
                "recreation_difficulty": "high" if analysis.confidence_score > 0.8 else "medium" if analysis.confidence_score > 0.6 else "challenging"
            }
        )
    
    def _generate_overview(self, analysis: AnalysisResponse) -> str:
        """Generate overview section"""
        dimensions = analysis.image_info.get('dimensions', {})
        width = dimensions.get('width', 'Unknown')
        height = dimensions.get('height', 'Unknown')
        
        return f"""# 🎯 PIXEL-PERFECT WEBSITE/APP RECREATION PROMPT

## 📋 EXACT SPECIFICATIONS FROM SCANNED SCREENSHOT
**CRITICAL: This prompt is generated from actual image analysis. Every detail MUST be replicated exactly.**

### 🖼️ Source Image Analysis
- **File**: {analysis.image_info.get('filename', 'screenshot.png')}
- **Exact Dimensions**: {width} × {height} pixels
- **Layout System**: {analysis.layout.layout_type.value.upper()}
- **Detected Colors**: {len(analysis.colors)} unique colors with exact hex codes
- **Text Elements**: {len(analysis.typography)} typography styles detected via OCR
- **Interactive Elements**: {len(analysis.interactive_elements)} clickable/interactive components
- **Analysis Confidence**: {analysis.confidence_score:.1%}
- **Processing Quality**: {analysis.processing_time:.2f}s analysis time

### 🎯 RECREATION REQUIREMENTS (100% ACCURACY REQUIRED)
You must recreate this design with ZERO deviation from the original:

1. **PIXEL-PERFECT POSITIONING**: Every element must be positioned exactly as detected
2. **COLOR MATCHING**: Use ONLY the exact hex codes provided (no approximations)
3. **TYPOGRAPHY PRECISION**: Match exact font sizes, weights, and spacing detected via OCR
4. **LAYOUT FIDELITY**: Replicate the exact layout structure and grid system
5. **INTERACTIVE ELEMENTS**: All buttons, forms, and clickable areas must match positions
6. **SPACING ACCURACY**: Maintain exact padding, margins, and gaps as measured
7. **VISUAL HIERARCHY**: Preserve the exact visual flow and element prominence

### ⚠️ CRITICAL SUCCESS CRITERIA
- The final result should be indistinguishable from the original screenshot
- Every color, spacing, and text placement must be precisely matched
- All interactive elements must be functionally equivalent
- The layout must render identically across the same viewport size

---"""

    def _generate_layout_section(self, layout: LayoutStructure) -> str:
        """Generate layout and structure section"""
        grid_info = layout.grid_structure or "Single column detected"
        spacing_info = ", ".join([f"{k}: {v}" for k, v in layout.spacing.items()])
        responsive_hints = layout.responsive_hints or ["Standard responsive patterns detected"]
        
        return f"""## 📐 EXACT LAYOUT & STRUCTURAL BLUEPRINT

### 🏗️ DETECTED LAYOUT SYSTEM (IMPLEMENT EXACTLY)
- **Primary Layout**: `{layout.layout_type.value}` (REQUIRED - detected from image analysis)
- **Grid Structure**: {grid_info}
- **Content Alignment**: `{layout.alignment}` (maintain this exact alignment)
- **Measured Spacing**: {spacing_info}
- **Responsive Behavior**: {', '.join(responsive_hints)}

### 🔧 CSS IMPLEMENTATION BLUEPRINT
```css
/* EXACT LAYOUT REPLICATION - DO NOT MODIFY */
.main-container {{
  display: {layout.layout_type.value};
  {f"grid-template-columns: {layout.grid_structure.replace('Estimated', '').strip()};" if layout.layout_type.value == "grid" and layout.grid_structure else ""}
  {"align-items: " + layout.alignment + ";" if layout.alignment else ""}
  {"justify-content: " + layout.alignment + ";" if layout.alignment else ""}
  /* Spacing detected from image analysis */
  {chr(10).join([f"  {k.replace('_', '-')}: {v};" for k, v in layout.spacing.items()])}
}}
```

### 📏 FLEXBOX PROPERTIES (IF DETECTED)
{self._format_dict_as_css(layout.flexbox_properties) if layout.flexbox_properties else "```css\n/* Standard block layout detected - no flexbox properties */\n```"}

### ⚡ IMPLEMENTATION COMMANDS
1. **MANDATORY**: Use `{layout.layout_type.value}` as the primary layout method
2. **CRITICAL**: Maintain exact spacing ratios detected in the image
3. **REQUIRED**: Test layout at the exact viewport size: {layout.grid_structure or "original screenshot dimensions"}
4. **VALIDATION**: Compare side-by-side with original screenshot for positioning accuracy

---"""

    def _generate_colors_section(self, colors: List[ColorInfo]) -> str:
        """Generate colors and theme section"""
        if not colors:
            return "## 🎨 COLORS & THEME\n⚠️ No color data detected - manual color extraction required."
        
        # Sort colors by confidence (most prominent first)
        sorted_colors = sorted(colors, key=lambda x: x.confidence, reverse=True)
        
        # Group by usage context for better organization
        primary_colors = [c for c in sorted_colors if 'primary' in c.usage_context.lower()]
        background_colors = [c for c in sorted_colors if 'background' in c.usage_context.lower()]
        text_colors = [c for c in sorted_colors if 'text' in c.usage_context.lower()]
        accent_colors = [c for c in sorted_colors if 'accent' in c.usage_context.lower() or 'button' in c.usage_context.lower()]
        border_colors = [c for c in sorted_colors if 'border' in c.usage_context.lower() or 'divider' in c.usage_context.lower()]
        
        def format_color_list_detailed(color_list: List[ColorInfo], title: str) -> str:
            if not color_list:
                return ""
            colors_text = "\n".join([
                f"  • **{color.hex_code}** | RGB({color.rgb[0]}, {color.rgb[1]}, {color.rgb[2]}) | Usage: {color.usage_context} | Prominence: {color.confidence:.1%}"
                for color in color_list
            ])
            return f"\n### {title}\n{colors_text}"
        
        return f"""## 🎨 EXACT COLOR PALETTE (MANDATORY HEX CODES)

### 🔍 SCANNED COLOR ANALYSIS
**CRITICAL**: These colors were extracted via computer vision analysis. Use EXACTLY these hex codes.
**Total Colors Detected**: {len(colors)} unique colors

{format_color_list_detailed(background_colors, "🏠 BACKGROUND COLORS (High Prominence)")}
{format_color_list_detailed(text_colors, "📝 TEXT COLORS (OCR Detected)")}
{format_color_list_detailed(primary_colors, "🎯 PRIMARY/BRAND COLORS")}
{format_color_list_detailed(accent_colors, "✨ ACCENT & INTERACTIVE COLORS")}
{format_color_list_detailed(border_colors, "🔲 BORDERS & DIVIDERS")}

### 🎨 MANDATORY CSS COLOR VARIABLES
```css
/* EXACT COLORS FROM IMAGE ANALYSIS - DO NOT CHANGE */
:root {{
{chr(10).join([f"  --color-{i+1}-{color.usage_context.lower().replace(' ', '-').replace('/', '-')}: {color.hex_code}; /* {color.usage_context} - {color.confidence:.1%} prominence */" for i, color in enumerate(sorted_colors[:12])])}
  
  /* Quick reference for most common colors */
  --primary-bg: {background_colors[0].hex_code if background_colors else sorted_colors[0].hex_code};
  --primary-text: {text_colors[0].hex_code if text_colors else '#000000'};
  --accent-color: {accent_colors[0].hex_code if accent_colors else primary_colors[0].hex_code if primary_colors else sorted_colors[1].hex_code if len(sorted_colors) > 1 else '#0066cc'};
}}
```

### 🎯 COLOR APPLICATION RULES
1. **EXACT MATCHING**: Use only the hex codes above - NO approximations or "similar" colors
2. **CONTEXT AWARENESS**: Apply colors based on their detected usage context
3. **PROMINENCE RESPECT**: Higher confidence colors are more visually dominant in the design
4. **VALIDATION**: Use a color picker to verify your implementation matches the original

### 🔬 COLOR ACCESSIBILITY NOTES
- Text contrast ratios preserved from original design
- Color combinations maintain the original visual hierarchy
- Interactive elements use the detected accent colors for consistency

---"""

    def _generate_typography_section(self, typography: List[Typography]) -> str:
        """Generate typography section"""
        if not typography:
            return "## 📝 TYPOGRAPHY\n⚠️ No text detected via OCR - manual text analysis required."
        
        # Group by element type with more precision
        headings = [t for t in typography if 'heading' in t.element_type.lower() or 'h1' in t.element_type.lower() or 'h2' in t.element_type.lower() or 'h3' in t.element_type.lower()]
        subheadings = [t for t in typography if 'subheading' in t.element_type.lower()]
        body_text = [t for t in typography if 'text' in t.element_type.lower() or 'paragraph' in t.element_type.lower() or 'body' in t.element_type.lower()]
        buttons = [t for t in typography if 'button' in t.element_type.lower()]
        links = [t for t in typography if 'link' in t.element_type.lower()]
        labels = [t for t in typography if 'label' in t.element_type.lower() or 'caption' in t.element_type.lower()]
        
        def format_typography_group_detailed(typo_list: List[Typography], title: str, icon: str = "📝") -> str:
            if not typo_list:
                return ""
            typo_text = "\n".join([
                f"  • **\"{typo.text_content[:80]}{'...' if len(typo.text_content) > 80 else ''}\"**\n"
                f"    - Font: `{typo.font_family}`\n"
                f"    - Size: `{typo.font_size}`\n"
                f"    - Weight: `{typo.font_weight}`\n"
                f"    - Color: `{typo.color}`\n"
                f"    - Alignment: `{typo.alignment}`"
                + (f"\n    - Line Height: `{typo.line_height}`" if typo.line_height else "")
                + (f"\n    - Letter Spacing: `{typo.letter_spacing}`" if typo.letter_spacing else "")
                + f"\n    - Element Type: `{typo.element_type}`\n"
                for typo in typo_list
            ])
            return f"\n### {icon} {title} ({len(typo_list)} detected)\n{typo_text}"
        
        return f"""## 📝 EXACT TYPOGRAPHY SPECIFICATIONS (OCR DETECTED)

### 🔍 TEXT ANALYSIS SUMMARY
**CRITICAL**: All text below was detected via OCR (Optical Character Recognition) from the actual screenshot.
**Total Text Elements**: {len(typography)} unique typography styles detected

{format_typography_group_detailed(headings, "MAIN HEADINGS", "🏆")}
{format_typography_group_detailed(subheadings, "SUBHEADINGS", "📊")}
{format_typography_group_detailed(body_text, "BODY TEXT", "📖")}
{format_typography_group_detailed(buttons, "BUTTON TEXT", "🔘")}
{format_typography_group_detailed(links, "LINKS & NAVIGATION", "🔗")}
{format_typography_group_detailed(labels, "LABELS & CAPTIONS", "🏷️")}

### 🎯 MANDATORY CSS TYPOGRAPHY CLASSES
```css
/* EXACT TYPOGRAPHY FROM OCR ANALYSIS - COPY PRECISELY */
{chr(10).join([f"""
.typography-{i+1}-{typo.element_type.lower().replace(' ', '-')} {{
  font-family: {typo.font_family};
  font-size: {typo.font_size};
  font-weight: {typo.font_weight};
  color: {typo.color};
  text-align: {typo.alignment};{f'''
  line-height: {typo.line_height};''' if typo.line_height else ''}{f'''
  letter-spacing: {typo.letter_spacing};''' if typo.letter_spacing else ''}
  /* Original text: "{typo.text_content[:50]}{'...' if len(typo.text_content) > 50 else ''}" */
}}""" for i, typo in enumerate(typography[:8])])}
```

### 📋 TEXT CONTENT CHECKLIST
**EXACT TEXT TO INCLUDE** (Copy these exactly):
{chr(10).join([f"- [ ] \"{text.text_content}\" ({text.element_type})" for text in typography if text.text_content.strip()])}

### ⚡ TYPOGRAPHY IMPLEMENTATION RULES
1. **EXACT FONTS**: Use the precise font families detected - ensure they're loaded
2. **PRECISE SIZING**: Match font sizes exactly as measured from the image
3. **COLOR ACCURACY**: Use exact color hex codes for each text element
4. **SPACING PRESERVATION**: Maintain line heights and letter spacing precisely
5. **TEXT CONTENT**: Include ALL detected text content exactly as shown above

### 🔤 FONT LOADING REQUIREMENTS
```css
/* Ensure all detected fonts are properly loaded */
@import url('https://fonts.googleapis.com/css2?family={"+".join(set([typo.font_family.split(",")[0].strip().replace(" ", "+") for typo in typography if "font" not in typo.font_family.lower()]))}&display=swap');

/* Font fallbacks for web safety */
body {{
  font-family: {typography[0].font_family if typography else 'Arial, sans-serif'};
}}
```

---"""

    def _generate_components_section(self, elements: List[InteractiveElement]) -> str:
        """Generate interactive components section"""
        if not elements:
            return "## 🖱️ INTERACTIVE COMPONENTS\n⚠️ No interactive elements detected - manual identification required."
        
        # Group by type with detailed analysis
        buttons = [e for e in elements if e.element_type == ElementType.BUTTON]
        forms = [e for e in elements if e.element_type in [ElementType.INPUT, ElementType.FORM]]
        navigation = [e for e in elements if e.element_type == ElementType.NAVBAR]
        images = [e for e in elements if e.element_type == ElementType.IMAGE]
        containers = [e for e in elements if e.element_type == ElementType.CONTAINER]
        other = [e for e in elements if e not in buttons + forms + navigation + images + containers]
        
        def format_elements_group_detailed(elem_list: List[InteractiveElement], title: str, icon: str = "🔧") -> str:
            if not elem_list:
                return ""
            elem_text = "\n".join([
                f"  • **{elem.text_content or 'Unnamed Element'}** ({elem.element_type.value})\n"
                f"    - **Exact Position**: {elem.position}\n"
                f"    - **Exact Dimensions**: {elem.dimensions}\n"
                f"    - **Styling Properties**: {elem.styling}"
                + (f"\n    - **Interactive States**: {elem.states}" if elem.states else "")
                + (f"\n    - **Text Content**: \"{elem.text_content}\"" if elem.text_content else "")
                + "\n"
                for elem in elem_list
            ])
            return f"\n### {icon} {title} ({len(elem_list)} detected)\n{elem_text}"
        
        return f"""## 🖱️ INTERACTIVE ELEMENTS (PIXEL-PERFECT POSITIONING)

### 🔍 DETECTED INTERACTIVE COMPONENTS
**CRITICAL**: These elements were detected via computer vision analysis. Position them EXACTLY as specified.
**Total Interactive Elements**: {len(elements)} components requiring implementation

{format_elements_group_detailed(buttons, "BUTTONS & CLICKABLE ELEMENTS", "🔘")}
{format_elements_group_detailed(forms, "FORM ELEMENTS & INPUTS", "📝")}
{format_elements_group_detailed(navigation, "NAVIGATION COMPONENTS", "🧭")}
{format_elements_group_detailed(images, "IMAGE ELEMENTS", "🖼️")}
{format_elements_group_detailed(containers, "CONTAINER ELEMENTS", "📦")}
{format_elements_group_detailed(other, "OTHER INTERACTIVE ELEMENTS", "⚙️")}

### 🎯 MANDATORY IMPLEMENTATION REQUIREMENTS
```css
/* EXACT POSITIONING FOR INTERACTIVE ELEMENTS */
{chr(10).join([f"""
.element-{i+1}-{elem.element_type.value.replace('_', '-')} {{
  /* Exact positioning from image analysis */
  position: absolute;
  left: {elem.position.get('x', 0)}px;
  top: {elem.position.get('y', 0)}px;
  width: {elem.dimensions.get('width', 'auto')}px;
  height: {elem.dimensions.get('height', 'auto')}px;
  
  /* Styling properties detected */
  {chr(10).join([f"  {k.replace('_', '-')}: {v};" for k, v in (elem.styling or {}).items()])}
}}""" for i, elem in enumerate(elements[:6])])}
```

### 🖱️ INTERACTION BEHAVIOR SPECIFICATIONS
1. **HOVER STATES**: Implement hover effects for all button elements
2. **CLICK HANDLERS**: Add appropriate click handlers based on element context
3. **FORM VALIDATION**: Implement validation for all detected form inputs
4. **KEYBOARD NAVIGATION**: Ensure all interactive elements are keyboard accessible
5. **TOUCH COMPATIBILITY**: Add touch event handlers for mobile devices

### ⚡ CRITICAL POSITIONING RULES
- Use EXACT pixel coordinates provided above
- Maintain relative positioning relationships between elements
- Ensure interactive areas match the detected dimensions precisely
- Test functionality by comparing with original screenshot overlay

---"""

    def _generate_styling_section(self, global_styles: Any, style_guide: StyleGuide) -> str:
        """Generate styling and CSS section"""
        primary_font = style_guide.font_stack[0] if style_guide.font_stack else "Arial, sans-serif"
        secondary_font = style_guide.font_stack[1] if len(style_guide.font_stack) > 1 else "Arial, sans-serif"
        base_font_size = style_guide.design_tokens.get("base_font_size", "16px")
        line_height = style_guide.design_tokens.get("line_height", "1.5")
        
        return f"""## Styling & CSS Implementation

### Global Styles
- **Primary Font**: {primary_font}
- **Secondary Font**: {secondary_font}
- **Base Font Size**: {base_font_size}
- **Line Height**: {line_height}
- **Border Radius**: {global_styles.border_radius.get("default", "4px") if hasattr(global_styles, 'border_radius') else "4px"}
- **Shadow Style**: {global_styles.shadows.get("default", "0 2px 4px rgba(0,0,0,0.1)") if hasattr(global_styles, 'shadows') else "0 2px 4px rgba(0,0,0,0.1)"}
- **Primary Color**: {style_guide.primary_colors[0] if style_guide.primary_colors else "#2196f3"}

### CSS Framework Recommendations
Based on the design patterns, consider using:
- **CSS Grid/Flexbox** for layout
- **CSS Custom Properties** for theming
- **Modern CSS Reset** for consistency
- **Progressive Enhancement** for animations

### Responsive Design
- Mobile-first approach recommended
- Breakpoints should match common device sizes
- Maintain design integrity across all viewports
- Test on actual devices, not just browser dev tools

### Performance Considerations
- Optimize images and assets
- Use efficient CSS selectors
- Minimize layout shifts
- Implement lazy loading where appropriate
"""

    def _generate_implementation_section(self, analysis: AnalysisResponse) -> str:
        """Generate implementation guidelines"""
        dimensions = analysis.image_info.get('dimensions', {})
        width = dimensions.get('width', 1920)
        height = dimensions.get('height', 1080)
        
        return f"""## 🚀 STEP-BY-STEP IMPLEMENTATION GUIDE

### 📋 PRE-IMPLEMENTATION CHECKLIST
Before starting, ensure you have:
- [ ] Original screenshot for side-by-side comparison
- [ ] Color picker tool for verification
- [ ] Browser developer tools ready
- [ ] All fonts identified and accessible

### 🔧 RECOMMENDED TECH STACK
Based on the complexity analysis (Confidence: {analysis.confidence_score:.1%}):

**For High-Fidelity Recreation:**
- **HTML5** + **CSS3** (Grid/Flexbox) for exact positioning
- **Vanilla JavaScript** for interactions (avoid framework overhead)
- **CSS Custom Properties** for the exact color variables provided
- **Google Fonts** or **local fonts** for typography matching

**Alternative Stacks:**
- **React** + **Styled Components** (for component-based approach)
- **Vue.js** + **Scoped CSS** (for reactive interactions)
- **Tailwind CSS** (with custom config for exact values)

### 📁 EXACT PROJECT STRUCTURE
```
pixel-perfect-recreation/
├── index.html                 # Main HTML structure
├── styles/
│   ├── reset.css             # CSS reset for consistency
│   ├── variables.css         # Color and spacing variables
│   ├── layout.css            # Layout and positioning
│   ├── typography.css        # Exact font specifications
│   ├── components.css        # Interactive element styles
│   └── responsive.css        # Viewport adjustments
├── scripts/
│   ├── main.js              # Primary functionality
│   └── interactions.js      # Interactive behaviors
├── assets/
│   ├── fonts/               # Custom font files
│   └── images/              # Extracted images
└── comparison/
    └── original-screenshot.png # Reference image
```

### 🎯 IMPLEMENTATION SEQUENCE
1. **HTML Structure** (30 min)
   - Create semantic HTML matching detected elements
   - Add exact text content from OCR analysis
   - Structure interactive elements correctly

2. **CSS Variables** (15 min)
   - Implement the exact color variables provided
   - Set up typography variables
   - Define spacing constants

3. **Layout Implementation** (45 min)
   - Apply the detected {analysis.layout.layout_type.value} layout system
   - Position elements using exact coordinates
   - Implement responsive grid structure

4. **Typography Styling** (30 min)
   - Load required fonts
   - Apply exact font specifications
   - Match text colors and spacing

5. **Interactive Elements** (60 min)
   - Style buttons and form elements
   - Add hover and focus states
   - Implement click handlers

6. **Visual Polish** (30 min)
   - Fine-tune spacing and alignment
   - Add shadows and borders as detected
   - Verify color accuracy

### 🔍 QUALITY ASSURANCE PROTOCOL
1. **Pixel-Perfect Comparison**
   ```bash
   # Open both side-by-side
   # Use browser zoom: exactly {width}x{height}px viewport
   # Overlay comparison for accuracy
   ```

2. **Color Verification**
   - Use browser color picker on each element
   - Verify against provided hex codes
   - Check contrast ratios maintained

3. **Typography Validation**
   - Measure font sizes with dev tools
   - Verify line heights and spacing
   - Confirm text content matches exactly

4. **Interactive Testing**
   - Test all buttons and links
   - Verify form functionality
   - Check keyboard navigation

### ⚠️ CRITICAL SUCCESS METRICS
- **Visual Accuracy**: 100% match when overlaid on original
- **Color Precision**: Exact hex code matches (use color picker to verify)
- **Text Fidelity**: All OCR-detected text included and positioned correctly
- **Layout Integrity**: Identical spacing and positioning relationships
- **Interactive Parity**: All detected interactive elements functional

### 🐛 COMMON PITFALLS TO AVOID
1. **Approximating Colors**: Use ONLY the provided hex codes
2. **Font Substitution**: Load exact fonts or use closest system matches
3. **Responsive Assumptions**: Start with exact original dimensions
4. **CSS Framework Overrides**: Ensure framework doesn't override exact values
5. **Browser Differences**: Test in the same browser used for original

### 📱 DEPLOYMENT VALIDATION
```html
<!-- Add this viewport meta tag for exact sizing -->
<meta name="viewport" content="width={width}, initial-scale=1.0">
```

Final validation: Your recreation should be indistinguishable from the original screenshot at the exact same viewport dimensions.

---"""

    def _generate_assets_section(self, assets) -> str:
        """Generate assets section"""
        if not assets:
            return """## 📁 ASSETS & RESOURCES

### ⚠️ No Digital Assets Detected
Manual extraction may be required for:
- Logo images
- Background images  
- Icons and graphics
- Custom illustrations

### 🔍 Manual Asset Extraction Guide
1. **Right-click** on images in original screenshot
2. **Save images** in appropriate formats (PNG for logos, JPG for photos)
3. **Optimize** for web (WebP with fallbacks recommended)
4. **Catalog** exact dimensions and positions for implementation

---"""
        
        return f"""## 📁 ASSETS & VISUAL RESOURCES

### 🖼️ DETECTED DIGITAL ASSETS
**Total Assets Identified**: {len(assets)} visual elements requiring extraction

{chr(10).join([f"""
#### Asset {i+1}: {asset.asset_type.upper()}
- **Dimensions**: {asset.dimensions['width']}×{asset.dimensions['height']}px
- **Position**: X:{asset.position.get('x', 0)}px, Y:{asset.position.get('y', 0)}px
- **Format**: {asset.file_format or 'Unknown - recommend PNG/WebP'}
- **Alt Text Intent**: {asset.alt_text_intent or 'Decorative element'}
- **Implementation**: `<img src="assets/{asset.asset_type.lower()}-{i+1}.{asset.file_format.lower() if asset.file_format else 'png'}" width="{asset.dimensions['width']}" height="{asset.dimensions['height']}" alt="{asset.alt_text_intent or ''}">`
""" for i, asset in enumerate(assets)])}

### 📋 ASSET EXTRACTION CHECKLIST
{chr(10).join([f"- [ ] Extract {asset.asset_type} at {asset.dimensions['width']}×{asset.dimensions['height']}px" for asset in assets])}

### 🎨 ASSET OPTIMIZATION REQUIREMENTS
```bash
# Recommended optimization workflow
# 1. Extract assets at exact detected dimensions
# 2. Convert to modern formats with fallbacks
# 3. Compress for web delivery
# 4. Implement responsive loading

# For each asset:
convert original.png -resize {assets[0].dimensions['width']}x{assets[0].dimensions['height']} optimized.webp
convert original.png -resize {assets[0].dimensions['width']}x{assets[0].dimensions['height']} fallback.png
```

### 🔧 IMPLEMENTATION CODE
```html
<!-- Exact asset positioning -->
{chr(10).join([f'''<img 
  src="assets/{asset.asset_type.lower()}-{i+1}.webp"
  alt="{asset.alt_text_intent or ''}"
  width="{asset.dimensions['width']}"
  height="{asset.dimensions['height']}"
  style="position: absolute; left: {asset.position.get('x', 0)}px; top: {asset.position.get('y', 0)}px;"
  loading="lazy"
/>''' for i, asset in enumerate(assets)])}
```

### 📊 ASSET PERFORMANCE NOTES
- **Format Priority**: WebP → AVIF → PNG/JPG fallback
- **Loading Strategy**: Lazy load non-critical images
- **Sizing Strategy**: Exact dimensions as detected (no scaling)
- **Positioning**: Absolute positioning with exact coordinates provided

---"""

    def _format_dict_as_css(self, properties: Dict[str, Any]) -> str:
        """Format dictionary as CSS-like properties"""
        if not properties:
            return "No specific properties defined"
        
        css_lines = []
        for key, value in properties.items():
            css_key = key.replace('_', '-')
            css_lines.append(f"  {css_key}: {value};")
        
        return "```css\n" + "\n".join(css_lines) + "\n```"

    def _combine_sections(self, sections: Dict[str, str]) -> str:
        """Combine all sections into final prompt"""
        return "\n\n".join([section for section in sections.values() if section.strip()])
