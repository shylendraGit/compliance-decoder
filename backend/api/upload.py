# 2. Now let's modify your existing upload.py to handle CE documents
# Modify: api/upload.py

from flask import Blueprint, request, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from utils.pdf_parser import PDFParser
from utils.ce_analyzer import CEAnalyzer  # Import our new CE analyzer

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        document_type = request.form.get('document_type', 'general')  # New parameter
        product_category = request.form.get('product_category', None)  # New parameter
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            file_id = str(uuid.uuid4())
            filename = f"{file_id}.pdf"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Save file
            file.save(filepath)
            
            # Parse PDF
            pdf_parser = PDFParser()
            text_content = pdf_parser.extract_text(filepath)
            
            # Analyze with CE-specific analyzer
            if document_type in ['technical_file', 'declaration_of_conformity', 'test_reports', 'risk_assessment', 'user_manual']:
                ce_analyzer = CEAnalyzer()
                analysis_result = ce_analyzer.analyze_ce_document(
                    text_content, 
                    document_type, 
                    product_category
                )
            else:
                # Fallback to your original analyzer for non-CE documents
                from utils.gpt_analyzer import GPTAnalyzer
                analyzer = GPTAnalyzer()
                analysis_result = analyzer.analyze(text_content)  # Your original method
            
            return jsonify({
                'file_id': file_id,
                'filename': secure_filename(file.filename),
                'analysis': analysis_result,
                'document_type': document_type,
                'product_category': product_category
            }), 200
            
        return jsonify({'error': 'Invalid file type'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500