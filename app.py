import os
import logging
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import zipfile
import csv
import io
import tempfile
from card_generator import CardGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
UPLOAD_FOLDER = 'uploads'
EXPORT_FOLDER = 'exports'
ALLOWED_EXTENSIONS = {'csv', 'png', 'jpg', 'jpeg', 'gif', 'svg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXPORT_FOLDER'] = EXPORT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with business card form and template selector"""
    templates = CardGenerator.get_available_templates()
    fonts = CardGenerator.get_available_fonts()
    colors = CardGenerator.get_available_colors()
    return render_template('index.html', templates=templates, fonts=fonts, colors=colors)

@app.route('/preview', methods=['POST'])
def preview():
    """Generate preview of business card"""
    try:
        # Get form data
        card_data = {
            'name': request.form.get('name', ''),
            'job_title': request.form.get('job_title', ''),
            'company': request.form.get('company', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'website': request.form.get('website', ''),
            'address': request.form.get('address', ''),
            'template': request.form.get('template', 'modern'),
            'font': request.form.get('font', 'Arial'),
            'color': request.form.get('color', 'blue'),
            'text_align': request.form.get('text_align', 'left'),
            'include_qr': request.form.get('include_qr') == 'on'
        }
        
        # Handle logo upload
        logo_file = None
        if 'logo' in request.files and request.files['logo'].filename:
            file = request.files['logo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(logo_path)
                logo_file = logo_path
        
        generator = CardGenerator()
        preview_path = generator.generate_preview(card_data, logo_file)
        
        return render_template('preview.html', 
                             card_data=card_data, 
                             preview_image=preview_path,
                             logo_file=logo_file)
    
    except Exception as e:
        logging.error(f"Error in preview: {str(e)}")
        flash(f'Error generating preview: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/export/<format>')
def export_card(format):
    """Export business card in specified format"""
    try:
        # Get card data from session or form
        card_data = request.args.to_dict()
        
        generator = CardGenerator()
        
        if format == 'png':
            file_path = generator.generate_png(card_data)
            return send_file(file_path, as_attachment=True, download_name='business_card.png')
        
        elif format == 'pdf':
            file_path = generator.generate_pdf(card_data)
            return send_file(file_path, as_attachment=True, download_name='business_card.pdf')
        
        elif format == 'pdf_print':
            file_path = generator.generate_print_pdf(card_data)
            return send_file(file_path, as_attachment=True, download_name='business_card_print.pdf')
        
        elif format == 'html':
            file_path = generator.generate_animated_html(card_data)
            return send_file(file_path, as_attachment=True, download_name='business_card.html')
        
        else:
            flash('Invalid export format', 'error')
            return redirect(url_for('index'))
    
    except Exception as e:
        logging.error(f"Error in export: {str(e)}")
        flash(f'Error exporting card: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/batch')
def batch():
    """Batch processing page"""
    return render_template('batch.html')

@app.route('/batch/upload', methods=['POST'])
def batch_upload():
    """Handle CSV upload for batch processing"""
    try:
        if 'csv_file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(url_for('batch'))
        
        file = request.files['csv_file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('batch'))
        
        if not file.filename or not file.filename.lower().endswith('.csv'):
            flash('Please upload a CSV file', 'error')
            return redirect(url_for('batch'))
        
        # Read CSV data
        csv_data = []
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        for row in csv_reader:
            csv_data.append(row)
        
        if not csv_data:
            flash('CSV file is empty or invalid', 'error')
            return redirect(url_for('batch'))
        
        # Get batch settings
        template = request.form.get('batch_template', 'modern')
        font = request.form.get('batch_font', 'Arial')
        color = request.form.get('batch_color', 'blue')
        export_format = request.form.get('batch_format', 'png')
        
        # Generate batch cards
        generator = CardGenerator()
        zip_path = generator.generate_batch(csv_data, template, font, color, export_format)
        
        return send_file(zip_path, as_attachment=True, download_name='business_cards_batch.zip')
    
    except Exception as e:
        logging.error(f"Error in batch upload: {str(e)}")
        flash(f'Error processing batch: {str(e)}', 'error')
        return redirect(url_for('batch'))

@app.route('/api/preview', methods=['POST'])
def api_preview():
    """AJAX endpoint for real-time preview updates"""
    try:
        card_data = request.json
        generator = CardGenerator()
        preview_path = generator.generate_preview(card_data)
        return jsonify({'success': True, 'preview_url': preview_path})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
