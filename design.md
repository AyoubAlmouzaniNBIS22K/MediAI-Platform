# Medical AI Diagnosis Platform - Design Style Guide

## Design Philosophy

### Visual Language
**Clinical Precision meets Modern Technology**: The design embodies the intersection of medical expertise and cutting-edge AI. Clean, minimal interfaces prioritize functionality while maintaining visual sophistication. Every element serves a purpose in the diagnostic workflow.

### Color Palette
**Primary Colors**:
- **Medical Blue**: #2563eb (Primary actions, trust, reliability)
- **Clinical White**: #ffffff (Clean backgrounds, medical sterility)
- **Diagnostic Teal**: #0891b2 (Secondary elements, data visualization)

**Accent Colors**:
- **Success Green**: #059669 (Positive diagnoses, completed tasks)
- **Warning Amber**: #d97706 (Attention needed, moderate risk)
- **Alert Red**: #dc2626 (Critical findings, errors)
- **Neutral Gray**: #64748b (Text, secondary information)

**Data Visualization Palette** (All under 50% saturation):
- **Chart Blue**: #7dd3fc
- **Chart Green**: #86efac  
- **Chart Orange**: #fcd34d
- **Chart Purple**: #c4b5fd

### Typography
**Primary Font**: Inter (Clean, medical-grade readability)
- **Headings**: Inter Bold, 24-32px for main titles
- **Subheadings**: Inter Semibold, 18-20px for sections
- **Body Text**: Inter Regular, 14-16px for content
- **Data Labels**: Inter Medium, 12-14px for metrics

**Secondary Font**: JetBrains Mono (For technical data, code, metrics)
- **AI Predictions**: 16-18px for confidence scores
- **Technical Data**: 12-14px for system information

## Visual Effects & Styling

### Background Treatment
**Subtle Medical Pattern**: Light geometric grid pattern reminiscent of medical charts, with opacity at 5% to maintain readability while adding professional context.

### Interactive Elements
**Button Styles**:
- Primary: Medical Blue with subtle shadow and hover lift effect
- Secondary: White with blue border and hover background change
- Danger: Alert Red with confirmation states

**Card Design**:
- Clean white cards with subtle shadows
- 8px border radius for modern feel
- Hover effects with gentle lift and shadow expansion

### Animation Library Usage

**Anime.js Effects**:
- **Metric Counters**: Animated number counting for dashboard statistics
- **Progress Indicators**: Smooth progress bar animations
- **Card Transitions**: Staggered loading animations for patient cards
- **Button Interactions**: Subtle scale and color transitions

**ECharts.js Visualizations**:
- **Model Performance Charts**: Line charts for accuracy over time
- **Patient Flow Analytics**: Bar charts for daily processing metrics
- **Confusion Matrix**: Heatmap visualization with medical color coding
- **ROC Curves**: Precision-recall curves with interactive tooltips

**p5.js Creative Elements**:
- **AI Neural Network Visualization**: Subtle animated background representing AI processing
- **Data Flow Animation**: Particle system showing data processing pipeline

**Splitting.js Text Effects**:
- **Loading States**: Character-by-character reveal for AI analysis results
- **Header Animations**: Staggered letter appearance for main headings

### Header & Navigation Effects
**Navigation Bar**:
- Fixed position with subtle backdrop blur
- Smooth color transitions on scroll
- Active state indicators with medical blue underline

**Logo Treatment**:
- Clean, medical-inspired icon with AI elements
- Subtle pulse animation to indicate system activity

### Interactive Component Styling

**Image Upload Zone**:
- Dashed border with medical blue accent
- Drag-over state with gentle glow effect
- Upload progress with animated fill

**AI Prediction Display**:
- Confidence meters with smooth gauge animations
- Color-coded results based on medical urgency
- Expandable sections with slide transitions

**Patient Cards**:
- Grid layout with hover lift effects
- Status indicators with color-coded dots
- Expandable details with smooth accordion animation

**Data Tables**:
- Alternating row colors for readability
- Sortable headers with clear visual indicators
- Hover states for row selection

### Responsive Design Considerations
- Mobile-first approach with touch-friendly interactions
- Tablet optimization for clinical environments
- Desktop layout maximizing screen real estate for data
- Consistent spacing and typography across all devices

### Accessibility Features
- High contrast ratios for medical compliance
- Keyboard navigation support
- Screen reader friendly markup
- Color-blind friendly chart palettes
- Focus indicators for all interactive elements

### Loading & Feedback States
- Skeleton screens for data loading
- Progress indicators for AI processing
- Success/error states with clear messaging
- Subtle pulse animations for real-time updates