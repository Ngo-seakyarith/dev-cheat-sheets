#!/usr/bin/env python3
"""
CSS Flexbox vs Tailwind CSS Cheat Sheet PDF Generator
Creates a colorful, well-formatted PDF comparing CSS Flexbox properties with Tailwind equivalents
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from datetime import datetime

class FlexboxCheatSheetPDF:
    def __init__(self, filename="flexbox_cheat_sheet.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4,
                                   rightMargin=1*cm, leftMargin=1*cm,
                                   topMargin=1.5*cm, bottomMargin=1*cm)
        self.styles = getSampleStyleSheet()
        self.story = []

        # Define color scheme
        self.colors = {
            'header': HexColor('#2563EB'),      # Blue
            'section': HexColor('#059669'),     # Green
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
        title = Paragraph("🎨 CSS Flexbox vs Tailwind CSS", self.styles['MainTitle'])
        subtitle = Paragraph("Face-to-Face Comparison Cheat Sheet", self.styles['Subtitle'])
        self.story.append(title)
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.5*cm))


    def add_container_properties(self):
        """Add flex container properties"""
        properties = [
            ("display: flex", "flex", "Makes element a flex container"),
            ("flex-direction: row", "flex-row", "Items flow horizontally (default)"),
            ("flex-direction: row-reverse", "flex-row-reverse", "Items flow horizontally in reverse"),
            ("flex-direction: column", "flex-col", "Items flow vertically"),
            ("flex-direction: column-reverse", "flex-col-reverse", "Items flow vertically in reverse"),
            ("flex-wrap: nowrap", "flex-nowrap", "Items stay on single line (default)"),
            ("flex-wrap: wrap", "flex-wrap", "Items wrap to next line if needed"),
            ("flex-wrap: wrap-reverse", "flex-wrap-reverse", "Items wrap in reverse order"),
            ("justify-content: flex-start", "justify-start", "Items align to start of container"),
            ("justify-content: flex-end", "justify-end", "Items align to end of container"),
            ("justify-content: center", "justify-center", "Items align to center of container"),
            ("justify-content: space-between", "justify-between", "Items evenly distributed with space between"),
            ("justify-content: space-around", "justify-around", "Items evenly distributed with space around"),
            ("justify-content: space-evenly", "justify-evenly", "Items evenly distributed with equal space"),
            ("align-items: stretch", "items-stretch", "Items stretch to fill container height (default)"),
            ("align-items: flex-start", "items-start", "Items align to top of container"),
            ("align-items: flex-end", "items-end", "Items align to bottom of container"),
            ("align-items: center", "items-center", "Items align to vertical center of container"),
            ("align-items: baseline", "items-baseline", "Items align to their baselines"),
            ("align-content: stretch", "content-stretch", "Lines stretch to fill container (default)"),
            ("align-content: flex-start", "content-start", "Lines align to start of container"),
            ("align-content: flex-end", "content-end", "Lines align to end of container"),
            ("align-content: center", "content-center", "Lines align to center of container"),
            ("align-content: space-between", "content-between", "Lines evenly distributed with space between"),
            ("align-content: space-around", "content-around", "Lines evenly distributed with space around"),
        ]
        self.create_comparison_table("🔧 Flex Container Properties", properties)

    def add_item_properties(self):
        """Add flex item properties"""
        properties = [
            ("flex-grow: 0", "flex-grow-0", "Item doesn't grow (default)"),
            ("flex-grow: 1", "flex-grow", "Item grows to fill available space"),
            ("flex-shrink: 1", "flex-shrink", "Item can shrink if needed (default)"),
            ("flex-shrink: 0", "flex-shrink-0", "Item doesn't shrink"),
            ("flex-basis: auto", "flex-auto", "Item size based on content or width/height"),
            ("flex-basis: 0", "flex-initial", "Item size based on content only"),
            ("flex: 1", "flex-1", "flex: 1 1 0% (grows, shrinks, no basis)"),
            ("flex: none", "flex-none", "flex: 0 0 auto (no grow/shrink)"),
            ("align-self: auto", "self-auto", "Item uses parent's align-items (default)"),
            ("align-self: flex-start", "self-start", "Item aligns to start of cross axis"),
            ("align-self: flex-end", "self-end", "Item aligns to end of cross axis"),
            ("align-self: center", "self-center", "Item aligns to center of cross axis"),
            ("align-self: stretch", "self-stretch", "Item stretches to fill cross axis"),
            ("align-self: baseline", "self-baseline", "Item aligns to baseline"),
            ("order: 0", "order-0", "Item appears in normal order (default)"),
            ("order: 1", "order-1", "Item appears after items with lower order"),
            ("order: -1", "order-first", "Item appears before all other items"),
            ("order: 9999", "order-last", "Item appears after all other items"),
        ]
        self.create_comparison_table("📦 Flex Item Properties", properties)

    def add_examples_section(self):
        """Add practical examples"""
        examples_text = """
        <b>🚀 Common Patterns:</b><br/>
        <br/>
        <b>Perfect Centering:</b><br/>
        CSS: <font color='#DC2626'>display:flex; justify-content:center; align-items:center; min-h:100vh</font><br/>
        Tailwind: <font color='#7C3AED'>flex justify-center items-center min-h-screen</font><br/>
        <br/>
        <b>Navigation Bar:</b><br/>
        CSS: <font color='#DC2626'>display:flex; justify-content:space-between; align-items:center; padding:1rem</font><br/>
        Tailwind: <font color='#7C3AED'>flex justify-between items-center p-4</font><br/>
        <br/>
        <b>Card Layout:</b><br/>
        CSS: <font color='#DC2626'>display:flex; flex-direction:column; justify-content:space-between; height:300px</font><br/>
        Tailwind: <font color='#7C3AED'>flex flex-col justify-between h-72</font><br/>
        <br/>
        <b>Responsive Grid:</b><br/>
        CSS: <font color='#DC2626'>display:flex; flex-wrap:wrap; gap:1rem; justify-content:center</font><br/>
        Tailwind: <font color='#7C3AED'>flex flex-wrap gap-4 justify-center</font><br/>
        <br/>
        <b>Equal Width Columns:</b><br/>
        CSS: <font color='#DC2626'>display:flex; flex:1</font> (on each item)<br/>
        Tailwind: <font color='#7C3AED'>flex-1</font> (on each item)<br/>
        <br/>
        <b>Sticky Footer:</b><br/>
        CSS: <font color='#DC2626'>display:flex; flex-direction:column; min-h:100vh; flex:1</font> (on main)<br/>
        Tailwind: <font color='#7C3AED'>flex flex-col min-h-screen flex-1</font> (on main)
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
        <b>Getting Started:</b><br/>
        • Always start with <font color='#7C3AED'><b>flex</b></font> class to enable flexbox<br/>
        • Default direction is row (horizontal), use <font color='#7C3AED'><b>flex-col</b></font> for vertical<br/>
        • Items stretch by default, use <font color='#7C3AED'><b>items-start</b></font> to prevent<br/>
        <br/>
        <b>Axis Understanding:</b><br/>
        • <font color='#7C3AED'><b>justify-*</b></font> controls main axis (direction of flex)<br/>
        • <font color='#7C3AED'><b>items-*</b></font> controls cross axis (perpendicular to main)<br/>
        • When <font color='#7C3AED'><b>flex-col</b></font>, main axis becomes vertical<br/>
        <br/>
        <b>Common Techniques:</b><br/>
        • Use <font color='#7C3AED'><b>flex-1</b></font> for equal-width/height growing items<br/>
        • <font color='#7C3AED'><b>flex-none</b></font> prevents growing/shrinking<br/>
        • <font color='#7C3AED'><b>gap-*</b></font> adds spacing between items (modern browsers)<br/>
        <br/>
        <b>Responsive Design:</b><br/>
        • <font color='#7C3AED'><b>md:flex-col lg:flex-row</b></font> for responsive layouts<br/>
        • <font color='#7C3AED'><b>sm:justify-start md:justify-center</b></font> for breakpoint-specific alignment<br/>
        • Test on different screen sizes to ensure proper behavior<br/>
        <br/>
        <b>Performance:</b><br/>
        • Flexbox is hardware-accelerated in modern browsers<br/>
        • Avoid changing flex direction frequently<br/>
        • Use <font color='#7C3AED'><b>flex-wrap</b></font> for responsive multi-line layouts<br/>
        <br/>
        <b>Debugging:</b><br/>
        • Add background colors to visualize containers and items<br/>
        • Use browser dev tools to inspect flex properties<br/>
        • Remember: flexbox only affects direct children
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
        # Single page
        self.add_title()
        self.add_container_properties()
        self.add_item_properties()
        self.add_examples_section()
        self.add_tips_section()

        # Build PDF
        self.doc.build(self.story)
        print(f"✅ Flexbox Cheat Sheet PDF generated successfully: {self.filename}")
        return self.filename

def main():
    """Main function to generate the PDF"""
    try:
        # Create PDF generator
        pdf_generator = FlexboxCheatSheetPDF("flexbox_cheat_sheet.pdf")

        # Generate the PDF
        filename = pdf_generator.generate_pdf()

        print(f"\n🎨 Flexbox Cheat Sheet PDF created: {filename}")
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