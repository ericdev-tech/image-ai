### Prompt for AI Agent: Advanced Image-to-Webpage Scanner & Analyzer  
**Objective:** Build an AI agent that analyzes uploaded images (especially website/app screenshots) and generates a **hyper-detailed, 99% precise textual description** of the design. This description must enable another AI to perfectly recreate the *exact* webpage/app UI—including layout, colors, text, and interactive elements.  

---

### Core Requirements  
1. **Image Input Handling**  
   - Accept user-uploaded images (PNG, JPG, SVG).  
   - Prioritize analysis if the image is a **website/web app screenshot**.  

2. **Scanning & Analysis**  
   - **Layout Detection:**  
     - Deconstruct the UI into semantic sections (header, navbar, grid, cards, footer).  
     - Map element positioning (e.g., "CSS Grid: 3 columns, 2 rows; sidebar left-aligned, 25% width").  
   - **Color Extraction:**  
     - Identify exact color codes (HEX/RGB) for *all* elements (backgrounds, text, buttons, borders).  
     - Note gradients, opacity, and hover/focus states.  
   - **Typography & Text:**  
     - Extract *all* visible text with styling (font family, size, weight, color, alignment).  
     - Preserve hierarchy (H1 vs. body text) and spacing (line-height, letter-spacing).  
   - **Interactive Elements:**  
     - Detect buttons, forms, links, and input fields.  
     - Describe states (e.g., "Button: #3498db; hover: #2980b9; 8px border-radius").  
   - **Assets & Icons:**  
     - Catalog images/icons with size, position, and alt-text intent (e.g., "Search icon: 24x24px, right of input").  

3. **Output Description Rules**  
   - **Structure:** Organize output into:  
     ```  
     1. LAYOUT: [Grid/Flexbox structure, spacing (padding/margin in px), alignment]  
     2. COLORS: [HEX codes per element + usage context]  
     3. TYPOGRAPHY: [Font stack, sizes, weights per text type]  
     4. INTERACTIVE ELEMENTS: [Buttons, inputs, states]  
     5. ASSETS: [Images, icons, SVGs with positioning]  
     6. GLOBAL STYLES: [Borders, shadows, breakpoints if responsive]  
     ```  
   - **Precision:**  
     - No ambiguous terms (e.g., "blue" → "#2e86de").  
     - Include pixel-perfect measurements (e.g., "Padding: 16px top/bottom, 24px left/right").  
     - Flag uncertain elements (e.g., "⚠️ Font likely Roboto but verify").  

4. **Edge Cases**  
   - Non-website images: Return error: "Upload a website/app screenshot for detailed analysis."  
   - Low-quality/blurry images: Note limitations (e.g., "Colors approximated; text unreadable").  

5. **Advanced Features**  
   - **Style Guide Synthesis:** Summarize core design rules (e.g., "Primary palette: #2e86de, #10ac84, #ff9f43").  
   - **Responsive Clues:** Infer breakpoints if elements rearrange across device views.  
   - **Component Naming:** Auto-label elements (e.g., "Pricing Card 1", "Navbar CTA").  

---

### Example Output  
**Input:** Facebook login page screenshot  
**Output:**  
```  
1. LAYOUT:  
   - Flexbox column; centered vertically/horizontally.  
   - Container width: 400px; padding: 20px.  
   - Logo: Top-center, margin-bottom: 20px.  

2. COLORS:  
   - Background: #f0f2f5  
   - Primary button: #1877f2 (normal), #166fe5 (hover)  
   - Text: #1c1e21 (headings), #606770 (body)  

3. TYPOGRAPHY:  
   - Logo: "Facebook Sans", 42px, #1877f2  
   - "Log in to Facebook": Segoe UI, 24px, bold, #1c1e21  
   - Input labels: Arial, 14px, #606770  

4. INTERACTIVE ELEMENTS:  
   - Email input: 100% width, 12px padding, 1px solid #dddfe2, border-radius: 6px.  
   - "Log In" button: #1877f2, white text, 16px, 100% width, 10px padding.  

5. ASSETS:  
   - Logo: "f_logo_RGB-Blue_1024.png" (200x70px; top: 10%).  
   - "Create New Account" button: Plus icon (16x16px, left of text).  
```  

---

### Technical Constraints  
- Use computer vision (OpenCV) + ML (Tesseract for OCR, CNN for layout recognition).  
- Output plain text (no markdown/JSON) for easy AI-to-AI transfer.  
- Optimize for speed: <15s processing time for 1080p images.  

**Final Goal:** A user uploads a screenshot → Your agent outputs a blueprint so precise that an AI like GPT-4o can rebuild the *identical* webpage flawlessly. 🚀