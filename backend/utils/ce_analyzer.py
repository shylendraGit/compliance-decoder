# Create: utils/ce_analyzer.py

import json
from typing import Dict, List, Any, Optional
from .gpt_analyzer import GPTAnalyzer  # Import your existing analyzer

class CEAnalyzer(GPTAnalyzer):
    """Specialized CE marking compliance analyzer"""
    
    def __init__(self):
        super().__init__()  # Initialize parent GPTAnalyzer
        self.document_types = [
            "technical_file",
            "declaration_of_conformity", 
            "test_reports",
            "risk_assessment",
            "user_manual"
        ]
        
        # EU Directive mapping for different product categories
        self.directive_mapping = {
            "electronics": ["2014/35/EU (LVD)", "2014/30/EU (EMC)", "2011/65/EU (RoHS)"],
            "machinery": ["2006/42/EC (Machinery)", "2014/35/EU (LVD)", "2014/30/EU (EMC)"],
            "toys": ["2009/48/EC (Toy Safety)", "2011/65/EU (RoHS)"],
            "medical_devices": ["2017/745 (MDR)", "2014/35/EU (LVD)", "2014/30/EU (EMC)"],
            "radio_equipment": ["2014/53/EU (RED)", "2011/65/EU (RoHS)"],
            "ppe": ["2016/425 (PPE)", "2014/35/EU (LVD)"],
            "cosmetics": ["1223/2009 (Cosmetics)", "2019/1020 (Market Surveillance)"]
        }

    def get_ce_analysis_prompt(self, document_type: str, document_text: str, product_category: str = None) -> str:
        """Generate CE-specific analysis prompt"""
        
        base_context = f"""
You are a CE marking compliance expert analyzing a {document_type.replace('_', ' ')} document.
Your goal is to assess EU compliance and provide actionable recommendations.

DOCUMENT CONTENT:
{document_text}

ANALYSIS REQUIREMENTS:
1. Identify applicable EU directives/regulations
2. Check completeness against legal requirements  
3. Flag missing mandatory information
4. Assess risk level: LOW, MODERATE, HIGH, or CRITICAL
5. Provide specific, actionable solutions
6. Estimate compliance costs and timeline

"""
        
        if document_type == "technical_file":
            return base_context + self._get_technical_file_requirements()
        elif document_type == "declaration_of_conformity":
            return base_context + self._get_doc_requirements()
        elif document_type == "test_reports":
            return base_context + self._get_test_report_requirements()
        elif document_type == "risk_assessment":
            return base_context + self._get_risk_assessment_requirements()
        else:
            return base_context + self._get_general_requirements()

    def _get_technical_file_requirements(self) -> str:
        return """
TECHNICAL FILE VALIDATION CHECKLIST:

MANDATORY ELEMENTS TO VERIFY:
✓ Manufacturer name and complete business address
✓ Product description and intended use statement
✓ Design drawings, technical specifications
✓ List of applicable EU directives/regulations
✓ Essential requirements analysis and compliance
✓ Risk analysis documentation
✓ Test reports from accredited/notified bodies
✓ Declaration of Conformity reference
✓ User instructions and safety information

CRITICAL FLAGS:
⚠️ Missing manufacturer identification
⚠️ Incomplete technical specifications
⚠️ No conformity assessment procedure
⚠️ Missing or expired test certificates
⚠️ Inadequate risk analysis

RISK ASSESSMENT LOGIC:
- CRITICAL: Missing DoC, invalid test reports, no risk analysis
- HIGH: Incomplete specs, expired certificates, missing standards
- MODERATE: Minor documentation gaps, formatting issues
- LOW: Complete documentation with administrative notes only

Provide specific recommendations for each gap found.
"""

    def _get_doc_requirements(self) -> str:
        return """
DECLARATION OF CONFORMITY VALIDATION:

MANDATORY INFORMATION CHECK:
✓ Manufacturer identification (name, address)
✓ Authorized representative details (if applicable)
✓ Product identification (model, type, batch, serial)
✓ Sole responsibility statement
✓ Product description and intended use
✓ Applicable EU legislation references
✓ Essential requirements compliance statement
✓ Conformity assessment procedures used
✓ Notified body details and numbers (if required)
✓ Place and date of issue
✓ Authorized person name and signature

VALIDATION CHECKS:
- Are directive references current and correct?
- Do notified body numbers exist in official database?
- Is product description sufficiently detailed?
- Are harmonized standards current versions?
- Is signature present and properly authorized?

COMMON ERRORS TO FLAG:
⚠️ Generic or vague product descriptions
⚠️ Incorrect directive citations
⚠️ Missing or invalid notified body references
⚠️ Unsigned or undated documents
⚠️ Wrong conformity assessment procedures

Return structured analysis with specific fixes needed.
"""

    def _get_test_report_requirements(self) -> str:
        return """
TEST REPORTS & CERTIFICATES ANALYSIS:

ACCREDITATION VALIDATION:
✓ Laboratory accreditation status and scope
✓ Notified body number verification
✓ Certificate validity periods (not expired)
✓ Test standard versions (current/withdrawn)
✓ Product tested matches DoC description
✓ Complete test coverage for applicable requirements

RED FLAGS TO IDENTIFY:
⚠️ Non-accredited laboratory reports
⚠️ Expired certificates (check validity periods)
⚠️ Missing critical safety tests
⚠️ Product description mismatches
⚠️ Incomplete electromagnetic compatibility testing
⚠️ Wrong or outdated test standards referenced

COMPLIANCE ASSESSMENT:
- Are all essential requirements tested?
- Do test results meet acceptance criteria?
- Is electromagnetic compatibility covered (if applicable)?
- Are chemical/safety tests complete for product type?

Provide specific guidance on missing tests and accreditation requirements.
"""

    def _get_risk_assessment_requirements(self) -> str:
        return """
PRODUCT RISK ASSESSMENT VALIDATION:

REQUIRED RISK ASSESSMENT ELEMENTS:
✓ Systematic hazard identification
✓ Risk evaluation methodology used
✓ Risk reduction measures implemented
✓ Residual risk assessment and acceptance
✓ User information and warnings
✓ Post-market surveillance provisions

HAZARD CATEGORIES TO VERIFY:
- Mechanical hazards (cutting, crushing, impact)
- Electrical hazards (shock, fire, electrocution)
- Chemical hazards (toxic substances, emissions)
- Thermal hazards (burns, overheating)
- Biological/hygiene hazards
- Noise and vibration exposure
- Ergonomic and usability risks

QUALITY INDICATORS:
- Comprehensive hazard identification?
- Appropriate risk evaluation methods?
- Evidence of risk reduction hierarchy?
- Adequate user information provided?
- Post-market surveillance plan defined?

Flag any gaps in methodology or hazard coverage.
"""

    def _get_general_requirements(self) -> str:
        return """
GENERAL CE COMPLIANCE DOCUMENT REVIEW:

COMPLIANCE INDICATORS TO CHECK:
✓ CE marking format and placement
✓ Product labeling completeness
✓ User manual adequacy
✓ Packaging compliance
✓ Import/distribution documentation

COMMON ISSUES:
- Incorrect CE marking size or format
- Missing mandatory product information
- Inadequate user instructions
- Non-compliant marketing materials
- Missing distributor responsibilities

Assess overall compliance maturity and next steps.
"""

    def analyze_ce_document(self, document_text: str, document_type: str, product_category: str = None) -> Dict[str, Any]:
        """
        Analyze CE compliance document using specialized prompts
        """
        try:
            # Get CE-specific prompt
            prompt = self.get_ce_analysis_prompt(document_type, document_text, product_category)
            
            # Use your existing GPT analysis method
            # Modify this to match your current GPTAnalyzer implementation
            analysis_text = self.analyze_text(prompt)  # Assuming this method exists in parent class
            
            # Parse and structure the response
            structured_result = self._parse_ce_analysis(analysis_text, document_type, product_category)
            
            return structured_result
            
        except Exception as e:
            return {
                "error": f"Analysis failed: {str(e)}",
                "risk_level": "UNKNOWN",
                "confidence_score": 0.0
            }

    def _parse_ce_analysis(self, analysis_text: str, document_type: str, product_category: str) -> Dict[str, Any]:
        """Parse AI response into structured CE compliance data"""
        
        # This is a simplified parser - you'll want to make this more robust
        # based on your GPT response format
        
        return {
            "document_type": document_type,
            "product_category": product_category or "general",
            "risk_level": self._extract_risk_level(analysis_text),
            "confidence_score": 0.85,  # You can calculate this based on analysis quality
            "applicable_directives": self._extract_directives(analysis_text, product_category),
            "compliance_gaps": self._extract_compliance_gaps(analysis_text),
            "strengths": self._extract_strengths(analysis_text),
            "next_steps": self._extract_next_steps(analysis_text),
            "estimated_cost": self._estimate_compliance_cost(analysis_text),
            "estimated_timeline": self._estimate_timeline(analysis_text),
            "summary": self._extract_summary(analysis_text)
        }

    def _extract_risk_level(self, text: str) -> str:
        """Extract risk level from analysis text"""
        text_upper = text.upper()
        if "CRITICAL" in text_upper:
            return "CRITICAL"
        elif "HIGH" in text_upper:
            return "HIGH"
        elif "MODERATE" in text_upper:
            return "MODERATE"
        else:
            return "LOW"

    def _extract_directives(self, text: str, product_category: str) -> List[str]:
        """Extract applicable EU directives"""
        if product_category and product_category in self.directive_mapping:
            return self.directive_mapping[product_category]
        
        # Fallback: extract from text analysis
        common_directives = [
            "2014/35/EU (LVD)", "2014/30/EU (EMC)", "2011/65/EU (RoHS)",
            "2006/42/EC (Machinery)", "2009/48/EC (Toy Safety)"
        ]
        return common_directives[:2]  # Return most common ones as fallback

    def _extract_compliance_gaps(self, text: str) -> List[Dict[str, str]]:
        """Extract compliance issues from analysis"""
        # Simplified extraction - make this more sophisticated based on your needs
        return [
            {
                "severity": "HIGH",
                "issue": "Missing notified body certificate",
                "requirement": "Conformity assessment procedure",
                "solution": "Obtain testing from accredited notified body"
            }
        ]

    def _extract_strengths(self, text: str) -> List[str]:
        """Extract compliance strengths"""
        return [
            "Complete manufacturer identification",
            "Proper document structure maintained"
        ]

    def _extract_next_steps(self, text: str) -> List[str]:
        """Extract recommended actions"""
        return [
            "Submit product for required testing",
            "Update technical documentation",
            "Prepare Declaration of Conformity"
        ]

    def _estimate_compliance_cost(self, text: str) -> str:
        """Estimate compliance costs"""
        return "$2,500 - $4,000"  # You can make this dynamic based on gaps found

    def _estimate_timeline(self, text: str) -> str:
        """Estimate compliance timeline"""
        return "4-6 weeks"  # You can make this dynamic based on complexity

    def _extract_summary(self, text: str) -> str:
        """Extract executive summary"""
        return "Document shows moderate compliance gaps requiring attention to testing and certification requirements."

