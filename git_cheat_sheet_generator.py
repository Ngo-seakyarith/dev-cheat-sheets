#!/usr/bin/env python3
"""
Git Commands Cheat Sheet PDF Generator
Creates a colorful, well-formatted 2-page A4 PDF Git command reference
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

class GitCheatSheetPDF:
    def __init__(self, filename="git_cheat_sheet.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4, 
                                   rightMargin=1*cm, leftMargin=1*cm,
                                   topMargin=1.5*cm, bottomMargin=1*cm)
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Define color scheme
        self.colors = {
            'header': HexColor('#F14E32'),      # Git Red
            'section': HexColor('#2E8B57'),     # Sea Green  
            'command': HexColor('#FF6B35'),     # Orange Red
            'description': HexColor('#2C3E50'), # Dark gray
            'background': HexColor('#F8F9FA'),  # Light gray
            'accent': HexColor('#6C5CE7'),      # Purple
            'warning': HexColor('#E74C3C')      # Red for dangerous commands
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
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            textColor=self.colors['section'],
            fontName='Helvetica-Bold'
        ))

    def create_command_table(self, title, commands, col_widths=[7*cm, 8*cm], dangerous_commands=None):
        """Create a formatted table for commands"""
        if dangerous_commands is None:
            dangerous_commands = []
            
        # Add section header
        self.story.append(Paragraph(title, self.styles['SectionHeader']))
        
        # Prepare table data
        data = []
        for cmd, desc in commands:
            # Use warning color for dangerous commands
            color = '#E74C3C' if any(danger in cmd for danger in dangerous_commands) else '#FF6B35'
            data.append([
                Paragraph(f"<font name='Courier-Bold' color='{color}'>{cmd}</font>", self.styles['Normal']),
                Paragraph(desc, self.styles['Normal'])
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
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['section']),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [white, self.colors['background']]),
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
        title = Paragraph("🌿 Git Commands Cheat Sheet 🌿", self.styles['MainTitle'])
        self.story.append(title)
        self.story.append(Spacer(1, 0.5*cm))

    def add_basic_commands(self):
        """Add basic Git commands"""
        commands = [
            ("git init", "Initialize a new Git repository"),
            ("git clone &lt;url&gt;", "Clone remote repository to local machine"),
            ("git clone &lt;url&gt; &lt;directory&gt;", "Clone into specific directory"),
            ("git status", "Show working tree status"),
            ("git add &lt;file&gt;", "Add file to staging area"),
            ("git add .", "Add all files to staging area"),
            ("git add -A", "Add all files (including deleted)"),
            ("git commit -m '&lt;message&gt;'", "Commit staged changes with message"),
            ("git commit -am '&lt;message&gt;'", "Add all tracked files and commit"),
            ("git commit --amend", "Modify last commit"),
            ("git log", "Show commit history"),
            ("git log --oneline", "Show condensed commit history"),
            ("git log --graph", "Show commit history as graph"),
        ]
        self.create_command_table("Basic Git Operations", commands)

    def add_branching_commands(self):
        """Add branching and merging commands"""
        dangerous_commands = ['reset --hard', 'push --force', 'rebase']
        commands = [
            ("git branch", "List local branches"),
            ("git branch -a", "List all branches (local + remote)"),
            ("git branch &lt;branch-name&gt;", "Create new branch"),
            ("git branch -d &lt;branch-name&gt;", "Delete merged branch"),
            ("git branch -D &lt;branch-name&gt;", "Force delete branch"),
            ("git checkout &lt;branch-name&gt;", "Switch to branch"),
            ("git checkout -b &lt;branch-name&gt;", "Create and switch to new branch"),
            ("git switch &lt;branch-name&gt;", "Switch to branch (Git 2.23+)"),
            ("git switch -c &lt;branch-name&gt;", "Create and switch to new branch"),
            ("git merge &lt;branch-name&gt;", "Merge branch into current branch"),
            ("git merge --no-ff &lt;branch-name&gt;", "Merge with merge commit"),
            ("git rebase &lt;branch-name&gt;", "⚠️ Rebase current branch onto branch"),
        ]
        self.create_command_table("Branching & Merging", commands, dangerous_commands=dangerous_commands)

    def add_remote_commands(self):
        """Add remote repository commands"""
        dangerous_commands = ['push --force']
        commands = [
            ("git remote", "List remote repositories"),
            ("git remote -v", "List remotes with URLs"),
            ("git remote add &lt;name&gt; &lt;url&gt;", "Add remote repository"),
            ("git remote remove &lt;name&gt;", "Remove remote repository"),
            ("git fetch", "Download changes from remote"),
            ("git fetch &lt;remote&gt;", "Fetch from specific remote"),
            ("git pull", "Fetch and merge from remote"),
            ("git pull --rebase", "Fetch and rebase instead of merge"),
            ("git push", "Push changes to remote"),
            ("git push &lt;remote&gt; &lt;branch-name&gt;", "Push branch to specific remote"),
            ("git push -u origin &lt;branch-name&gt;", "Push and set upstream branch"),
            ("git push --force", "⚠️ Force push (dangerous)"),
            ("git push --force-with-lease", "Safer force push"),
        ]
        self.create_command_table("Remote Repository Operations", commands, dangerous_commands=dangerous_commands)

    def add_inspection_commands(self):
        """Add inspection and comparison commands"""
        commands = [
            ("git diff", "Show unstaged changes"),
            ("git diff --staged", "Show staged changes"),
            ("git diff &lt;branch-name&gt;", "Compare with another branch"),
            ("git diff HEAD~1", "Compare with previous commit"),
            ("git show &lt;commit-id&gt;", "Show specific commit details"),
            ("git blame &lt;file&gt;", "Show who changed each line"),
            ("git log --follow &lt;file&gt;", "Show file history across renames"),
            ("git log --grep='&lt;pattern&gt;'", "Search commits by message"),
            ("git log --author='&lt;name&gt;'", "Filter commits by author"),
            ("git reflog", "Show reference log (recovery tool)"),
        ]
        self.create_command_table("Inspection & Comparison", commands)

    def add_undoing_commands(self):
        """Add commands for undoing changes"""
        dangerous_commands = ['reset --hard', 'clean -fd']
        commands = [
            ("git checkout -- &lt;file&gt;", "Discard changes in working directory"),
            ("git restore &lt;file&gt;", "Discard changes (Git 2.23+)"),
            ("git reset &lt;file&gt;", "Unstage file (keep changes in working directory)"),
            ("git reset --soft HEAD~1", "Resets to one commit before HEAD (the immediate previous commit). HEAD~1 means 'parent of HEAD'"),
            ("git reset --soft &lt;commit-id&gt;", "Resets to a specific commit hash you provide. You can reset to any commit in history"),
            ("git reset --mixed HEAD~1", "Resets to one commit before HEAD, unstaging changes but keeping them in working directory"),
            ("git reset --mixed &lt;commit-id&gt;", "Resets to a specific commit hash, unstaging changes but keeping them in working directory"),
            ("git reset --hard HEAD~1", "⚠️ Resets to one commit before HEAD and permanently deletes all uncommitted changes"),
            ("git reset --hard &lt;commit-id&gt;", "⚠️ Resets to a specific commit hash and permanently deletes all uncommitted changes"),
            ("git revert &lt;commit-id&gt;", "Create commit that undoes specified commit"),
            ("git clean -n", "Preview untracked files to delete"),
            ("git clean -f", "Delete untracked files"),
            ("git clean -fd", "⚠️ Delete untracked files and directories"),
        ]
        self.create_command_table("Undoing Changes", commands, dangerous_commands=dangerous_commands)

    def add_stashing_commands(self):
        """Add stashing commands"""
        commands = [
            ("git stash", "Stash current changes"),
            ("git stash save '&lt;message&gt;'", "Stash with message"),
            ("git stash list", "List all stashes"),
            ("git stash show", "Show latest stash changes"),
            ("git stash show -p", "Show latest stash as patch"),
            ("git stash apply", "Apply latest stash"),
            ("git stash apply stash@{&lt;index&gt;}", "Apply specific stash"),
            ("git stash pop", "Apply and remove latest stash"),
            ("git stash drop", "Delete latest stash"),
            ("git stash clear", "Delete all stashes"),
        ]
        self.create_command_table("Stashing", commands, [6*cm, 9*cm])

    def add_advanced_commands(self):
        """Add advanced Git commands"""
        dangerous_commands = ['filter-branch', 'gc --aggressive']
        commands = [
            ("git tag", "List tags"),
            ("git tag &lt;tag-name&gt;", "Create lightweight tag"),
            ("git tag -a &lt;tag-name&gt; -m '&lt;message&gt;'", "Create annotated tag"),
            ("git tag -d &lt;tag-name&gt;", "Delete tag"),
            ("git cherry-pick &lt;commit-id&gt;", "Apply specific commit to current branch"),
            ("git bisect start", "Start binary search for bug"),
            ("git submodule add &lt;url&gt;", "Add Git submodule"),
            ("git submodule update --init", "Initialize and update submodules"),
            ("git archive --format=zip HEAD", "Create archive of current HEAD"),
            ("git gc", "Cleanup unnecessary files"),
            ("git fsck", "Check repository integrity"),
        ]
        self.create_command_table("Advanced Commands", commands, [6*cm, 9*cm], dangerous_commands)

    def add_configuration_commands(self):
        """Add Git configuration commands"""
        commands = [
            ("git config --global user.name '&lt;name&gt;'", "Set global username"),
            ("git config --global user.email '&lt;email&gt;'", "Set global email"),
            ("git config --list", "Show all configuration"),
            ("git config user.name", "Show username"),
            ("git config --global init.defaultBranch main", "Set default branch name"),
            ("git config --global core.editor &lt;editor&gt;", "Set default editor"),
            ("git config --global alias.&lt;alias&gt; &lt;command&gt;", "Create alias for command"),
            ("git config --global core.autocrlf true", "Auto convert line endings (Windows)"),
            ("git config --global core.autocrlf input", "Auto convert line endings (Mac/Linux)"),
            ("git config --global pull.rebase false", "Default merge behavior for pull"),
        ]
        self.create_command_table("Configuration", commands, [8*cm, 7*cm])

    def add_workflows_section(self):
        """Add common Git workflows"""
        workflows_text = """
        <b>🔄 Common Git Workflows:</b><br/>
        <br/>
        <b>Feature Branch Workflow:</b><br/>
        1. git checkout -b feature/&lt;feature-name&gt;<br/>
        2. Make changes and commits<br/>
        3. git push -u origin feature/&lt;feature-name&gt;<br/>
        4. Create pull request<br/>
        5. git checkout main && git pull<br/>
        6. git branch -d feature/&lt;feature-name&gt;<br/>
        <br/>
        <b>Hotfix Workflow:</b><br/>
        1. git checkout -b hotfix/&lt;fix-name&gt;<br/>
        2. Make fix and commit<br/>
        3. git checkout main && git merge hotfix/&lt;fix-name&gt;<br/>
        4. git checkout develop && git merge hotfix/&lt;fix-name&gt;<br/>
        5. git branch -d hotfix/&lt;fix-name&gt;<br/>
        <br/>
        <b>Release Workflow:</b><br/>
        1. git checkout -b release/&lt;version&gt;<br/>
        2. Bump version numbers, final testing<br/>
        3. git checkout main && git merge release/&lt;version&gt;<br/>
        4. git tag -a &lt;version&gt; -m "Version &lt;version&gt;"<br/>
        5. git checkout develop && git merge release/&lt;version&gt;
        """
        
        workflows_para = Paragraph(workflows_text, self.styles['Normal'])
        
        # Create a colored background table for workflows
        workflows_table = Table([[workflows_para]], colWidths=[17*cm])
        workflows_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#E8F4FD')),
            ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#1B4F72')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#2E8B57')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        self.story.append(workflows_table)
        self.story.append(Spacer(1, 0.3*cm))

    def add_tips_section(self):
        """Add tips and best practices"""
        tips_text = """
        <b>💡 Git Tips & Best Practices:</b><br/>
        <br/>
        • Write clear, descriptive commit messages<br/>
        • Commit early and often with logical chunks<br/>
        • Always review changes before committing (git diff --staged)<br/>
        • Use .gitignore to exclude unnecessary files<br/>
        • Never commit sensitive information (passwords, keys)<br/>
        • Use branches for features, experiments, and fixes<br/>
        • Rebase feature branches before merging (when safe)<br/>
        • Use 'git stash' when switching contexts quickly<br/>
        • Regularly fetch updates from remote repositories<br/>
        • Learn to read and understand git log --graph<br/>
        • Use git reflog as a safety net for recovery<br/>
        • Set up GPG signing for verified commits<br/>
        <br/>
        <b>⚠️ Dangerous Commands (use with caution):</b><br/>
        • git reset --hard: Permanently loses uncommitted changes<br/>
        • git push --force: Can overwrite others' work<br/>
        • git rebase: Changes commit history (don't rebase shared branches)<br/>
        • git clean -fd: Permanently deletes untracked files
        """
        
        tips_para = Paragraph(tips_text, self.styles['Normal'])
        
        # Create a colored background table for tips
        tips_table = Table([[tips_para]], colWidths=[17*cm])
        tips_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F0F8E8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#1B4F72')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#2E8B57')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        self.story.append(tips_table)

    def generate_pdf(self):
        """Generate the complete PDF"""
        # Page 1
        self.add_title()
        self.add_basic_commands()
        self.add_branching_commands()
        self.add_remote_commands()
        self.add_inspection_commands()
        
        # Page break
        self.story.append(PageBreak())
        
        # Page 2
        self.add_undoing_commands()
        self.add_stashing_commands()
        self.add_advanced_commands()
        self.add_configuration_commands()
        self.add_workflows_section()
        self.add_tips_section()
        
        # Build PDF
        self.doc.build(self.story)
        print(f"✅ Git Cheat Sheet PDF generated successfully: {self.filename}")
        return self.filename

def main():
    """Main function to generate the PDF"""
    try:
        # Create PDF generator
        pdf_generator = GitCheatSheetPDF("git_cheat_sheet.pdf")
        
        # Generate the PDF
        filename = pdf_generator.generate_pdf()
        
        print(f"\n🌿 Git Cheat Sheet PDF created: {filename}")
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