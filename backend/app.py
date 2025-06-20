from flask import Flask, request, jsonify
from api.upload import upload_blueprint
from config import load_config
from flask_cors import CORS
import re
from api.ce_compliance import ce_bp

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins="*")
    load_config(app)

    # Log all requests during development
    @app.before_request
    def log_request():
        if app.debug:
            print(f"Request: {request.method} {request.path}")
            if request.args:
                print(f"Args: {dict(request.args)}")
            print("---")

    # Register your API blueprint (e.g., /api/upload_certificate)
    app.register_blueprint(upload_blueprint, url_prefix='/api')
    app.register_blueprint(ce_bp)

    @app.route("/health")
    def health_check():
        return jsonify({"status": "healthy", "service": "Compliance Decoder API"})

    @app.route("/iframe")
    def iframe_test():
        shop = request.args.get("shop", "test-shop")
        from flask import make_response

        html = f'''
        <html>
            <head><title>Iframe Test</title></head>
            <body style="font-family: Arial; padding: 2rem;">
                <h2>✅ Iframe Embedding Successful!</h2>
                <p>Shop: {shop}</p>
            </body>
        </html>
        '''

        resp = make_response(html)
        resp.headers["X-Frame-Options"] = "ALLOWALL"
        resp.headers["Content-Security-Policy"] = "frame-ancestors *"
        return resp

    @app.after_request
    def set_iframe_headers(response):
        response.headers["X-Frame-Options"] = "ALLOWALL"
        if request.headers.get('Sec-Fetch-Dest') != 'iframe':
            response.headers["Content-Security-Policy"] = "frame-ancestors *"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    def is_valid_shopify_shop(shop):
        pattern = r'^[a-zA-Z0-9\-]+\.myshopify\.com$'
        return bool(re.match(pattern, shop))

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app

app = create_app()

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host="0.0.0.0", port=port)
