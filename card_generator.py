import os
import qrcode
from qrcode import constants
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import Color, black, white
import zipfile
import tempfile
import uuid
import logging

class CardGenerator:
    """Business card generator with multiple export formats"""
    
    def __init__(self):
        self.card_width = 400
        self.card_height = 240
        self.dpi = 300
        
    @staticmethod
    def get_available_templates():
        """Return available card templates"""
        return [
            {'id': 'modern', 'name': 'Modern', 'description': 'Clean and minimalist design'},
            {'id': 'classic', 'name': 'Classic', 'description': 'Traditional business card layout'},
            {'id': 'creative', 'name': 'Creative', 'description': 'Bold and colorful design'},
            {'id': 'elegant', 'name': 'Elegant', 'description': 'Sophisticated and professional'},
            {'id': 'tech', 'name': 'Tech', 'description': 'Modern technology-focused design'},
            {'id': 'corporate', 'name': 'Corporate', 'description': 'Professional business style'},
            {'id': 'artistic', 'name': 'Artistic', 'description': 'Creative with artistic flair'},
            {'id': 'minimal', 'name': 'Minimal', 'description': 'Ultra-clean simple design'},
            {'id': 'bold', 'name': 'Bold', 'description': 'Strong visual impact design'},
            {'id': 'vintage', 'name': 'Vintage', 'description': 'Retro classic appearance'},
            {'id': 'geometric', 'name': 'Geometric', 'description': 'Modern geometric patterns'},
            {'id': 'gradient', 'name': 'Gradient', 'description': 'Smooth color transitions'},
            {'id': 'executive', 'name': 'Executive', 'description': 'Premium luxury design'}
        ]
    
    @staticmethod
    def get_available_fonts():
        """Return available fonts"""
        return [
            {'id': 'Arial', 'name': 'Arial'},
            {'id': 'Helvetica', 'name': 'Helvetica'},
            {'id': 'Times', 'name': 'Times New Roman'},
            {'id': 'Georgia', 'name': 'Georgia'},
            {'id': 'Verdana', 'name': 'Verdana'},
            {'id': 'Calibri', 'name': 'Calibri'},
            {'id': 'Trebuchet', 'name': 'Trebuchet MS'},
            {'id': 'Tahoma', 'name': 'Tahoma'},
            {'id': 'Impact', 'name': 'Impact'},
            {'id': 'Palatino', 'name': 'Palatino'},
            {'id': 'Garamond', 'name': 'Garamond'},
            {'id': 'Century', 'name': 'Century Gothic'}
        ]
    
    @staticmethod
    def get_available_colors():
        """Return available color schemes"""
        return [
            {'id': 'blue', 'name': 'Blue', 'primary': '#007bff', 'secondary': '#6c757d'},
            {'id': 'red', 'name': 'Red', 'primary': '#dc3545', 'secondary': '#6c757d'},
            {'id': 'green', 'name': 'Green', 'primary': '#28a745', 'secondary': '#6c757d'},
            {'id': 'purple', 'name': 'Purple', 'primary': '#6f42c1', 'secondary': '#6c757d'},
            {'id': 'orange', 'name': 'Orange', 'primary': '#fd7e14', 'secondary': '#6c757d'},
            {'id': 'black', 'name': 'Black', 'primary': '#000000', 'secondary': '#6c757d'},
            {'id': 'teal', 'name': 'Teal', 'primary': '#20c997', 'secondary': '#6c757d'},
            {'id': 'indigo', 'name': 'Indigo', 'primary': '#6610f2', 'secondary': '#6c757d'},
            {'id': 'pink', 'name': 'Pink', 'primary': '#e83e8c', 'secondary': '#6c757d'},
            {'id': 'yellow', 'name': 'Yellow', 'primary': '#ffc107', 'secondary': '#495057'},
            {'id': 'cyan', 'name': 'Cyan', 'primary': '#17a2b8', 'secondary': '#6c757d'},
            {'id': 'brown', 'name': 'Brown', 'primary': '#8d4925', 'secondary': '#6c757d'},
            {'id': 'navy', 'name': 'Navy', 'primary': '#1e3a8a', 'secondary': '#64748b'},
            {'id': 'emerald', 'name': 'Emerald', 'primary': '#059669', 'secondary': '#6b7280'},
            {'id': 'rose', 'name': 'Rose', 'primary': '#e11d48', 'secondary': '#6b7280'},
            {'id': 'amber', 'name': 'Amber', 'primary': '#f59e0b', 'secondary': '#374151'},
            {'id': 'violet', 'name': 'Violet', 'primary': '#8b5cf6', 'secondary': '#6b7280'},
            {'id': 'slate', 'name': 'Slate', 'primary': '#475569', 'secondary': '#94a3b8'}
        ]
    
    def get_color_scheme(self, color_id):
        """Get color scheme by ID"""
        colors = self.get_available_colors()
        for color in colors:
            if color['id'] == color_id:
                return color
        return colors[0]  # Default to blue
    
    def generate_qr_code(self, card_data):
        """Generate QR code with vCard data"""
        try:
            # Create vCard format with social media
            vcard_lines = [
                "BEGIN:VCARD",
                "VERSION:3.0",
                f"FN:{card_data.get('name', '')}",
                f"ORG:{card_data.get('company', '')}",
                f"TITLE:{card_data.get('job_title', '')}",
                f"EMAIL:{card_data.get('email', '')}",
                f"TEL:{card_data.get('phone', '')}",
                f"URL:{card_data.get('website', '')}"
            ]
            
            # Add social media URLs to vCard
            if card_data.get('social_media'):
                for platform, value in card_data['social_media'].items():
                    if value:
                        if platform == 'linkedin' and value.startswith('http'):
                            vcard_lines.append(f"URL:{value}")
                        elif platform == 'twitter':
                            twitter_url = value if value.startswith('http') else f"https://twitter.com/{value.lstrip('@')}"
                            vcard_lines.append(f"URL:{twitter_url}")
                        elif platform == 'instagram':
                            instagram_url = value if value.startswith('http') else f"https://instagram.com/{value.lstrip('@')}"
                            vcard_lines.append(f"URL:{instagram_url}")
                        elif platform == 'github':
                            github_url = value if value.startswith('http') else f"https://github.com/{value}"
                            vcard_lines.append(f"URL:{github_url}")
                        elif platform == 'facebook':
                            facebook_url = value if value.startswith('http') else f"https://facebook.com/{value}"
                            vcard_lines.append(f"URL:{facebook_url}")
                        elif platform == 'tiktok':
                            tiktok_url = value if value.startswith('http') else f"https://tiktok.com/@{value.lstrip('@')}"
                            vcard_lines.append(f"URL:{tiktok_url}")
            
            vcard_lines.extend([
                f"ADR:;;{card_data.get('address', '')};;;;",
                "END:VCARD"
            ])
            
            vcard = '\n'.join(vcard_lines)
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(vcard)
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color="black", back_color="white")
            return qr_img
        except Exception as e:
            logging.error(f"Error generating QR code: {str(e)}")
            return None
    
    def create_card_image(self, card_data, logo_path=None):
        """Create business card image"""
        try:
            # Create blank image
            img = Image.new('RGB', (self.card_width, self.card_height), 'white')
            draw = ImageDraw.Draw(img)
            
            # Get color scheme
            color_scheme = self.get_color_scheme(card_data.get('color', 'blue'))
            primary_color = color_scheme['primary']
            
            # Apply template-specific styling
            template = card_data.get('template', 'modern')
            self._apply_template_styling(draw, img, template, primary_color)
            
            # Load font (fallback to default if not available)
            try:
                font_large = ImageFont.truetype("arial.ttf", 24)
                font_medium = ImageFont.truetype("arial.ttf", 16)
                font_small = ImageFont.truetype("arial.ttf", 12)
            except:
                try:
                    font_large = ImageFont.load_default()
                    font_medium = ImageFont.load_default()
                    font_small = ImageFont.load_default()
                except:
                    font_large = font_medium = font_small = None
            
            # Calculate text positioning
            text_align = card_data.get('text_align', 'left')
            x_offset = 20 if text_align == 'left' else self.card_width // 2
            y_start = 30
            line_height = 25
            
            # Draw text elements
            y_pos = y_start
            
            # Name (largest)
            name = card_data.get('name', '')
            if name and font_large:
                if text_align == 'center':
                    bbox = draw.textbbox((0, 0), name, font=font_large)
                    text_width = bbox[2] - bbox[0]
                    x_pos = (self.card_width - text_width) // 2
                else:
                    x_pos = x_offset
                draw.text((x_pos, y_pos), name, fill=primary_color, font=font_large)
                y_pos += line_height + 5
            
            # Job title
            job_title = card_data.get('job_title', '')
            if job_title and font_medium:
                if text_align == 'center':
                    bbox = draw.textbbox((0, 0), job_title, font=font_medium)
                    text_width = bbox[2] - bbox[0]
                    x_pos = (self.card_width - text_width) // 2
                else:
                    x_pos = x_offset
                draw.text((x_pos, y_pos), job_title, fill='black', font=font_medium)
                y_pos += line_height
            
            # Company
            company = card_data.get('company', '')
            if company and font_medium:
                if text_align == 'center':
                    bbox = draw.textbbox((0, 0), company, font=font_medium)
                    text_width = bbox[2] - bbox[0]
                    x_pos = (self.card_width - text_width) // 2
                else:
                    x_pos = x_offset
                draw.text((x_pos, y_pos), company, fill=color_scheme['secondary'], font=font_medium)
                y_pos += line_height + 10
            
            # Contact information with colorful icons
            contact_info = []
            if card_data.get('email'):
                contact_info.append(f"📧 {card_data['email']}")
            if card_data.get('phone'):
                contact_info.append(f"📱 {card_data['phone']}")
            if card_data.get('website'):
                contact_info.append(f"🌍 {card_data['website']}")
            if card_data.get('address'):
                contact_info.append(f"🏢 {card_data['address']}")
            
            # Social media information
            social_info = []
            social_icons = {
                'linkedin': '🔗',
                'twitter': '🐦',
                'instagram': '📸',
                'github': '🐙',
                'facebook': '👥',
                'tiktok': '🎬'
            }
            
            if card_data.get('social_media'):
                for platform, value in card_data['social_media'].items():
                    if value:
                        icon = social_icons.get(platform, '🔗')
                        if platform == 'linkedin':
                            display_value = value.replace('https://linkedin.com/in/', 'in/').replace('https://www.linkedin.com/in/', 'in/')
                        elif platform in ['twitter', 'instagram', 'tiktok']:
                            display_value = value if value.startswith('@') else f"@{value}"
                        elif platform == 'github':
                            display_value = value.replace('github.com/', '').replace('https://github.com/', '')
                        elif platform == 'facebook':
                            display_value = value.replace('https://facebook.com/', '').replace('https://www.facebook.com/', '')
                        else:
                            display_value = value
                        social_info.append(f"{icon} {display_value}")
            
            # Combine contact and social info
            all_contact_info = contact_info + social_info
            
            for info in all_contact_info:
                if font_small:
                    if text_align == 'center':
                        bbox = draw.textbbox((0, 0), info, font=font_small)
                        text_width = bbox[2] - bbox[0]
                        x_pos = (self.card_width - text_width) // 2
                    else:
                        x_pos = x_offset
                    draw.text((x_pos, y_pos), info, fill='black', font=font_small)
                    y_pos += 18
            
            # Add logo if provided
            if logo_path and os.path.exists(logo_path):
                try:
                    logo = Image.open(logo_path)
                    logo.thumbnail((60, 60), Image.Resampling.LANCZOS)
                    logo_x = self.card_width - logo.width - 20
                    logo_y = 20
                    img.paste(logo, (logo_x, logo_y))
                except Exception as e:
                    logging.error(f"Error adding logo: {str(e)}")
            
            # Add QR code if requested
            if card_data.get('include_qr', False):
                qr_img = self.generate_qr_code(card_data)
                if qr_img:
                    qr_img = qr_img.resize((60, 60), Image.Resampling.LANCZOS)
                    qr_x = self.card_width - 80
                    qr_y = self.card_height - 80
                    img.paste(qr_img, (qr_x, qr_y))
            
            return img
        
        except Exception as e:
            logging.error(f"Error creating card image: {str(e)}")
            raise
    
    def _apply_template_styling(self, draw, img, template, primary_color):
        """Apply template-specific styling"""
        if template == 'modern':
            # Modern: Clean lines and accent border
            draw.rectangle([(0, 0), (self.card_width, 5)], fill=primary_color)
        
        elif template == 'classic':
            # Classic: Simple border
            draw.rectangle([(0, 0), (self.card_width-1, self.card_height-1)], 
                         outline='black', width=2)
        
        elif template == 'creative':
            # Creative: Colorful background gradient effect
            for i in range(self.card_height):
                alpha = int(255 * (1 - i / self.card_height) * 0.1)
                color = self._hex_to_rgb(primary_color) + (alpha,)
                draw.line([(0, i), (self.card_width, i)], fill=color[:3])
        
        elif template == 'elegant':
            # Elegant: Subtle corner decorations
            draw.rectangle([(0, 0), (50, 5)], fill=primary_color)
            draw.rectangle([(self.card_width-50, self.card_height-5), 
                          (self.card_width, self.card_height)], fill=primary_color)
        
        elif template == 'tech':
            # Tech: Geometric patterns
            draw.rectangle([(0, 0), (10, self.card_height)], fill=primary_color)
            for i in range(0, self.card_width, 40):
                draw.line([(i, 0), (i+20, 20)], fill=primary_color, width=1)
        
        elif template == 'corporate':
            # Corporate: Professional double border
            draw.rectangle([(0, 0), (self.card_width-1, self.card_height-1)], 
                         outline=primary_color, width=3)
            draw.rectangle([(5, 5), (self.card_width-6, self.card_height-6)], 
                         outline=primary_color, width=1)
        
        elif template == 'artistic':
            # Artistic: Creative curved lines
            rgb = self._hex_to_rgb(primary_color)
            for i in range(0, self.card_width, 20):
                x = i
                y = int(20 * (1 + 0.5 * (i / self.card_width)))
                draw.ellipse([(x-10, y-10), (x+10, y+10)], outline=rgb, width=2)
        
        elif template == 'minimal':
            # Minimal: Just a subtle line
            draw.line([(20, self.card_height-20), (self.card_width-20, self.card_height-20)], 
                     fill=primary_color, width=1)
        
        elif template == 'bold':
            # Bold: Strong geometric shapes
            draw.rectangle([(0, 0), (30, self.card_height)], fill=primary_color)
            draw.polygon([(30, 0), (60, 0), (30, 30)], fill=primary_color)
        
        elif template == 'vintage':
            # Vintage: Ornate corner elements
            rgb = self._hex_to_rgb(primary_color)
            # Top corners
            for i in range(3):
                draw.rectangle([(10+i*5, 10+i*2), (40-i*5, 12+i*2)], outline=rgb)
                draw.rectangle([(self.card_width-40+i*5, 10+i*2), 
                              (self.card_width-10-i*5, 12+i*2)], outline=rgb)
        
        elif template == 'geometric':
            # Geometric: Modern shapes pattern
            rgb = self._hex_to_rgb(primary_color)
            for i in range(0, self.card_width, 60):
                # Triangles
                draw.polygon([(i, 0), (i+15, 0), (i+7, 15)], fill=rgb)
                # Circles
                draw.ellipse([(i+20, 5), (i+35, 20)], outline=rgb, width=2)
        
        elif template == 'gradient':
            # Gradient: Smooth color transition
            rgb = self._hex_to_rgb(primary_color)
            for i in range(self.card_height):
                opacity = int(255 * (1 - i / self.card_height) * 0.3)
                if opacity > 0:
                    color = tuple(min(255, c + opacity//3) for c in rgb)
                    draw.line([(0, i), (self.card_width, i)], fill=color)
        
        elif template == 'executive':
            # Executive: Luxury gold-style accent
            draw.rectangle([(0, 0), (self.card_width, 8)], fill=primary_color)
            draw.rectangle([(0, self.card_height-8), (self.card_width, self.card_height)], 
                         fill=primary_color)
            # Side accent
            draw.rectangle([(self.card_width-8, 0), (self.card_width, self.card_height)], 
                         fill=primary_color)
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def generate_preview(self, card_data, logo_path=None):
        """Generate preview image"""
        try:
            img = self.create_card_image(card_data, logo_path)
            
            # Save preview
            preview_filename = f"preview_{uuid.uuid4().hex}.png"
            preview_path = os.path.join('static', 'previews')
            os.makedirs(preview_path, exist_ok=True)
            full_path = os.path.join(preview_path, preview_filename)
            
            img.save(full_path, 'PNG')
            return f"/static/previews/{preview_filename}"
        
        except Exception as e:
            logging.error(f"Error generating preview: {str(e)}")
            raise
    
    def generate_png(self, card_data, logo_path=None):
        """Generate PNG export"""
        try:
            img = self.create_card_image(card_data, logo_path)
            
            # High resolution for export
            high_res_img = img.resize((self.card_width * 3, self.card_height * 3), 
                                    Image.Resampling.LANCZOS)
            
            export_filename = f"business_card_{uuid.uuid4().hex}.png"
            export_path = os.path.join('exports', export_filename)
            high_res_img.save(export_path, 'PNG', dpi=(self.dpi, self.dpi))
            
            return export_path
        
        except Exception as e:
            logging.error(f"Error generating PNG: {str(e)}")
            raise
    
    def generate_pdf(self, card_data, logo_path=None):
        """Generate PDF export"""
        try:
            export_filename = f"business_card_{uuid.uuid4().hex}.pdf"
            export_path = os.path.join('exports', export_filename)
            
            c = canvas.Canvas(export_path, pagesize=letter)
            
            # Convert business card dimensions to points (72 points = 1 inch)
            card_width_pt = (self.card_width / 96) * 72  # Assuming 96 DPI
            card_height_pt = (self.card_height / 96) * 72
            
            # Center the card on the page
            page_width, page_height = letter
            x_offset = (page_width - card_width_pt) / 2
            y_offset = (page_height - card_height_pt) / 2
            
            # Draw card background
            c.setFillColor(colors.white)
            c.rect(x_offset, y_offset, card_width_pt, card_height_pt, fill=1)
            
            # Get color scheme
            color_scheme = self.get_color_scheme(card_data.get('color', 'blue'))
            primary_rgb = self._hex_to_rgb(color_scheme['primary'])
            primary_color = colors.Color(primary_rgb[0]/255.0, primary_rgb[1]/255.0, primary_rgb[2]/255.0)
            
            # Draw text
            text_x = x_offset + 20
            text_y = y_offset + card_height_pt - 40
            
            # Name
            if card_data.get('name'):
                c.setFillColor(primary_color)
                c.setFont("Helvetica-Bold", 16)
                c.drawString(text_x, text_y, card_data['name'])
                text_y -= 25
            
            # Job title
            if card_data.get('job_title'):
                c.setFillColor(colors.black)
                c.setFont("Helvetica", 12)
                c.drawString(text_x, text_y, card_data['job_title'])
                text_y -= 20
            
            # Company
            if card_data.get('company'):
                c.setFillColor(colors.grey)
                c.setFont("Helvetica", 12)
                c.drawString(text_x, text_y, card_data['company'])
                text_y -= 25
            
            # Contact info
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 10)
            
            contact_info = []
            if card_data.get('email'):
                contact_info.append(f"Email: {card_data['email']}")
            if card_data.get('phone'):
                contact_info.append(f"Phone: {card_data['phone']}")
            if card_data.get('website'):
                contact_info.append(f"Web: {card_data['website']}")
            if card_data.get('address'):
                contact_info.append(f"Address: {card_data['address']}")
            
            for info in contact_info:
                c.drawString(text_x, text_y, info)
                text_y -= 15
            
            # Add logo if provided
            if logo_path and os.path.exists(logo_path):
                try:
                    from reportlab.lib.utils import ImageReader
                    # Position logo in top right corner
                    logo_x = x_offset + card_width_pt - 60
                    logo_y = y_offset + card_height_pt - 60
                    logo_width = 50
                    logo_height = 50
                    
                    c.drawImage(ImageReader(logo_path), logo_x, logo_y, 
                              width=logo_width, height=logo_height, mask='auto')
                except Exception as e:
                    logging.error(f"Error adding logo to PDF: {str(e)}")
            
            c.save()
            return export_path
        
        except Exception as e:
            logging.error(f"Error generating PDF: {str(e)}")
            raise
    
    def generate_print_pdf(self, card_data, logo_path=None):
        """Generate print-ready PDF with CMYK colors"""
        # For now, use the same PDF generation as above
        # In a production environment, you'd use a library that supports CMYK
        return self.generate_pdf(card_data, logo_path)
    
    def generate_animated_html(self, card_data, logo_path=None):
        """Generate animated HTML business card"""
        try:
            color_scheme = self.get_color_scheme(card_data.get('color', 'blue'))
            
            # Convert logo to base64 if provided
            logo_data_url = ""
            if logo_path and os.path.exists(logo_path):
                try:
                    import base64
                    with open(logo_path, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode('utf-8')
                        file_extension = os.path.splitext(logo_path)[1].lower()
                        mime_type = 'image/png' if file_extension == '.png' else 'image/jpeg'
                        logo_data_url = f"data:{mime_type};base64,{img_data}"
                except Exception as e:
                    logging.error(f"Error converting logo to base64: {str(e)}")
            
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Digital Business Card - {card_data.get('name', 'Business Card')}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        body {{
            margin: 0;
            padding: 20px;
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .business-card {{
            width: 400px;
            height: 240px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            padding: 30px;
            box-sizing: border-box;
            position: relative;
            overflow: hidden;
            animation: cardEntry 1s ease-out;
        }}
        
        .business-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: {color_scheme['primary']};
            animation: slideIn 1.5s ease-out;
        }}
        
        .name {{
            font-size: 24px;
            font-weight: 700;
            color: {color_scheme['primary']};
            margin-bottom: 5px;
            animation: fadeInUp 1s ease-out 0.2s both;
        }}
        
        .job-title {{
            font-size: 16px;
            color: #333;
            margin-bottom: 5px;
            animation: fadeInUp 1s ease-out 0.4s both;
        }}
        
        .company {{
            font-size: 16px;
            color: {color_scheme['secondary']};
            margin-bottom: 20px;
            animation: fadeInUp 1s ease-out 0.6s both;
        }}
        
        .contact-info {{
            font-size: 12px;
            color: #666;
            line-height: 1.6;
            animation: fadeInUp 1s ease-out 0.8s both;
        }}
        
        .contact-info div {{
            margin-bottom: 3px;
        }}
        
        @keyframes cardEntry {{
            from {{
                transform: translateY(50px);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}
        
        @keyframes slideIn {{
            from {{
                transform: translateX(-100%);
            }}
            to {{
                transform: translateX(0);
            }}
        }}
        
        @keyframes fadeInUp {{
            from {{
                transform: translateY(20px);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}
        
        .business-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }}
        
        .logo {{
            position: absolute;
            top: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            border-radius: 8px;
            animation: fadeInUp 1s ease-out 1s both;
        }}
        
        @media (max-width: 480px) {{
            .business-card {{
                width: 90%;
                max-width: 350px;
            }}
            
            .logo {{
                width: 50px;
                height: 50px;
            }}
        }}
    </style>
</head>
<body>
    <div class="business-card">
        {"<img src='" + logo_data_url + "' alt='Company Logo' class='logo'>" if logo_data_url else ""}
        <div class="name">{card_data.get('name', '')}</div>
        <div class="job-title">{card_data.get('job_title', '')}</div>
        <div class="company">{card_data.get('company', '')}</div>
        <div class="contact-info">
"""
            
            if card_data.get('email'):
                html_content += f"            <div>Email: {card_data['email']}</div>\n"
            if card_data.get('phone'):
                html_content += f"            <div>Phone: {card_data['phone']}</div>\n"
            if card_data.get('website'):
                html_content += f"            <div>Web: {card_data['website']}</div>\n"
            if card_data.get('address'):
                html_content += f"            <div>Address: {card_data['address']}</div>\n"
            
            html_content += """        </div>
    </div>
</body>
</html>"""
            
            export_filename = f"business_card_{uuid.uuid4().hex}.html"
            export_path = os.path.join('exports', export_filename)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return export_path
        
        except Exception as e:
            logging.error(f"Error generating HTML: {str(e)}")
            raise
    
    def generate_batch(self, csv_data, template, font, color, export_format):
        """Generate batch business cards from CSV data"""
        try:
            # Create temporary directory for batch files
            with tempfile.TemporaryDirectory() as temp_dir:
                batch_files = []
                
                for i, row in enumerate(csv_data):
                    # Map CSV columns to card data
                    card_data = {
                        'name': row.get('name', row.get('Name', '')),
                        'job_title': row.get('job_title', row.get('Job Title', row.get('title', ''))),
                        'company': row.get('company', row.get('Company', '')),
                        'email': row.get('email', row.get('Email', '')),
                        'phone': row.get('phone', row.get('Phone', '')),
                        'website': row.get('website', row.get('Website', '')),
                        'address': row.get('address', row.get('Address', '')),
                        'template': template,
                        'font': font,
                        'color': color,
                        'include_qr': True
                    }
                    
                    # Generate card based on format
                    if export_format == 'png':
                        file_path = self.generate_png(card_data)
                        new_filename = f"card_{i+1}_{card_data.get('name', 'unknown').replace(' ', '_')}.png"
                    elif export_format == 'pdf':
                        file_path = self.generate_pdf(card_data)
                        new_filename = f"card_{i+1}_{card_data.get('name', 'unknown').replace(' ', '_')}.pdf"
                    elif export_format == 'html':
                        file_path = self.generate_animated_html(card_data)
                        new_filename = f"card_{i+1}_{card_data.get('name', 'unknown').replace(' ', '_')}.html"
                    else:
                        continue
                    
                    # Copy to temp directory with proper name
                    temp_file_path = os.path.join(temp_dir, new_filename)
                    with open(file_path, 'rb') as src, open(temp_file_path, 'wb') as dst:
                        dst.write(src.read())
                    
                    batch_files.append(temp_file_path)
                    
                    # Clean up original file
                    try:
                        os.remove(file_path)
                    except:
                        pass
                
                # Create ZIP file
                zip_filename = f"business_cards_batch_{uuid.uuid4().hex}.zip"
                zip_path = os.path.join('exports', zip_filename)
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in batch_files:
                        zipf.write(file_path, os.path.basename(file_path))
                
                return zip_path
        
        except Exception as e:
            logging.error(f"Error in batch generation: {str(e)}")
            raise
