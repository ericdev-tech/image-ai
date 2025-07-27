export interface GeneratedPrompt {
  title: string;
  description: string;
  full_prompt: string;
  sections: Record<string, string>;
  metadata: Record<string, any>;
}

export interface AnalysisResponse {
  layout: LayoutStructure;
  colors: ColorInfo[];
  typography: Typography[];
  interactive_elements: InteractiveElement[];
  assets: Asset[];
  global_styles: GlobalStyles;
  style_guide: StyleGuide;
  component_labels: Record<string, string>;
  generated_prompt?: GeneratedPrompt;
  image_info: ImageInfo;
  processing_time: number;
  confidence_score: number;
  warnings: string[];
  raw_data?: Record<string, any>;
}

export interface LayoutStructure {
  layout_type: 'flexbox' | 'grid' | 'block' | 'inline' | 'absolute' | 'relative';
  grid_structure?: string;
  flexbox_properties?: Record<string, any>;
  spacing: Record<string, string>;
  alignment: string;
  responsive_hints?: string[];
}

export interface ColorInfo {
  hex_code: string;
  rgb: [number, number, number];
  usage_context: string;
  element_type: string;
  confidence: number;
}

export interface Typography {
  font_family: string;
  font_size: string;
  font_weight: string;
  color: string;
  text_content: string;
  element_type: string;
  alignment: string;
  line_height?: string;
  letter_spacing?: string;
}

export interface InteractiveElement {
  element_type: 'header' | 'navbar' | 'sidebar' | 'footer' | 'button' | 'input' | 'form' | 'card' | 'image' | 'text' | 'icon' | 'container';
  position: Record<string, any>;
  dimensions: Record<string, any>;
  styling: Record<string, any>;
  states?: Record<string, any>;
  text_content?: string;
}

export interface Asset {
  asset_type: string;
  dimensions: Record<string, number>;
  position: Record<string, any>;
  alt_text_intent?: string;
  file_format?: string;
}

export interface GlobalStyles {
  borders: Record<string, string>;
  shadows: Record<string, string>;
  border_radius: Record<string, string>;
  breakpoints?: Record<string, string>;
  css_variables?: Record<string, string>;
}

export interface StyleGuide {
  primary_colors: string[];
  secondary_colors: string[];
  font_stack: string[];
  spacing_scale: string[];
  design_tokens: Record<string, any>;
}

export interface ImageInfo {
  filename: string;
  dimensions: {
    width: number;
    height: number;
  };
  channels: number;
  format: string;
}
