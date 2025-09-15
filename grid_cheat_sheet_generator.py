#!/usr/bin/env python3
"""
CSS Grid vs Tailwind CSS Grid Cheat Sheet PDF Generator
Creates a colorful, well-formatted PDF comparing CSS Grid properties with Tailwind equivalents
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from datetime import datetime

class GridCheatSheetPDF:
    def __init__(self, filename="grid_cheat_sheet.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4,
                                   rightMargin=1*cm, leftMargin=1*cm,
                                   topMargin=1.5*cm, bottomMargin=1*cm)
        self.styles = getSampleStyleSheet()
        self.story = []

        # Define color scheme
        self.colors = {
            'header': HexColor('#10B981'),      # Green
            'section': HexColor('#F59E0B'),     # Amber
            'css': HexColor('#EF4444'),         # Red for CSS
            'tailwind': HexColor('#8B5CF6'),    # Purple for Tailwind
            'description': HexColor('#374151'), # Gray
            'background': HexColor('#F9FAFB'),  # Light gray
            'accent': HexColor('#06B6D4'),      # Cyan
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
        title = Paragraph("🔲 CSS Grid vs Tailwind CSS", self.styles['MainTitle'])
        subtitle = Paragraph("Face-to-Face Comparison Cheat Sheet", self.styles['Subtitle'])
        self.story.append(title)
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.5*cm))

    def add_container_properties(self):
        """Add grid container properties"""
        properties = [
            ("display: grid", "grid", "Makes element a grid container"),
            ("grid-template-columns: repeat(3, 1fr)", "grid-cols-3", "3 equal-width columns"),
            ("grid-template-columns: repeat(4, 1fr)", "grid-cols-4", "4 equal-width columns"),
            ("grid-template-columns: 1fr 2fr", "grid-cols-[1fr_2fr]", "Custom column sizes"),
            ("grid-template-columns: 100px 1fr 100px", "grid-cols-[100px_1fr_100px]", "Fixed and flexible columns"),
            ("grid-template-rows: repeat(2, 100px)", "grid-rows-2", "2 rows of 100px height"),
            ("grid-template-rows: 1fr 2fr 1fr", "grid-rows-[1fr_2fr_1fr]", "Custom row sizes"),
            ("gap: 1rem", "gap-4", "1rem gap between grid items"),
            ("gap: 0.5rem", "gap-2", "0.5rem gap between grid items"),
            ("grid-auto-flow: column", "grid-flow-col", "Items flow horizontally"),
            ("grid-auto-flow: row", "grid-flow-row", "Items flow vertically (default)"),
            ("grid-auto-flow: dense", "grid-flow-dense", "Dense packing algorithm"),
            ("justify-items: start", "justify-items-start", "Items align to start of column"),
            ("justify-items: center", "justify-items-center", "Items align to center of column"),
            ("justify-items: end", "justify-items-end", "Items align to end of column"),
            ("justify-items: stretch", "justify-items-stretch", "Items stretch to fill column (default)"),
            ("align-items: start", "items-start", "Items align to start of row"),
            ("align-items: center", "items-center", "Items align to center of row"),
            ("align-items: end", "items-end", "Items align to end of row"),
            ("align-items: stretch", "items-stretch", "Items stretch to fill row (default)"),
            ("justify-content: start", "justify-start", "Grid aligns to start of container"),
            ("justify-content: center", "justify-center", "Grid aligns to center of container"),
            ("justify-content: end", "justify-end", "Grid aligns to end of container"),
            ("justify-content: space-between", "justify-between", "Grid items evenly distributed"),
            ("justify-content: space-around", "justify-around", "Grid items with space around"),
            ("justify-content: space-evenly", "justify-evenly", "Grid items with equal space"),
            ("align-content: start", "content-start", "Grid aligns to start of container"),
            ("align-content: center", "content-center", "Grid aligns to center of container"),
            ("align-content: end", "content-end", "Grid aligns to end of container"),
            ("align-content: space-between", "content-between", "Grid rows evenly distributed"),
            ("align-content: space-around", "content-around", "Grid rows with space around"),
        ]
        self.create_comparison_table("🔧 Grid Container Properties", properties)

    def add_item_properties(self):
        """Add grid item properties"""
        properties = [
            ("grid-column: span 2", "col-span-2", "Item spans 2 columns"),
            ("grid-column: span 3", "col-span-3", "Item spans 3 columns"),
            ("grid-column: span full", "col-span-full", "Item spans all columns"),
            ("grid-row: span 2", "row-span-2", "Item spans 2 rows"),
            ("grid-row: span 3", "row-span-3", "Item spans 3 rows"),
            ("grid-row: span full", "row-span-full", "Item spans all rows"),
            ("grid-column-start: 1", "col-start-1", "Item starts at column line 1"),
            ("grid-column-start: 2", "col-start-2", "Item starts at column line 2"),
            ("grid-column-end: 3", "col-end-3", "Item ends at column line 3"),
            ("grid-column-end: 4", "col-end-4", "Item ends at column line 4"),
            ("grid-row-start: 1", "row-start-1", "Item starts at row line 1"),
            ("grid-row-start: 2", "row-start-2", "Item starts at row line 2"),
            ("grid-row-end: 3", "row-end-3", "Item ends at row line 3"),
            ("grid-row-end: 4", "row-end-4", "Item ends at row line 4"),
            ("grid-column: 1 / 3", "col-span-2", "Item spans from column 1 to 3"),
            ("grid-row: 1 / 3", "row-span-2", "Item spans from row 1 to 3"),
            ("justify-self: start", "justify-self-start", "Item aligns to start of its column"),
            ("justify-self: center", "justify-self-center", "Item aligns to center of its column"),
            ("justify-self: end", "justify-self-end", "Item aligns to end of its column"),
            ("justify-self: stretch", "justify-self-stretch", "Item stretches to fill its column"),
            ("align-self: start", "self-start", "Item aligns to start of its row"),
            ("align-self: center", "self-center", "Item aligns to center of its row"),
            ("align-self: end", "self-end", "Item aligns to end of its row"),
            ("align-self: stretch", "self-stretch", "Item stretches to fill its row"),
            ("place-self: center", "place-self-center", "Item centers in both directions"),
            ("place-self: start", "place-self-start", "Item aligns to start in both directions"),
            ("place-self: end", "place-self-end", "Item aligns to end in both directions"),
            ("place-self: stretch", "place-self-stretch", "Item stretches in both directions"),
        ]
        self.create_comparison_table("📦 Grid Item Properties", properties)

    def add_examples_section(self):
        """Add practical examples"""
        examples_text = """
        <b>🚀 Common Grid Patterns:</b><br/>
        <br/>
        <b>Simple 3-Column Layout:</b><br/>
        CSS: <font color='#EF4444'>display:grid; grid-template-columns:repeat(3,1fr); gap:1rem</font><br/>
        Tailwind: <font color='#8B5CF6'>grid grid-cols-3 gap-4</font><br/>
        <br/>
        <b>Sidebar + Main Content:</b><br/>
        CSS: <font color='#EF4444'>display:grid; grid-template-columns:250px 1fr; gap:2rem</font><br/>
        Tailwind: <font color='#8B5CF6'>grid grid-cols-[250px_1fr] gap-8</font><br/>
        <br/>
        <b>Card Grid:</b><br/>
        CSS: <font color='#EF4444'>display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:1rem</font><br/>
        Tailwind: <font color='#8B5CF6'>grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-4</font><br/>
        <br/>
        <b>Header + Content + Footer:</b><br/>
        CSS: <font color='#EF4444'>display:grid; grid-template-rows:auto 1fr auto; min-h:100vh</font><br/>
        Tailwind: <font color='#8B5CF6'>grid grid-rows-[auto_1fr_auto] min-h-screen</font><br/>
        <br/>
        <b>Full-Width Header:</b><br/>
        CSS: <font color='#EF4444'>grid-column:1/-1</font> (on header item)<br/>
        Tailwind: <font color='#8B5CF6'>col-span-full</font> (on header item)<br/>
        <br/>
        <b>Centered Content:</b><br/>
        CSS: <font color='#EF4444'>place-self:center</font> (on item)<br/>
        Tailwind: <font color='#8B5CF6'>place-self-center</font> (on item)
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
        • Always start with <font color='#8B5CF6'><b>grid</b></font> class to enable CSS Grid<br/>
        • Use <font color='#8B5CF6'><b>grid-cols-*</b></font> for predefined column counts<br/>
        • Use <font color='#8B5CF6'><b>grid-cols-[...]</b></font> for custom column definitions<br/>
        <br/>
        <b>Common Patterns:</b><br/>
        • <font color='#8B5CF6'><b>grid-cols-1</b></font> to <font color='#8B5CF6'><b>grid-cols-12</b></font> for standard layouts<br/>
        • <font color='#8B5CF6'><b>col-span-*</b></font> to make items span multiple columns<br/>
        • <font color='#8B5CF6'><b>row-span-*</b></font> to make items span multiple rows<br/>
        <br/>
        <b>Responsive Design:</b><br/>
        • <font color='#8B5CF6'><b>md:grid-cols-2 lg:grid-cols-3</b></font> for responsive grids<br/>
        • <font color='#8B5CF6'><b>sm:col-span-1 md:col-span-2</b></font> for responsive item spans<br/>
        • Combine with <font color='#8B5CF6'><b>gap-*</b></font> for consistent spacing<br/>
        <br/>
        <b>Advanced Techniques:</b><br/>
        • Use <font color='#8B5CF6'><b>grid-flow-dense</b></font> to fill gaps in irregular layouts<br/>
        • <font color='#8B5CF6'><b>place-self-center</b></font> combines justify-self and align-self<br/>
        • <font color='#8B5CF6'><b>col-span-full</b></font> makes item span entire grid width<br/>
        <br/>
        <b>Performance:</b><br/>
        • CSS Grid is hardware-accelerated in modern browsers<br/>
        • Avoid changing grid structure frequently<br/>
        • Use implicit grids for dynamic content<br/>
        <br/>
        <b>Debugging:</b><br/>
        • Add background colors to visualize grid areas<br/>
        • Use browser dev tools grid inspector<br/>
        • Remember: grid only affects direct children
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
        print(f"✅ Grid Cheat Sheet PDF generated successfully: {self.filename}")
        return self.filename

def main():
    """Main function to generate the PDF"""
    try:
        # Create PDF generator
        pdf_generator = GridCheatSheetPDF("grid_cheat_sheet.pdf")

        # Generate the PDF
        filename = pdf_generator.generate_pdf()

        print(f"\n🔲 Grid Cheat Sheet PDF created: {filename}")
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