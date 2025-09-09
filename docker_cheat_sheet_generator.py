#!/usr/bin/env python3
"""
Docker Commands Cheat Sheet PDF Generator
Creates a colorful, well-formatted 2-page A4 PDF Docker command reference
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from datetime import datetime

class DockerCheatSheetPDF:
    def __init__(self, filename="docker_cheat_sheet.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4,
                                   rightMargin=1.2*cm, leftMargin=1.2*cm,
                                   topMargin=2*cm, bottomMargin=1.5*cm)
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Define modern color scheme
        self.colors = {
            'header': HexColor('#1F2937'),      # Dark blue-gray
            'section': HexColor('#059669'),     # Emerald green
            'command': HexColor('#DC2626'),     # Red
            'description': HexColor('#374151'), # Gray-700
            'background': HexColor('#F9FAFB'),  # Gray-50
            'accent': HexColor('#7C3AED'),      # Violet
            'border': HexColor('#E5E7EB'),      # Gray-200
            'row_alt': HexColor('#F3F4F6'),     # Gray-100
        }
        
        # Custom styles
        self.create_custom_styles()
    
    def create_custom_styles(self):
        """Create custom paragraph styles"""
        # Main title style
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            spaceAfter=30,
            spaceBefore=10,
            textColor=self.colors['header'],
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=32
        ))

        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            spaceBefore=25,
            textColor=self.colors['section'],
            fontName='Helvetica-Bold',
            leading=20,
            borderColor=self.colors['section'],
            borderWidth=0,
            borderPadding=5
        ))

        # Command style
        self.styles.add(ParagraphStyle(
            name='Command',
            parent=self.styles['Code'],
            fontSize=10,
            textColor=self.colors['command'],
            fontName='Courier-Bold',
            leftIndent=5,
            leading=12
        ))

        # Description style
        self.styles.add(ParagraphStyle(
            name='Description',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.colors['description'],
            fontName='Helvetica',
            leading=12,
            leftIndent=5
        ))

    def create_command_table(self, title, commands, col_widths=[7*cm, 8*cm]):
        """Create a formatted table for commands"""
        # Add section header
        self.story.append(Paragraph(title, self.styles['SectionHeader']))
        
        # Prepare table data
        data = []
        for cmd, desc in commands:
            data.append([
                Paragraph(f"<font name='Courier-Bold' color='#D35400'>{cmd}</font>", self.styles['Normal']),
                Paragraph(desc, self.styles['Description'])
            ])
        
        # Create table
        table = Table(data, colWidths=col_widths, repeatRows=0)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['background']),
            ('TEXTCOLOR', (0, 0), (-1, -1), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Courier-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, self.colors['border']),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [white, self.colors['row_alt']]),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 1.5, self.colors['section']),
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*cm))
        return table

    def add_title(self):
        """Add the main title"""
        title = Paragraph("🐳 Docker Commands Cheat Sheet 🐳", self.styles['MainTitle'])
        self.story.append(title)

        # Add subtitle
        subtitle_style = ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=self.colors['description'],
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique',
            spaceAfter=20
        )
        subtitle = Paragraph("Complete Reference Guide for Docker Commands", subtitle_style)
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.8*cm))

    def add_container_management(self):
        """Add container management commands"""
        commands = [
            ("docker run -d nginx", "Run container in detached mode"),
            ("docker run -it ubuntu bash", "Interactive container with terminal"),
            ("docker run -p 8080:80 nginx", "Map port 8080 to container port 80"),
            ("docker run --name myapp nginx", "Run with custom container name"),
            ("docker run -v /host:/container app", "Mount volume from host to container"),
            ("docker ps", "List running containers"),
            ("docker ps -a", "List all containers (including stopped)"),
            ("docker start CONTAINER", "Start a stopped container"),
            ("docker stop CONTAINER", "Stop a running container"),
            ("docker restart CONTAINER", "Restart a container"),
            ("docker kill CONTAINER", "Force stop a container"),
            ("docker rm CONTAINER", "Remove a container"),
            ("docker rm -f CONTAINER", "Force remove a running container"),
        ]
        self.create_command_table("Container Management", commands)

    def add_container_info(self):
        """Add container information commands"""
        commands = [
            ("docker logs CONTAINER", "View container logs"),
            ("docker logs -f CONTAINER", "Follow logs in real-time"),
            ("docker logs --tail 100 CONTAINER", "Show last 100 log lines"),
            ("docker inspect CONTAINER", "Detailed container information"),
            ("docker stats", "Live resource usage statistics"),
            ("docker top CONTAINER", "Running processes in container"),
            ("docker exec CONTAINER COMMAND", "Execute command in container"),
            ("docker exec -it CONTAINER bash", "Interactive bash session"),
        ]
        self.create_command_table("Container Information & Logs", commands)

    def add_image_management(self):
        """Add image management commands"""
        commands = [
            ("docker images", "List local images"),
            ("docker images -a", "List all images (including intermediate)"),
            ("docker pull IMAGE[:TAG]", "Download image from registry"),
            ("docker push IMAGE[:TAG]", "Upload image to registry"),
            ("docker build .", "Build image from current directory"),
            ("docker build -t myapp:v1.0 .", "Build image with tag"),
            ("docker build --no-cache .", "Build without using cache"),
            ("docker rmi IMAGE", "Remove an image"),
            ("docker rmi -f IMAGE", "Force remove an image"),
            ("docker tag SOURCE TARGET", "Tag an image"),
            ("docker history IMAGE", "Show image layer history"),
            ("docker image prune", "Remove unused images"),
            ("docker image prune -a", "Remove all unused images"),
        ]
        self.create_command_table("Image Management", commands)

    def add_network_volume(self):
        """Add network and volume management"""
        commands = [
            ("docker network ls", "List networks"),
            ("docker network create NETWORK", "Create custom network"),
            ("docker network rm NETWORK", "Remove network"),
            ("docker network inspect NETWORK", "Network detailed information"),
            ("docker volume ls", "List volumes"),
            ("docker volume create VOLUME", "Create named volume"),
            ("docker volume rm VOLUME", "Remove volume"),
            ("docker volume inspect VOLUME", "Volume detailed information"),
            ("docker volume prune", "Remove unused volumes"),
        ]
        self.create_command_table("Network & Volume Management", commands)

    def add_docker_compose(self):
        """Add Docker Compose commands"""
        commands = [
            ("docker-compose up", "Start all services"),
            ("docker-compose up -d", "Start services in detached mode"),
            ("docker-compose up --build", "Rebuild images and start services"),
            ("docker-compose down", "Stop and remove containers/networks"),
            ("docker-compose down -v", "Stop and remove volumes too"),
            ("docker-compose ps", "List running services"),
            ("docker-compose logs", "View logs from all services"),
            ("docker-compose logs SERVICE", "View logs from specific service"),
            ("docker-compose exec SERVICE bash", "Execute bash in service container"),
            ("docker-compose restart SERVICE", "Restart specific service"),
            ("docker-compose scale SERVICE=3", "Scale service to 3 instances"),
        ]
        self.create_command_table("Docker Compose", commands)

    def add_system_management(self):
        """Add system management commands"""
        commands = [
            ("docker version", "Show Docker version information"),
            ("docker info", "Display system-wide information"),
            ("docker system df", "Show Docker disk usage"),
            ("docker system prune", "Remove unused data"),
            ("docker system prune -a", "Remove all unused data"),
            ("docker system prune -a --volumes", "Remove everything unused"),
            ("docker container prune", "Remove stopped containers"),
            ("docker login", "Login to Docker registry"),
            ("docker logout", "Logout from Docker registry"),
            ("docker search TERM", "Search Docker Hub for images"),
        ]
        self.create_command_table("System Management & Cleanup", commands)

    def add_run_options(self):
        """Add common docker run options"""
        commands = [
            ("-d, --detach", "Run container in background"),
            ("-it", "Interactive mode with TTY"),
            ("-p, --publish HOST:CONTAINER", "Publish container port to host"),
            ("-v, --volume HOST:CONTAINER", "Bind mount a volume"),
            ("--name NAME", "Assign name to container"),
            ("-e, --env KEY=VALUE", "Set environment variables"),
            ("--rm", "Remove container when it exits"),
            ("-m, --memory LIMIT", "Memory limit (e.g., 512m, 2g)"),
            ("--cpus NUMBER", "CPU limit (e.g., 0.5, 2.0)"),
            ("--restart POLICY", "Restart policy (no/always/unless-stopped)"),
            ("--network NETWORK", "Connect to specific network"),
            ("-w, --workdir PATH", "Set working directory"),
        ]
        self.create_command_table("Common Docker Run Options", commands, [6*cm, 9*cm])

    def add_dockerfile_instructions(self):
        """Add Dockerfile instructions"""
        commands = [
            ("FROM image:tag", "Specify base image"),
            ("WORKDIR /path", "Set working directory"),
            ("COPY src dest", "Copy files from host to image"),
            ("ADD src dest", "Copy files (supports URLs & archives)"),
            ("RUN command", "Execute command during build"),
            ("ENV KEY=VALUE", "Set environment variable"),
            ("EXPOSE port", "Document port usage"),
            ("USER user:group", "Set user for subsequent commands"),
            ("CMD [\"cmd\", \"arg1\"]", "Default command to run"),
            ("ENTRYPOINT [\"cmd\"]", "Configure container executable"),
            ("VOLUME [\"/data\"]", "Create mount point"),
            ("LABEL key=value", "Add metadata to image"),
        ]
        self.create_command_table("Common Dockerfile Instructions", commands, [6*cm, 9*cm])

    def add_tips_section(self):
        """Add tips and best practices"""
        tips_text = """
        <b>💡 Pro Tips & Best Practices:</b><br/>
        <br/>
        • Use specific image tags instead of 'latest' in production<br/>
        • Use .dockerignore to exclude unnecessary files from build context<br/>
        • Multi-stage builds help reduce final image size<br/>
        • Use 'docker run --rm' for temporary containers<br/>
        • Regularly clean up with 'docker system prune'<br/>
        • Name your containers and volumes for easier management<br/>
        • Use volumes for persistent data, not container filesystem<br/>
        • Always check container logs when troubleshooting<br/>
        • Use healthchecks in production deployments<br/>
        • Keep containers stateless and configuration external
        """

        tips_para = Paragraph(tips_text, self.styles['Normal'])

        # Create a colored background table for tips
        tips_table = Table([[tips_para]], colWidths=[17*cm])
        tips_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F0F9FF')),
            ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#1E40AF')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 2, self.colors['accent']),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 2, self.colors['accent']),
        ]))

        self.story.append(tips_table)

    def generate_pdf(self):
        """Generate the complete PDF"""
        # Page 1
        self.add_title()
        self.add_container_management()
        self.add_container_info()
        self.add_image_management()
        
        # Page break
        self.story.append(PageBreak())
        
        # Page 2
        self.add_network_volume()
        self.add_docker_compose()
        self.add_system_management()
        self.add_run_options()
        self.add_dockerfile_instructions()
        self.add_tips_section()
        
        # Build PDF
        self.doc.build(self.story)
        print(f"[SUCCESS] Docker Cheat Sheet PDF generated successfully: {self.filename}")
        return self.filename

def main():
    """Main function to generate the PDF"""
    try:
        # Create PDF generator
        pdf_generator = DockerCheatSheetPDF("docker_cheat_sheet.pdf")
        
        # Generate the PDF
        filename = pdf_generator.generate_pdf()
        
        print(f"\n[DOCKER] Docker Cheat Sheet PDF created: {filename}")
        print(f"[INFO] File size: {os.path.getsize(filename)} bytes")
        print(f"[INFO] Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Try to open the PDF (platform-specific)
        import platform
        if platform.system() == "Darwin":  # macOS
            os.system(f"open {filename}")
        elif platform.system() == "Windows":
            os.system(f"start {filename}")
        else:  # Linux
            os.system(f"xdg-open {filename}")

    except ImportError as e:
        print("[ERROR] Required library not found!")
        print("[INFO] Install required packages with:")
        print("   pip install reportlab")
        print(f"\nError details: {e}")
    except Exception as e:
        print(f"[ERROR] Error generating PDF: {e}")

if __name__ == "__main__":
    main()