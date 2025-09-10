#!/usr/bin/env python3
"""
Laravel 11 Cheat Sheet PDF Generator
Creates a comprehensive, colorful, well-formatted A4 PDF Laravel command reference
Includes modern Laravel features, Docker Sail, API development, and best practices
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
import html

class LaravelCheatSheetPDF:
    def __init__(self, filename="laravel_cheat_sheet.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=A4,
                                   rightMargin=1*cm, leftMargin=1*cm,
                                   topMargin=1.5*cm, bottomMargin=1*cm)
        self.styles = getSampleStyleSheet()
        self.story = []

        # Define color scheme (Laravel colors + new green for Laravel 11)
        self.colors = {
            'header': HexColor('#FF2D20'),      # Laravel Red
            'section': HexColor('#F39C12'),     # Orange
            'basic_command': HexColor('#E74C3C'),     # Red for basic commands
            'advanced_command': HexColor('#3498DB'),  # Blue for commands with options/flags
            'important_command': HexColor('#E67E22'), # Orange for important commands
            'new_feature': HexColor('#27AE60'),       # Green for Laravel 11 features
            'description': HexColor('#2C3E50'), # Dark gray
            'background': HexColor('#F8F9FA'),  # Light gray
            'accent': HexColor('#3498DB'),      # Blue
            'warning': HexColor('#E67E22')      # Orange for important
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

    def create_command_table(self, title, commands_with_colors, col_widths=None, important_commands=None):
        """Create a formatted table for commands with flexible column sizing"""
        if important_commands is None:
            important_commands = []

        # Add section header
        self.story.append(Paragraph(title, self.styles['SectionHeader']))

        # Calculate flexible column widths based on available page width
        if col_widths is None:
            # Get available width (page width minus margins)
            available_width = A4[0] - 2*cm  # Total width minus left and right margins
            # Use flex-like distribution: 60% for commands, 40% for descriptions
            col_widths = [available_width * 0.6, available_width * 0.4]

        # Prepare table data
        data = []
        for item in commands_with_colors:
            if len(item) == 3:  # (command, description, color)
                cmd, desc, color = item
            else:  # (command, description) - default to blue
                cmd, desc = item
                color = '#3498DB'  # Default blue for popular commands
            
            # Escape special characters in command and description
            escaped_cmd = html.escape(cmd)
            escaped_desc = html.escape(desc)

            data.append([
                Paragraph(f"<font name='Courier-Bold' color='{color}'>{escaped_cmd}</font>", self.styles['Normal']),
                Paragraph(escaped_desc, self.styles['Normal'])
            ])

        # Create table with flexible column sizing
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
        title = Paragraph("Laravel 11 Cheat Sheet", self.styles['MainTitle'])
        self.story.append(title)
        self.story.append(Spacer(1, 0.3*cm))
        
        # Add color legend
        legend_text = """
        <b>Color Legend:</b> 
        <font name='Courier-Bold' color='#3498DB'>Blue = Essential/Daily Commands</font> | 
        <font name='Courier-Bold' color='#E74C3C'>Red = Advanced/Specialized Commands</font> |
        <font name='Courier-Bold' color='#27AE60'>Green = New in Laravel 11</font>
        """
        legend_para = Paragraph(legend_text, self.styles['Normal'])
        
        # Create a table for the legend with background
        legend_table = Table([[legend_para]], colWidths=[17*cm])
        legend_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F0F8FF')),
            ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#BDC3C7')),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        self.story.append(legend_table)
        self.story.append(Spacer(1, 0.5*cm))

    def add_installation_commands(self):
        """Add installation and setup commands"""
        commands = [
            ("composer create-project laravel/laravel app-name", "Create new Laravel project", '#3498DB'),  # Blue - Popular
            ("composer global require laravel/installer", "Install Laravel installer globally", '#E74C3C'),  # Red - One-time setup
            ("laravel new app-name", "Create new Laravel project using installer", '#3498DB'),  # Blue - Popular
            ("laravel new app-name --git", "Create new project with git repo", '#27AE60'),  # Green - Laravel 11
            ("laravel new app-name --database=mysql", "Create project with specific database", '#27AE60'),  # Green - Laravel 11
            ("php artisan serve", "Start development server", '#3498DB'),  # Blue - Very Popular
            ("php artisan serve --host=0.0.0.0 --port=8080", "Start server with custom host/port", '#3498DB'),  # Blue - Common
            ("php artisan --version", "Check Laravel version", '#3498DB'),  # Blue - Popular
            ("composer update", "Update Laravel dependencies", '#3498DB'),  # Blue - Popular
            ("composer install", "Install project dependencies", '#3498DB'),  # Blue - Popular
            ("composer install --no-dev --optimize-autoloader", "Production install", '#3498DB'),  # Blue - Production
            ("npm install", "Install Node.js dependencies", '#3498DB'),  # Blue - Popular
            ("npm run dev", "Compile assets for development", '#3498DB'),  # Blue - Popular
            ("npm run build", "Compile assets for production", '#3498DB'),  # Blue - Regular use
            ("npm run watch", "Watch and recompile assets", '#3498DB'),  # Blue - Development
        ]
        self.create_command_table("Installation & Setup", commands)

    def add_artisan_commands(self):
        """Add Artisan commands"""
        commands = [
            ("php artisan list", "List all available commands", '#3498DB'),  # Blue - Used for reference
            ("php artisan help <command>", "Get help for specific command", '#3498DB'),  # Blue - Used when learning
            ("php artisan make:model <name>", "Create new model", '#3498DB'),  # Blue - Used in every project
            ("php artisan make:model <name> -m", "Create model with migration", '#3498DB'),  # Blue - Very common
            ("php artisan make:model <name> -mrc", "Create model, migration, resource controller", '#3498DB'),  # Blue - Common pattern
            ("php artisan make:model <name> -a", "Create model with all (migration, factory, seeder, policy, controller, form requests)", '#E74C3C'),  # Red - Rarely use all at once
            ("php artisan make:controller <name>", "Create new controller", '#3498DB'),  # Blue - Used in every project
            ("php artisan make:controller <name> --resource", "Create resource controller", '#3498DB'),  # Blue - Very common
            ("php artisan make:controller <name> --api", "Create API resource controller", '#3498DB'),  # Blue - Common for APIs
            ("php artisan make:controller <name> --invokable", "Create single action controller", '#E74C3C'),  # Red - Rarely used
            ("php artisan make:migration <name>", "Create new migration", '#3498DB'),  # Blue - Used in every project
            ("php artisan make:migration create_users_table", "Create migration with specific name", '#3498DB'),  # Blue - Common
            ("php artisan make:migration add_column_to_table --table=users", "Add column to existing table", '#3498DB'),  # Blue - Common maintenance
            ("php artisan make:seeder <name>", "Create new seeder", '#3498DB'),  # Blue - Used for test data
            ("php artisan make:seeder UserSeeder", "Create specific seeder", '#3498DB'),  # Blue - Common
            ("php artisan make:factory <name>", "Create new factory", '#3498DB'),  # Blue - Used for testing
            ("php artisan make:factory UserFactory --model=User", "Create factory for specific model", '#3498DB'),  # Blue - Common
            ("php artisan make:request <name>", "Create new form request", '#3498DB'),  # Blue - Used for validation
            ("php artisan make:request StoreUserRequest", "Create specific form request", '#3498DB'),  # Blue - Common
            ("php artisan make:middleware <name>", "Create new middleware", '#3498DB'),  # Blue - Used in most projects
            ("php artisan make:middleware CheckAge", "Create specific middleware", '#3498DB'),  # Blue - Common
            ("php artisan make:policy <name>", "Create new policy", '#3498DB'),  # Blue - Used for authorization
            ("php artisan make:policy UserPolicy --model=User", "Create policy for specific model", '#3498DB'),  # Blue - Common
            ("php artisan make:event <name>", "Create new event", '#E74C3C'),  # Red - Not used in every project
            ("php artisan make:listener <name>", "Create new listener", '#E74C3C'),  # Red - Not used in every project
            ("php artisan make:listener SendWelcomeEmail --event=UserRegistered", "Create listener for specific event", '#E74C3C'),  # Red - Advanced
            ("php artisan make:job <name>", "Create new job", '#3498DB'),  # Blue - Common for background tasks
            ("php artisan make:job ProcessPayment", "Create specific job", '#3498DB'),  # Blue - Common
            ("php artisan make:mail <name>", "Create new mail class", '#3498DB'),  # Blue - Used in most projects
            ("php artisan make:mail WelcomeEmail --markdown=emails.welcome", "Create mail with markdown template", '#3498DB'),  # Blue - Common
            ("php artisan make:notification <name>", "Create new notification", '#E74C3C'),  # Red - Not used in every project
            ("php artisan make:resource <name>", "Create new API resource", '#3498DB'),  # Blue - Common for APIs
            ("php artisan make:resource UserResource", "Create specific API resource", '#3498DB'),  # Blue - Common
            ("php artisan make:test <name>", "Create new test", '#3498DB'),  # Blue - Used in most projects
            ("php artisan make:test UserTest --unit", "Create unit test", '#3498DB'),  # Blue - Common
            ("php artisan make:test UserCanLoginTest --feature", "Create feature test", '#3498DB'),  # Blue - Common
            ("php artisan make:command <name>", "Create new artisan command", '#E74C3C'),  # Red - Advanced/rare
            ("php artisan make:provider <name>", "Create new service provider", '#E74C3C'),  # Red - Advanced
            ("php artisan make:rule <name>", "Create new validation rule", '#E74C3C'),  # Red - Rarely needed
            ("php artisan make:cast <name>", "Create new custom cast", '#E74C3C'),  # Red - Advanced feature
            ("php artisan make:component <name>", "Create new Blade component", '#3498DB'),  # Blue - Common with Blade
            ("php artisan make:observer <name>", "Create new model observer", '#E74C3C'),  # Red - Advanced feature
        ]
        self.create_command_table("Artisan Commands", commands)

    def add_routing_commands(self):
        """Add routing commands"""
        commands = [
            ("Route::get('/uri', [Controller::class, 'method']);", "Basic GET route", '#3498DB'),  # Blue - Used in every project
            ("Route::post('/uri', [Controller::class, 'method']);", "POST route", '#3498DB'),  # Blue - Used in every project
            ("Route::put('/uri', [Controller::class, 'method']);", "PUT route", '#3498DB'),  # Blue - Common for updates
            ("Route::patch('/uri', [Controller::class, 'method']);", "PATCH route", '#3498DB'),  # Blue - Common for partial updates
            ("Route::delete('/uri', [Controller::class, 'method']);", "DELETE route", '#3498DB'),  # Blue - Common for deletion
            ("Route::any('/uri', [Controller::class, 'method']);", "Route that responds to any HTTP verb", '#E74C3C'),  # Red - Rarely used
            ("Route::match(['get', 'post'], '/uri', [Controller::class, 'method']);", "Route responding to multiple verbs", '#E74C3C'),  # Red - Rarely used
            ("Route::resource('users', UserController::class);", "Resource route", '#3498DB'),  # Blue - Very common
            ("Route::apiResource('users', UserController::class);", "API resource route (no create/edit)", '#3498DB'),  # Blue - Common for APIs
            ("Route::resource('users', UserController::class)->only(['index', 'show']);", "Partial resource routes", '#3498DB'),  # Blue - Common
            ("Route::resource('users', UserController::class)->except(['destroy']);", "Resource routes except destroy", '#3498DB'),  # Blue - Common
            ("Route::group(['prefix' => 'admin'], function () { ... });", "Route group with prefix", '#3498DB'),  # Blue - Common
            ("Route::group(['middleware' => 'auth'], function () { ... });", "Route group with middleware", '#3498DB'),  # Blue - Very common
            ("Route::group(['namespace' => 'Admin'], function () { ... });", "Route group with namespace", '#E74C3C'),  # Red - Rarely used in modern Laravel
            ("Route::middleware(['auth'])->group(function () { ... });", "Route group with middleware", '#3498DB'),  # Blue - Very common
            ("Route::name('profile')->get('/profile', ...);", "Named route", '#3498DB'),  # Blue - Common
            ("route('profile')", "Generate URL for named route", '#3498DB'),  # Blue - Used daily
            ("route('profile', ['id' => 1])", "Generate URL with parameters", '#3498DB'),  # Blue - Common
            ("Route::redirect('/here', '/there');", "Redirect route", '#3498DB'),  # Blue - Common
            ("Route::redirect('/here', '/there', 301);", "Permanent redirect route", '#3498DB'),  # Blue - Common
            ("Route::view('/welcome', 'welcome');", "Return view directly", '#3498DB'),  # Blue - Common for static pages
            ("Route::view('/welcome', 'welcome', ['name' => 'Taylor']);", "Return view with data", '#3498DB'),  # Blue - Common
            ("Route::fallback(function () { ... });", "Fallback route", '#3498DB'),  # Blue - Common for 404 handling
            ("Route::domain('{account}.example.com')->group(...);", "Subdomain routing", '#E74C3C'),  # Red - Advanced/rare
            ("Route::where('id', '[0-9]+')->get('/user/{id}', ...);", "Route parameter constraints", '#3498DB'),  # Blue - Common
            ("Route::whereNumber('id')->get('/user/{id}', ...);", "Numeric parameter constraint", '#3498DB'),  # Blue - Common
            ("Route::whereAlpha('name')->get('/user/{name}', ...);", "Alphabetic parameter constraint", '#E74C3C'),  # Red - Rarely used
            ("Route::whereUuid('id')->get('/user/{id}', ...);", "UUID parameter constraint", '#E74C3C'),  # Red - Advanced
            ("php artisan route:list", "List all routes", '#3498DB'),  # Blue - Used for debugging
            ("php artisan route:list --name=user", "List routes with specific name", '#E74C3C'),  # Red - Rarely needed
            ("php artisan route:list --method=GET", "List routes with specific method", '#E74C3C'),  # Red - Rarely needed
            ("php artisan route:cache", "Cache routes for performance", '#3498DB'),  # Blue - Used in production
            ("php artisan route:clear", "Clear route cache", '#3498DB'),  # Blue - Common debugging
        ]
        # Custom flex ratio for routing: 70% commands, 30% descriptions (commands are longer)
        available_width = A4[0] - 2*cm
        custom_widths = [available_width * 0.7, available_width * 0.3]
        self.create_command_table("Routing", commands, custom_widths)

    def add_database_commands(self):
        """Add database and migration commands"""
        commands = [
            ("php artisan migrate", "Run pending migrations", '#3498DB'),  # Blue - Used in every project
            ("php artisan migrate --force", "Force run migrations in production", '#3498DB'),  # Blue - Used in deployment
            ("php artisan migrate --pretend", "Show SQL that would be executed", '#E74C3C'),  # Red - Debugging only
            ("php artisan migrate --step", "Run migrations one by one", '#E74C3C'),  # Red - Rarely needed
            ("php artisan migrate:rollback", "Rollback last migration", '#3498DB'),  # Blue - Common debugging
            ("php artisan migrate:rollback --step=5", "Rollback specific number of migrations", '#3498DB'),  # Blue - Common
            ("php artisan migrate:reset", "Reset all migrations", '#E74C3C'),  # Red - Dangerous, rarely used
            ("php artisan migrate:refresh", "Reset and re-run all migrations", '#3498DB'),  # Blue - Common in development
            ("php artisan migrate:refresh --seed", "Reset, re-run migrations and seed", '#3498DB'),  # Blue - Very common in development
            ("php artisan migrate:fresh", "Drop all tables and re-run migrations", '#3498DB'),  # Blue - Common in development
            ("php artisan migrate:fresh --seed", "Drop all tables, re-run migrations and seed", '#3498DB'),  # Blue - Very common in development
            ("php artisan migrate:status", "Show migration status", '#3498DB'),  # Blue - Used for debugging
            ("php artisan make:migration create_users_table", "Create migration", '#3498DB'),  # Blue - Used in every project
            ("php artisan make:migration add_email_to_users_table --table=users", "Add column migration", '#3498DB'),  # Blue - Very common
            ("php artisan make:migration create_users_table --create=users", "Create table migration", '#3498DB'),  # Blue - Common
            ("php artisan db:seed", "Run database seeders", '#3498DB'),  # Blue - Used in development and testing
            ("php artisan db:seed --class=UserSeeder", "Run specific seeder", '#3498DB'),  # Blue - Common
            ("php artisan db:seed --force", "Force run seeders in production", '#E74C3C'),  # Red - Rarely used in production
            ("php artisan db:wipe", "Drop all tables, views, and types", '#E74C3C'),  # Red - Dangerous, rarely used
            ("php artisan db:show", "Display information about database", '#E74C3C'),  # Red - Debugging only
            ("php artisan db:table users", "Display information about table", '#E74C3C'),  # Red - Debugging only
            ("php artisan db:monitor", "Monitor database connections", '#E74C3C'),  # Red - Advanced monitoring
            ("php artisan tinker", "Interactive PHP shell", '#3498DB'),  # Blue - Used for testing and debugging
            ("php artisan schema:dump", "Dump current database schema", '#E74C3C'),  # Red - Advanced feature
            ("php artisan schema:dump --prune", "Dump schema and prune migration files", '#E74C3C'),  # Red - Advanced feature
        ]
        self.create_command_table("Database & Migrations", commands)

    def add_eloquent_commands(self):
        """Add Eloquent ORM commands"""
        commands = [
            ("User::all()", "Get all records", '#3498DB'),  # Blue - Used in every project
            ("User::find($id)", "Find record by ID", '#3498DB'),  # Blue - Used daily
            ("User::findOrFail($id)", "Find record by ID or throw exception", '#3498DB'),  # Blue - Common for safety
            ("User::first()", "Get first record", '#3498DB'),  # Blue - Very common
            ("User::firstOrFail()", "Get first record or throw exception", '#3498DB'),  # Blue - Common for safety
            ("User::latest()->get()", "Get records ordered by latest", '#3498DB'),  # Blue - Very common
            ("User::oldest()->get()", "Get records ordered by oldest", '#3498DB'),  # Blue - Common
            ("User::where('name', 'John')->get()", "Query with where clause", '#3498DB'),  # Blue - Used daily
            ("User::where('age', '>', 18)->get()", "Query with comparison operator", '#3498DB'),  # Blue - Very common
            ("User::whereIn('id', [1, 2, 3])->get()", "Query with whereIn", '#3498DB'),  # Blue - Common
            ("User::whereBetween('age', [18, 65])->get()", "Query with whereBetween", '#3498DB'),  # Blue - Common
            ("User::whereNull('email_verified_at')->get()", "Query with whereNull", '#3498DB'),  # Blue - Common
            ("User::whereNotNull('email_verified_at')->get()", "Query with whereNotNull", '#3498DB'),  # Blue - Common
            ("User::whereDate('created_at', '2023-01-01')->get()", "Query by date", '#3498DB'),  # Blue - Common
            ("User::whereYear('created_at', 2023)->get()", "Query by year", '#E74C3C'),  # Red - Less common
            ("User::whereMonth('created_at', 1)->get()", "Query by month", '#E74C3C'),  # Red - Less common
            ("User::select('name', 'email')->get()", "Select specific columns", '#3498DB'),  # Blue - Common optimization
            ("User::distinct()->get()", "Get distinct records", '#E74C3C'),  # Red - Rarely needed
            ("User::orderBy('name', 'asc')->get()", "Order results ascending", '#3498DB'),  # Blue - Very common
            ("User::orderBy('created_at', 'desc')->get()", "Order results descending", '#3498DB'),  # Blue - Very common
            ("User::take(10)->get()", "Limit results", '#3498DB'),  # Blue - Common
            ("User::skip(10)->take(10)->get()", "Skip and take (pagination)", '#E74C3C'),  # Red - Rarely used directly
            ("User::paginate(15)", "Paginate results", '#3498DB'),  # Blue - Used in every project
            ("User::simplePaginate(15)", "Simple pagination", '#3498DB'),  # Blue - Common alternative
            ("User::count()", "Count records", '#3498DB'),  # Blue - Very common
            ("User::max('age')", "Get maximum value", '#3498DB'),  # Blue - Common
            ("User::min('age')", "Get minimum value", '#3498DB'),  # Blue - Common
            ("User::avg('age')", "Get average value", '#3498DB'),  # Blue - Common
            ("User::sum('salary')", "Get sum of values", '#3498DB'),  # Blue - Common
            ("User::create(['name' => 'John', 'email' => '...'])", "Create new record", '#3498DB'),  # Blue - Used daily
            ("User::insert([['name' => 'John'], ['name' => 'Jane']])", "Insert multiple records", '#3498DB'),  # Blue - Common for bulk inserts
            ("User::updateOrCreate(['email' => '...'], ['name' => 'John'])", "Update or create record", '#3498DB'),  # Blue - Very common pattern
            ("User::firstOrCreate(['email' => '...'], ['name' => 'John'])", "Find or create record", '#3498DB'),  # Blue - Very common pattern
            ("$user->update(['name' => 'Jane'])", "Update record", '#3498DB'),  # Blue - Used daily
            ("User::where('active', false)->update(['active' => true])", "Update multiple records", '#3498DB'),  # Blue - Common
            ("$user->delete()", "Delete record", '#3498DB'),  # Blue - Used daily
            ("User::destroy([1, 2, 3])", "Delete multiple records by ID", '#3498DB'),  # Blue - Common
            ("User::where('active', false)->delete()", "Delete multiple records by query", '#3498DB'),  # Blue - Common
            ("User::with('posts')->get()", "Eager loading", '#3498DB'),  # Blue - Essential for performance
            ("User::with(['posts', 'comments'])->get()", "Multiple eager loading", '#3498DB'),  # Blue - Very common
            ("User::with('posts:id,title,user_id')->get()", "Eager loading specific columns", '#3498DB'),  # Blue - Common optimization
            ("User::withCount('posts')->get()", "Eager loading with count", '#3498DB'),  # Blue - Common
        ]
        self.create_command_table("Eloquent ORM", commands)

    def add_blade_commands(self):
        """Add Blade template commands"""
        commands = [
            ("{{ $variable }}", "Echo variable (escaped)", '#3498DB'),  # Blue - Used in every blade template
            ("{!! $variable !!}", "Echo variable (unescaped)", '#3498DB'),  # Blue - Common for HTML content
            ("@if($condition) ... @endif", "Conditional statement", '#3498DB'),  # Blue - Used in every project
            ("@foreach($items as $item) ... @endforeach", "Loop through items", '#3498DB'),  # Blue - Used in every project
            ("@extends('layout.app')", "Extend layout", '#3498DB'),  # Blue - Used in every view
            ("@section('content') ... @endsection", "Define section", '#3498DB'),  # Blue - Used in every view
            ("@yield('content')", "Yield section content", '#3498DB'),  # Blue - Used in every layout
            ("@include('partials.header')", "Include partial view", '#3498DB'),  # Blue - Very common
            ("@auth ... @endauth", "Check if user is authenticated", '#3498DB'),  # Blue - Very common
            ("@guest ... @endguest", "Check if user is guest", '#3498DB'),  # Blue - Very common
            ("@csrf", "CSRF token field", '#3498DB'),  # Blue - Used in every form
            ("@method('PUT')", "Method spoofing field", '#3498DB'),  # Blue - Common in forms
        ]
        # Custom flex ratio for blade: 50% commands, 50% descriptions (more balanced)
        available_width = A4[0] - 2*cm
        custom_widths = [available_width * 0.5, available_width * 0.5]
        self.create_command_table("Blade Templates", commands, custom_widths)

    def add_auth_commands(self):
        """Add authentication commands"""
        commands = [
            ("php artisan make:auth", "Scaffold authentication views", '#E74C3C'),  # Red - Deprecated/rarely used
            ("php artisan ui:auth", "Generate authentication scaffolding", '#E74C3C'),  # Red - Older method
            ("Auth::check()", "Check if user is authenticated", '#3498DB'),  # Blue - Used daily
            ("Auth::user()", "Get authenticated user", '#3498DB'),  # Blue - Used daily
            ("Auth::login($user)", "Log in user", '#3498DB'),  # Blue - Common
            ("Auth::logout()", "Log out user", '#3498DB'),  # Blue - Common
            ("auth()->user()", "Helper for authenticated user", '#3498DB'),  # Blue - Very common
            ("auth()->check()", "Helper to check authentication", '#3498DB'),  # Blue - Very common
            ("@auth ... @endauth", "Blade directive for auth check", '#3498DB'),  # Blue - Very common
            ("Route::middleware('auth')->group(...)", "Protect routes with auth", '#3498DB'),  # Blue - Very common
        ]
        self.create_command_table("Authentication", commands)

    def add_middleware_commands(self):
        """Add middleware commands"""
        commands = [
            ("php artisan make:middleware CheckAge", "Create middleware", '#3498DB'),  # Blue - Common
            ("Route::middleware('auth')->get(...)", "Apply middleware to route", '#3498DB'),  # Blue - Very common
            ("Route::middleware(['auth', 'admin'])->get(...)", "Multiple middleware", '#3498DB'),  # Blue - Common
            ("protected $middleware = [...] in Kernel.php", "Global middleware", '#E74C3C'),  # Red - Advanced configuration
            ("protected $middlewareGroups = [...] in Kernel.php", "Middleware groups", '#E74C3C'),  # Red - Advanced configuration
            ("protected $routeMiddleware = [...] in Kernel.php", "Route middleware", '#3498DB'),  # Blue - Common configuration
            ("$request->user()", "Access user in middleware", '#3498DB'),  # Blue - Common
            ("return $next($request)", "Pass request to next middleware", '#3498DB'),  # Blue - Used in every middleware
            ("abort(403)", "Deny access in middleware", '#3498DB'),  # Blue - Common
        ]
        self.create_command_table("Middleware", commands)

    def add_testing_commands(self):
        """Add testing commands"""
        commands = [
            ("php artisan make:test UserTest", "Create test class", '#3498DB'),  # Blue - Common
            ("php artisan test", "Run all tests", '#3498DB'),  # Blue - Used regularly
            ("php artisan test --filter=UserTest", "Run specific test", '#3498DB'),  # Blue - Common debugging
            ("$this->assertEquals($expected, $actual)", "Assert equality", '#3498DB'),  # Blue - Used in every test
            ("$this->assertTrue($condition)", "Assert true", '#3498DB'),  # Blue - Used in every test
            ("$this->assertDatabaseHas('users', [...])", "Assert database record exists", '#3498DB'),  # Blue - Very common
            ("$this->get('/users')", "Make GET request in test", '#3498DB'),  # Blue - Used in every feature test
            ("$this->post('/users', $data)", "Make POST request in test", '#3498DB'),  # Blue - Used in every feature test
            ("$this->actingAs($user)", "Authenticate user in test", '#3498DB'),  # Blue - Very common
            ("$this->assertRedirect('/dashboard')", "Assert redirect", '#3498DB'),  # Blue - Common
        ]
        self.create_command_table("Testing", commands)

    def add_deployment_commands(self):
        """Add deployment commands"""
        commands = [
            ("php artisan config:cache", "Cache configuration", '#3498DB'),  # Blue - Used in every deployment
            ("php artisan route:cache", "Cache routes", '#3498DB'),  # Blue - Used in every deployment
            ("php artisan view:cache", "Cache views", '#3498DB'),  # Blue - Used in every deployment
            ("php artisan config:clear", "Clear config cache", '#3498DB'),  # Blue - Common debugging
            ("php artisan route:clear", "Clear route cache", '#3498DB'),  # Blue - Common debugging
            ("php artisan view:clear", "Clear view cache", '#3498DB'),  # Blue - Common debugging
            ("php artisan cache:clear", "Clear application cache", '#3498DB'),  # Blue - Common debugging
            ("composer install --optimize-autoloader --no-dev", "Optimize for production", '#3498DB'),  # Blue - Used in every deployment
            ("php artisan migrate --force", "Run migrations in production", '#3498DB'),  # Blue - Used in every deployment
            ("npm run build", "Build assets for production", '#3498DB'),  # Blue - Used in every deployment
        ]
        self.create_command_table("Deployment & Optimization", commands)

    def add_queue_commands(self):
        """Add queue and job commands"""
        commands = [
            ("php artisan queue:work", "Start processing jobs", '#3498DB'),  # Blue - Used daily in production
            ("php artisan queue:listen", "Listen for new jobs", '#3498DB'),  # Blue - Common for development
            ("php artisan queue:restart", "Restart queue workers", '#3498DB'),  # Blue - Used in deployment
            ("php artisan queue:failed", "List failed jobs", '#3498DB'),  # Blue - Common debugging
            ("php artisan queue:retry all", "Retry all failed jobs", '#3498DB'),  # Blue - Common recovery
            ("php artisan queue:retry 5", "Retry specific failed job", '#3498DB'),  # Blue - Common debugging
            ("php artisan queue:flush", "Delete all failed jobs", '#E74C3C'),  # Red - Rarely used
            ("php artisan queue:clear", "Delete all jobs from queue", '#E74C3C'),  # Red - Dangerous
            ("php artisan make:job ProcessPayment", "Create new job", '#3498DB'),  # Blue - Common
            ("php artisan horizon", "Start Laravel Horizon dashboard", '#27AE60'),  # Green - Laravel 11 feature
        ]
        self.create_command_table("Queues & Jobs", commands)

    def add_cache_commands(self):
        """Add cache commands"""
        commands = [
            ("Cache::put('key', 'value', 3600)", "Store cache item", '#3498DB'),  # Blue - Used daily
            ("Cache::get('key')", "Get cache item", '#3498DB'),  # Blue - Used daily
            ("Cache::remember('key', 3600, fn() => expensive_operation())", "Cache with fallback", '#3498DB'),  # Blue - Very common
            ("Cache::forget('key')", "Remove cache item", '#3498DB'),  # Blue - Common
            ("Cache::flush()", "Clear all cache", '#3498DB'),  # Blue - Common debugging
            ("php artisan cache:clear", "Clear application cache", '#3498DB'),  # Blue - Common debugging
            ("php artisan cache:forget key", "Forget specific cache key", '#E74C3C'),  # Red - Rarely used
            ("Cache::tags(['people', 'artists'])->put('John', $john, 60)", "Tagged cache", '#E74C3C'),  # Red - Advanced
            ("Cache::lock('order-processing')->get(function () {...})", "Cache locks", '#27AE60'),  # Green - Laravel 11 improvement
        ]
        self.create_command_table("Cache Management", commands)

    def add_validation_commands(self):
        """Add validation commands"""
        commands = [
            ("$request->validate(['email' => 'required|email'])", "Basic validation", '#3498DB'),  # Blue - Used daily
            ("'required|string|max:255'", "Common string validation", '#3498DB'),  # Blue - Used daily
            ("'required|email|unique:users'", "Email validation with unique", '#3498DB'),  # Blue - Very common
            ("'nullable|integer|min:1'", "Optional integer validation", '#3498DB'),  # Blue - Common
            ("'required|array|min:1'", "Array validation", '#3498DB'),  # Blue - Common
            ("'required|file|mimes:jpg,png|max:2048'", "File validation", '#3498DB'),  # Blue - Common for uploads
            ("'required|date|after:today'", "Date validation", '#3498DB'),  # Blue - Common
            ("'required|confirmed'", "Password confirmation", '#3498DB'),  # Blue - Common for forms
            ("'sometimes|nullable|string'", "Conditional validation", '#3498DB'),  # Blue - Common
            ("Rule::exists('users', 'id')", "Database validation rule", '#3498DB'),  # Blue - Common
            ("Rule::unique('users')->ignore($user->id)", "Unique with ignore", '#3498DB'),  # Blue - Common for updates
            ("'required|regex:/^[A-Za-z]+$/'", "Regex validation", '#E74C3C'),  # Red - Advanced
            ("php artisan make:rule Uppercase", "Custom validation rule", '#E74C3C'),  # Red - Advanced
        ]
        self.create_command_table("Validation Rules", commands)

    def add_api_commands(self):
        """Add API development commands"""
        commands = [
            ("php artisan make:resource UserResource", "Create API resource", '#3498DB'),  # Blue - Common for APIs
            ("php artisan make:resource UserCollection", "Create API collection", '#3498DB'),  # Blue - Common for APIs
            ("return new UserResource($user)", "Return single resource", '#3498DB'),  # Blue - Used in every API controller
            ("return UserResource::collection($users)", "Return resource collection", '#3498DB'),  # Blue - Used in every API controller
            ("php artisan install:api", "Install Laravel Sanctum", '#27AE60'),  # Green - Laravel 11 command
            ("$user->createToken('token-name')", "Create API token", '#3498DB'),  # Blue - Common for API auth
            ("Route::middleware('auth:sanctum')->get(...)", "Protect API route", '#3498DB'),  # Blue - Used in every protected API
            ("return response()->json($data)", "Return JSON response", '#3498DB'),  # Blue - Used in every API controller
            ("return response()->json($data, 201)", "Return JSON with status", '#3498DB'),  # Blue - Common for created responses
            ("abort_if($condition, 403)", "Conditional abort", '#3498DB'),  # Blue - Common for API authorization
            ("$request->expectsJson()", "Check if request expects JSON", '#E74C3C'),  # Red - Advanced API handling
        ]
        self.create_command_table("API Development", commands)

    def add_storage_commands(self):
        """Add storage and file commands"""
        commands = [
            ("Storage::disk('public')->put('file.txt', $contents)", "Store file", '#3498DB'),  # Blue - Common
            ("Storage::get('file.txt')", "Get file contents", '#3498DB'),  # Blue - Common
            ("Storage::download('file.txt')", "Download file", '#3498DB'),  # Blue - Common
            ("Storage::delete('file.txt')", "Delete file", '#3498DB'),  # Blue - Common
            ("Storage::exists('file.txt')", "Check if file exists", '#3498DB'),  # Blue - Common
            ("$request->file('upload')->store('uploads')", "Store uploaded file", '#3498DB'),  # Blue - Very common
            ("php artisan storage:link", "Create storage symlink", '#3498DB'),  # Blue - Used in every project with uploads
            ("Storage::url('file.txt')", "Get file URL", '#3498DB'),  # Blue - Common
            ("Storage::size('file.txt')", "Get file size", '#E74C3C'),  # Red - Rarely needed
            ("Storage::lastModified('file.txt')", "Get last modified time", '#E74C3C'),  # Red - Rarely needed
        ]
        self.create_command_table("Storage & Files", commands)

    def add_sail_commands(self):
        """Add Laravel Sail (Docker) commands"""
        commands = [
            ("./vendor/bin/sail up", "Start all services", '#27AE60'),  # Green - Laravel 11 improvement
            ("./vendor/bin/sail up -d", "Start services in background", '#27AE60'),  # Green - Laravel 11
            ("./vendor/bin/sail down", "Stop all services", '#27AE60'),  # Green - Laravel 11
            ("./vendor/bin/sail artisan migrate", "Run migrations in container", '#27AE60'),  # Green - Laravel 11
            ("./vendor/bin/sail composer install", "Install dependencies in container", '#27AE60'),  # Green - Laravel 11
            ("./vendor/bin/sail npm run dev", "Run npm in container", '#27AE60'),  # Green - Laravel 11
            ("./vendor/bin/sail test", "Run tests in container", '#27AE60'),  # Green - Laravel 11
            ("./vendor/bin/sail shell", "Access container shell", '#27AE60'),  # Green - Laravel 11
            ("./vendor/bin/sail mysql", "Access MySQL in container", '#27AE60'),  # Green - Laravel 11
            ("./vendor/bin/sail redis", "Access Redis in container", '#27AE60'),  # Green - Laravel 11
        ]
        self.create_command_table("Laravel Sail (Docker)", commands)

    def add_inertia_commands(self):
        """Add Inertia.js commands"""
        commands = [
            ("composer require inertiajs/inertia-laravel", "Install Inertia.js Laravel adapter", '#27AE60'),  # Green - Laravel 11 modern
            ("php artisan inertia:middleware", "Create Inertia middleware", '#27AE60'),  # Green - Setup command
            ("npm install @inertiajs/vue3", "Install Inertia Vue 3 adapter", '#27AE60'),  # Green - Modern stack
            ("npm install @inertiajs/react", "Install Inertia React adapter", '#27AE60'),  # Green - Modern stack
            ("Inertia::render('Users/Index', ['users' => $users])", "Render Inertia page with data", '#3498DB'),  # Blue - Common
            ("return inertia('Users/Show', compact('user'))", "Return Inertia response (helper)", '#3498DB'),  # Blue - Very common
            ("Inertia::location('/dashboard')", "Redirect with Inertia", '#3498DB'),  # Blue - Common for redirects
            ("$request->header('X-Inertia')", "Check if request is from Inertia", '#E74C3C'),  # Red - Advanced
            ("Inertia::share('auth.user', fn() => auth()->user())", "Share data globally", '#3498DB'),  # Blue - Common setup
            ("Inertia::version(fn() => md5_file(public_path('mix-manifest.json')))", "Asset versioning", '#E74C3C'),  # Red - Advanced
            ("<Head title='Page Title' />", "Set page title (Vue/React)", '#3498DB'),  # Blue - Common
            ("$page.props.user", "Access shared props (Vue/React)", '#3498DB'),  # Blue - Used daily
            ("import { Link } from '@inertiajs/vue3'", "Inertia Link component (Vue)", '#3498DB'),  # Blue - Common
            ("import { router } from '@inertiajs/vue3'", "Inertia router (Vue)", '#3498DB'),  # Blue - Common
            ("router.visit('/users')", "Programmatic navigation", '#3498DB'),  # Blue - Common
            ("router.post('/users', form)", "POST request with Inertia", '#3498DB'),  # Blue - Common
            ("$page.props.errors", "Access validation errors", '#3498DB'),  # Blue - Common in forms
        ]
        self.create_command_table("Inertia.js Integration", commands)

    def add_livewire_commands(self):
        """Add Livewire commands"""
        commands = [
            ("composer require livewire/livewire", "Install Livewire", '#27AE60'),  # Green - Laravel 11 modern
            ("php artisan make:livewire Counter", "Create Livewire component", '#27AE60'),  # Green - Common
            ("php artisan make:livewire Users/Index", "Create nested Livewire component", '#27AE60'),  # Green - Common
            ("<livewire:counter />", "Render Livewire component", '#3498DB'),  # Blue - Used daily
            ("@livewire('counter')", "Render with Blade directive", '#3498DB'),  # Blue - Common alternative
            ("public $count = 0;", "Define public property", '#3498DB'),  # Blue - Basic usage
            ("public function increment() { $this->count++; }", "Define action method", '#3498DB'),  # Blue - Common
            ("wire:click='increment'", "Wire click event", '#3498DB'),  # Blue - Very common
            ("wire:model='name'", "Two-way data binding", '#3498DB'),  # Blue - Very common
            ("wire:submit.prevent='save'", "Wire form submission", '#3498DB'),  # Blue - Common in forms
            ("$this->validate(['name' => 'required']);", "Validate in Livewire", '#3498DB'),  # Blue - Common
            ("$this->emit('userSaved');", "Emit event", '#3498DB'),  # Blue - Common for communication
            ("protected $listeners = ['userSaved' => 'refreshUsers'];", "Listen to events", '#3498DB'),  # Blue - Common
            ("wire:loading", "Show loading state", '#3498DB'),  # Blue - Common UX
            ("wire:offline", "Show offline state", '#E74C3C'),  # Red - Advanced UX
            ("$this->skipRender();", "Skip component re-render", '#E74C3C'),  # Red - Performance optimization
        ]
        self.create_command_table("Livewire Components", commands)

    def add_tips_section(self):
        """Add tips and best practices"""
        tips_text = """
        <b>💡 Laravel 11 Tips & Best Practices:</b><br/>
        <br/>
        • Use Eloquent relationships and eager loading for performance<br/>
        • Always validate user input using Form Requests<br/>
        • Leverage middleware for cross-cutting concerns (auth, CORS, etc.)<br/>
        • Use Laravel Sanctum for API authentication<br/>
        • Implement proper error handling with custom exception classes<br/>
        • Use database seeders and factories for testing data<br/>
        • Write comprehensive tests (Feature + Unit tests)<br/>
        • Use Laravel's built-in caching mechanisms (Redis recommended)<br/>
        • Follow PSR standards and use Laravel Pint for code formatting<br/>
        • Use environment variables for all configuration<br/>
        • Implement proper database indexing and query optimization<br/>
        • Use Laravel's queue system for background jobs<br/>
        • Use Laravel Horizon for queue monitoring in production<br/>
        • Leverage Laravel Sail for consistent development environments<br/>
        <br/>
        <b>� Laravel 11 New Features:</b><br/>
        • Improved artisan commands with better UX<br/>
        • Enhanced API resource handling<br/>
        • Better Docker integration with Sail<br/>
        • Improved testing capabilities<br/>
        • Enhanced security features<br/>
        <br/>
        <b>🔧 Essential Packages for Laravel 11:</b><br/>
        • Laravel Debugbar (barryvdh/laravel-debugbar)<br/>
        • Laravel IDE Helper (barryvdh/laravel-ide-helper)<br/>
        • Laravel Telescope (laravel/telescope)<br/>
        • Laravel Horizon (laravel/horizon)<br/>
        • Laravel Sanctum (built-in API authentication)<br/>
        • Laravel Pint (built-in code formatting)<br/>
        • Spatie Laravel packages (permissions, media, etc.)<br/>
        • Laravel Livewire for reactive components<br/>
        • Inertia.js for modern SPA development
        """

        tips_para = Paragraph(tips_text, self.styles['Normal'])

        # Create a colored background table for tips
        tips_table = Table([[tips_para]], colWidths=[17*cm])
        tips_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#F0FFF0')),  # Light green background
            ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#1B4F72')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#27AE60')),  # Green border
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
        self.add_installation_commands()
        self.add_artisan_commands()
        self.add_routing_commands()
        
        # Page break
        self.story.append(PageBreak())

        # Page 2  
        self.add_database_commands()
        self.add_eloquent_commands()
        self.add_blade_commands()
        
        # Page break
        self.story.append(PageBreak())
        
        # Page 3
        self.add_auth_commands()
        self.add_middleware_commands()
        self.add_validation_commands()
        self.add_api_commands()
        
        # Page break
        self.story.append(PageBreak())
        
        # Page 4
        self.add_queue_commands()
        self.add_cache_commands()
        self.add_storage_commands()
        self.add_sail_commands()
        self.add_testing_commands()
        
        # Page break
        self.story.append(PageBreak())
        
        # Page 5
        self.add_inertia_commands()
        self.add_livewire_commands()
        self.add_deployment_commands()
        self.add_tips_section()

        # Build PDF
        self.doc.build(self.story)
        print(f"✅ Laravel 11 Cheat Sheet PDF generated successfully: {self.filename}")
        return self.filename

def main():
    """Main function to generate the PDF"""
    try:
        # Create PDF generator
        pdf_generator = LaravelCheatSheetPDF("laravel_cheat_sheet.pdf")

        # Generate the PDF
        filename = pdf_generator.generate_pdf()

        print(f"\n🚀 Laravel 11 Cheat Sheet PDF created: {filename}")
        print(f"📄 File size: {os.path.getsize(filename)} bytes")
        print(f"📅 Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📋 Features: Installation, Artisan, Routing, Database, Eloquent, Blade, Auth, API, Queues, Cache, Storage, Docker Sail, Inertia.js, Livewire, Testing & Deployment")

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