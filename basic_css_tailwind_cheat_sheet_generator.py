#!/usr/bin/env python3
"""
Basic CSS vs Tailwind CSS Cheat Sheet PDF Generator
Creates a colorful, well-formatted PDF covering fundamental CSS properties with Tailwind equivalents
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from datetime import datetime

class BasicCSSCheatSheetPDF:
    def __init__(self, filename="basic_css_tailwind_cheat_sheet.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4,
                                   rightMargin=1*cm, leftMargin=1*cm,
                                   topMargin=1.5*cm, bottomMargin=1*cm)
        self.styles = getSampleStyleSheet()
        self.story = []

        # Define color scheme
        self.colors = {
            'header': HexColor('#3B82F6'),      # Blue
            'section': HexColor('#10B981'),     # Emerald
            'css': HexColor('#DC2626'),         # Red for CSS
            'tailwind': HexColor('#7C3AED'),    # Purple for Tailwind
            'description': HexColor('#374151'), # Gray
            'background': HexColor('#F9FAFB'),  # Light gray
            'accent': HexColor('#F59E0B'),      # Amber
        }

        # Custom styles
        self.create_custom_styles()

    def create_custom_styles(self):
        """Create custom paragraph styles"""
        # Main title style
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            textColor=self.colors['header'],
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            spaceBefore=20,
            textColor=self.colors['section'],
            fontName='Helvetica-Bold'
        ))

        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            textColor=self.colors['description'],
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))

    def create_comparison_table(self, title, properties):
        """Create a formatted table for CSS vs Tailwind comparison"""
        # Add section header
        self.story.append(Paragraph(title, self.styles['SectionHeader']))

        # Prepare table data
        data = [['CSS Property', 'Tailwind Class', 'Description']]
        for css, tailwind, desc in properties:
            data.append([
                Paragraph(f"<font name='Courier-Bold' color='{self.colors['css'].hexval()}'>{css}</font>", self.styles['Normal']),
                Paragraph(f"<font name='Courier-Bold' color='{self.colors['tailwind'].hexval()}'>{tailwind}</font>", self.styles['Normal']),
                Paragraph(desc, self.styles['Normal'])
            ])

        # Create table
        col_widths = [6*cm, 5*cm, 6*cm]
        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['header']),
            ('BACKGROUND', (0, 1), (-1, -1), self.colors['background']),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('TEXTCOLOR', (0, 1), (-1, -1), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['section']),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, self.colors['background']]),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        self.story.append(table)
        self.story.append(Spacer(1, 0.3*cm))
        return table

    def add_title(self):
        """Add the main title"""
        title = Paragraph("📝 Basic CSS vs Tailwind CSS", self.styles['MainTitle'])
        subtitle = Paragraph("Essential Styling Properties Cheat Sheet", self.styles['Subtitle'])
        self.story.append(title)
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.5*cm))

    def add_layout_basics(self):
        """Add basic layout properties"""
        properties = [
            ("display: block", "block", "Element takes full width, starts new line"),
            ("display: inline", "inline", "Element only takes necessary width"),
            ("display: inline-block", "inline-block", "Inline element with block properties"),
            ("display: none", "hidden", "Element is completely hidden"),
            ("display: flex", "flex", "Creates a flex container"),
            ("display: grid", "grid", "Creates a grid container"),
            ("position: static", "static", "Default positioning"),
            ("position: relative", "relative", "Positioned relative to normal position"),
            ("position: absolute", "absolute", "Positioned relative to nearest positioned parent"),
            ("position: fixed", "fixed", "Positioned relative to viewport"),
            ("position: sticky", "sticky", "Switches between relative and fixed"),
            ("float: left", "float-left", "Element floats to the left"),
            ("float: right", "float-right", "Element floats to the right"),
            ("clear: both", "clear-both", "Clears floated elements on both sides"),
        ]
        self.create_comparison_table("🏗️ Layout & Positioning", properties)

    def add_spacing_properties(self):
        """Add margin and padding properties"""
        properties = [
            ("margin: 0", "m-0", "No margin on all sides"),
            ("margin: 1rem", "m-4", "1rem margin on all sides"),
            ("margin-top: 0.5rem", "mt-2", "0.5rem margin on top"),
            ("margin-bottom: 1rem", "mb-4", "1rem margin on bottom"),
            ("margin-left: 2rem", "ml-8", "2rem margin on left"),
            ("margin-right: 2rem", "mr-8", "2rem margin on right"),
            ("margin: 0 auto", "mx-auto", "Horizontal centering"),
            ("padding: 0", "p-0", "No padding on all sides"),
            ("padding: 1rem", "p-4", "1rem padding on all sides"),
            ("padding-top: 0.5rem", "pt-2", "0.5rem padding on top"),
            ("padding-bottom: 1rem", "pb-4", "1rem padding on bottom"),
            ("padding-left: 2rem", "pl-8", "2rem padding on left"),
            ("padding-right: 2rem", "pr-8", "2rem padding on right"),
            ("padding: 1rem 2rem", "px-8 py-4", "Horizontal and vertical padding"),
        ]
        self.create_comparison_table("📏 Spacing (Margin & Padding)", properties)

    def add_sizing_properties(self):
        """Add width and height properties"""
        properties = [
            ("width: 100%", "w-full", "Full width"),
            ("width: 50%", "w-1/2", "Half width"),
            ("width: 25%", "w-1/4", "Quarter width"),
            ("width: auto", "w-auto", "Auto width"),
            ("width: 100px", "w-24", "Fixed width (100px ≈ 6rem)"),
            ("max-width: 100%", "max-w-full", "Maximum width 100%"),
            ("min-width: 0", "min-w-0", "Minimum width 0"),
            ("height: 100%", "h-full", "Full height"),
            ("height: 100vh", "h-screen", "Full viewport height"),
            ("height: 50%", "h-1/2", "Half height"),
            ("height: auto", "h-auto", "Auto height"),
            ("max-height: 100vh", "max-h-screen", "Maximum height of viewport"),
            ("min-height: 100vh", "min-h-screen", "Minimum height of viewport"),
        ]
        self.create_comparison_table("📐 Sizing (Width & Height)", properties)

    def add_text_properties(self):
        """Add text and typography properties"""
        properties = [
            ("color: black", "text-black", "Black text color"),
            ("color: white", "text-white", "White text color"),
            ("color: red", "text-red-500", "Red text color"),
            ("font-size: 12px", "text-xs", "Extra small font size"),
            ("font-size: 14px", "text-sm", "Small font size"),
            ("font-size: 16px", "text-base", "Base font size (default)"),
            ("font-size: 18px", "text-lg", "Large font size"),
            ("font-size: 24px", "text-2xl", "Extra large font size"),
            ("font-weight: normal", "font-normal", "Normal font weight"),
            ("font-weight: bold", "font-bold", "Bold font weight"),
            ("text-align: left", "text-left", "Left align text"),
            ("text-align: center", "text-center", "Center align text"),
            ("text-align: right", "text-right", "Right align text"),
            ("text-decoration: underline", "underline", "Underlined text"),
            ("text-decoration: none", "no-underline", "Remove text decoration"),
            ("line-height: 1.5", "leading-6", "Line height 1.5"),
            ("letter-spacing: 1px", "tracking-wide", "Wide letter spacing"),
        ]
        self.create_comparison_table("✍️ Typography & Text", properties)

    def add_background_border(self):
        """Add background and border properties"""
        properties = [
            ("background-color: white", "bg-white", "White background"),
            ("background-color: black", "bg-black", "Black background"),
            ("background-color: blue", "bg-blue-500", "Blue background"),
            ("background-color: transparent", "bg-transparent", "Transparent background"),
            ("border: 1px solid black", "border border-black", "1px solid black border"),
            ("border: 2px solid red", "border-2 border-red-500", "2px solid red border"),
            ("border: none", "border-none", "No border"),
            ("border-radius: 4px", "rounded", "Rounded corners"),
            ("border-radius: 8px", "rounded-lg", "Large rounded corners"),
            ("border-radius: 50%", "rounded-full", "Fully rounded (circle)"),
            ("box-shadow: 0 4px 6px rgba(0,0,0,0.1)", "shadow-md", "Medium shadow"),
            ("box-shadow: none", "shadow-none", "No shadow"),
            ("opacity: 0.5", "opacity-50", "50% opacity"),
            ("opacity: 1", "opacity-100", "Full opacity"),
        ]
        self.create_comparison_table("🎨 Background & Borders", properties)

    def add_common_patterns(self):
        """Add common CSS patterns"""
        examples_text = """
        <b>🚀 Common Patterns & Examples:</b><br/>
        <br/>
        <b>Center a Div:</b><br/>
        CSS: <font color='#DC2626'>margin: 0 auto; width: fit-content;</font><br/>
        Tailwind: <font color='#7C3AED'>mx-auto w-fit</font><br/>
        <br/>
        <b>Card Component:</b><br/>
        CSS: <font color='#DC2626'>background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);</font><br/>
        Tailwind: <font color='#7C3AED'>bg-white p-4 rounded-lg shadow-md</font><br/>
        <br/>
        <b>Button Style:</b><br/>
        CSS: <font color='#DC2626'>background: blue; color: white; padding: 0.5rem 1rem; border: none; border-radius: 4px;</font><br/>
        Tailwind: <font color='#7C3AED'>bg-blue-500 text-white py-2 px-4 border-none rounded</font><br/>
        <br/>
        <b>Full Height Container:</b><br/>
        CSS: <font color='#DC2626'>min-height: 100vh; display: flex; flex-direction: column;</font><br/>
        Tailwind: <font color='#7C3AED'>min-h-screen flex flex-col</font><br/>
        <br/>
        <b>Responsive Text:</b><br/>
        CSS: <font color='#DC2626'>font-size: 1rem;</font> + media queries<br/>
        Tailwind: <font color='#7C3AED'>text-base md:text-lg lg:text-xl</font><br/>
        <br/>
        <b>Hide on Mobile:</b><br/>
        CSS: <font color='#DC2626'>@media (max-width: 768px) { display: none; }</font><br/>
        Tailwind: <font color='#7C3AED'>hidden md:block</font><br/>
        <br/>
        <b>Hover Effects:</b><br/>
        CSS: <font color='#DC2626'>transition: all 0.3s ease; &:hover { transform: scale(1.05); }</font><br/>
        Tailwind: <font color='#7C3AED'>transition-all duration-300 hover:scale-105</font>
        """

        examples_para = Paragraph(examples_text, self.styles['Normal'])

        # Create a colored background table for examples
        examples_table = Table([[examples_para]], colWidths=[17*cm])
        examples_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F0FDF4')),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['description']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, self.colors['section']),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))

        self.story.append(examples_table)
        self.story.append(Spacer(1, 0.3*cm))

    def add_tips_section(self):
        """Add tips and best practices"""
        tips_text = """
        <b>💡 Tips & Best Practices:</b><br/>
        <br/>
        <b>Getting Started with Tailwind:</b><br/>
        • Add Tailwind CDN: <font color='#7C3AED'><b>&lt;script src="https://cdn.tailwindcss.com"&gt;&lt;/script&gt;</b></font><br/>
        • Or install via npm: <font color='#7C3AED'><b>npm install tailwindcss</b></font><br/>
        • Classes are applied directly in HTML: <font color='#7C3AED'><b>&lt;div class="bg-blue-500 text-white p-4"&gt;</b></font><br/>
        <br/>
        <b>Spacing Scale:</b><br/>
        • <font color='#7C3AED'><b>0</b></font> = 0px, <font color='#7C3AED'><b>1</b></font> = 0.25rem (4px), <font color='#7C3AED'><b>2</b></font> = 0.5rem (8px), <font color='#7C3AED'><b>4</b></font> = 1rem (16px)<br/>
        • <font color='#7C3AED'><b>8</b></font> = 2rem (32px), <font color='#7C3AED'><b>16</b></font> = 4rem (64px), <font color='#7C3AED'><b>32</b></font> = 8rem (128px)<br/>
        • Use consistent spacing: <font color='#7C3AED'><b>p-4 m-2 gap-4</b></font> for harmonious layouts<br/>
        <br/>
        <b>Color System:</b><br/>
        • Colors range from 50 (lightest) to 950 (darkest)<br/>
        • <font color='#7C3AED'><b>blue-100</b></font> (very light) to <font color='#7C3AED'><b>blue-900</b></font> (very dark)<br/>
        • Use <font color='#7C3AED'><b>500</b></font> as the default shade for most colors<br/>
        <br/>
        <b>Responsive Design:</b><br/>
        • <font color='#7C3AED'><b>sm:</b></font> ≥640px, <font color='#7C3AED'><b>md:</b></font> ≥768px, <font color='#7C3AED'><b>lg:</b></font> ≥1024px, <font color='#7C3AED'><b>xl:</b></font> ≥1280px<br/>
        • Mobile-first: start with base classes, add breakpoint prefixes<br/>
        • Example: <font color='#7C3AED'><b>text-sm md:text-base lg:text-lg</b></font><br/>
        <br/>
        <b>Common Mistakes:</b><br/>
        • Don't mix CSS and Tailwind classes unnecessarily<br/>
        • Use <font color='#7C3AED'><b>space-x-*</b></font> and <font color='#7C3AED'><b>space-y-*</b></font> for consistent spacing between children<br/>
        • Remember: Tailwind classes are purged in production (unused classes removed)<br/>
        <br/>
        <b>Debugging:</b><br/>
        • Add background colors to visualize layouts: <font color='#7C3AED'><b>bg-red-200</b></font><br/>
        • Use browser dev tools to see applied styles<br/>
        • Tailwind CSS IntelliSense extension for VS Code is very helpful
        """

        tips_para = Paragraph(tips_text, self.styles['Normal'])

        # Create a colored background table for tips
        tips_table = Table([[tips_para]], colWidths=[17*cm])
        tips_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#FEF3C7')),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['description']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, self.colors['accent']),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))

        self.story.append(tips_table)

    def generate_pdf(self):
        """Generate the complete PDF"""
        # Add all sections
        self.add_title()
        self.add_layout_basics()
        self.add_spacing_properties()
        self.add_sizing_properties()
        self.add_text_properties()
        self.add_background_border()
        self.add_common_patterns()
        self.add_tips_section()

        # Build PDF
        self.doc.build(self.story)
        print(f"✅ Basic CSS/Tailwind Cheat Sheet PDF generated successfully: {self.filename}")
        return self.filename

def main():
    """Main function to generate the PDF"""
    try:
        # Create PDF generator
        pdf_generator = BasicCSSCheatSheetPDF("basic_css_tailwind_cheat_sheet.pdf")

        # Generate the PDF
        filename = pdf_generator.generate_pdf()

        print(f"\n📝 Basic CSS/Tailwind Cheat Sheet PDF created: {filename}")
        print(f"📄 File size: {os.path.getsize(filename)} bytes")
        print(f"📅 Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Try to open the PDF (platform-specific)
        import platform
        if platform.system() == "Darwin":  # macOS
            os.system(f"open {filename}")
        elif platform.system() == "Windows":
            os.system(f"start {filename}")
        else:  # Linux
            os.system(f"xdg-open {filename}")

    except ImportError as e:
        print("❌ Required library not found!")
        print("📦 Install required packages with:")
        print("   pip install reportlab")
        print(f"\nError details: {e}")
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")

if __name__ == "__main__":
    main()