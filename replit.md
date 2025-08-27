# Business Card Generator

## Overview

This is a Flask-based web application that allows users to create professional business cards with customizable templates, colors, and fonts. The application supports both single card generation and batch processing from CSV files, with multiple export formats including PNG, PDF, and ZIP archives for batch operations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Flask with Jinja2 templating engine
- **UI Framework**: Bootstrap with dark theme integration
- **Interactive Elements**: Vanilla JavaScript for template selection, form validation, and file upload handling
- **Styling**: Custom CSS with Bootstrap overrides for business card preview and template gallery
- **Icons**: Font Awesome for consistent iconography

### Backend Architecture
- **Web Framework**: Flask with session management and file upload capabilities
- **Image Processing**: PIL (Python Imaging Library) for business card image generation
- **PDF Generation**: ReportLab for creating PDF versions of business cards
- **QR Code Generation**: qrcode library for adding QR codes to business cards
- **File Handling**: Secure file upload with extension validation and size limits (16MB max)

### Data Processing
- **CSV Processing**: Built-in csv module for batch card generation
- **Template System**: Static template definitions with configurable colors, fonts, and layouts
- **Image Export**: Multiple format support (PNG, JPG, PDF) with high DPI output (300 DPI)

### Security Features
- **File Upload Security**: Whitelist-based file extension validation
- **Secure Filenames**: Werkzeug's secure_filename for safe file handling
- **Session Management**: Flask sessions with configurable secret key
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies

### Application Structure
- **Route Organization**: RESTful endpoints for different functionalities (index, preview, batch processing)
- **Template Inheritance**: Base template with consistent navigation and layout
- **Static Asset Management**: Organized CSS and JavaScript files in static directory
- **Error Handling**: Flash messaging system for user feedback

## External Dependencies

### Core Dependencies
- **Flask**: Web framework for application structure and routing
- **PIL (Pillow)**: Image processing library for business card generation
- **ReportLab**: PDF generation library for creating printable business cards
- **qrcode**: QR code generation for embedding contact information

### Frontend Dependencies
- **Bootstrap**: CSS framework loaded via CDN with dark theme
- **Font Awesome**: Icon library loaded via CDN for UI elements
- **Custom Fonts**: System fonts (Arial, Helvetica, Times New Roman, Georgia, Verdana)

### File System Dependencies
- **Upload Directory**: Local file storage for uploaded CSV files and images
- **Export Directory**: Temporary storage for generated business card files
- **Template Directory**: Flask template system for HTML rendering

### Development Dependencies
- **Werkzeug**: WSGI utilities for secure file handling and proxy support
- **Python Standard Library**: os, logging, tempfile, zipfile, csv, io, uuid modules