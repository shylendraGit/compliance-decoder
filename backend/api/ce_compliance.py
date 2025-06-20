# 4. Create a new API endpoint for CE-specific features
# Create: api/ce_compliance.py

from flask import Blueprint, request, jsonify
from utils.ce_analyzer import CEAnalyzer

ce_bp = Blueprint('ce_compliance', __name__)

@ce_bp.route('/api/ce/document-types', methods=['GET'])
def get_document_types():
    """Get available CE document types"""
    document_types = {
        'technical_file': 'Technical File',
        'declaration_of_conformity': 'Declaration of Conformity',
        'test_reports': 'Test Reports & Certificates',
        'risk_assessment': 'Risk Assessment',
        'user_manual': 'User Manual'
    }
    return jsonify(document_types)

@ce_bp.route('/api/ce/product-categories', methods=['GET'])
def get_product_categories():
    """Get available product categories"""
    categories = {
        'electronics': 'Electronics & Electrical',
        'machinery': 'Machinery & Equipment',
        'toys': 'Toys & Children Products',
        'medical_devices': 'Medical Devices',
        'radio_equipment': 'Radio & Telecom Equipment',
        'ppe': 'Personal Protective Equipment',
        'cosmetics': 'Cosmetics & Beauty Products'
    }
    return jsonify(categories)

@ce_bp.route('/api/ce/directives/<product_category>', methods=['GET'])
def get_applicable_directives(product_category):
    """Get applicable EU directives for a product category"""
    analyzer = CEAnalyzer()
    directives = analyzer.directive_mapping.get(product_category, [])
    return jsonify({
        'product_category': product_category,
        'applicable_directives': directives
    })

@ce_bp.route('/api/ce/compliance-checklist/<document_type>', methods=['GET'])
def get_compliance_checklist(document_type):
    """Get compliance checklist for document type"""
    checklists = {
        'technical_file': [
            'Manufacturer identification and address',
            'Product description and intended use',
            'Design drawings and specifications',
            'Applicable EU directives listed',
            'Essential requirements analysis',
            'Risk assessment documentation',
            'Test reports from accredited bodies',
            'Declaration of Conformity reference',
            'User instructions included'
        ],
        'declaration_of_conformity': [
            'Manufacturer name and address',
            'Product identification details',
            'Sole responsibility statement',
            'Applicable EU legislation cited',
            'Essential requirements compliance',
            'Conformity assessment procedures',
            'Notified body details (if required)',
            'Place and date of issue',
            'Authorized signature present'
        ]
        # Add more checklists as needed
    }
    
    checklist = checklists.get(document_type, [])
    return jsonify({
        'document_type': document_type,
        'checklist_items': checklist
    })
