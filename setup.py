"""
initiation file for the app
this file invoked from setup.py outstide
this represent the corpe/ directory
"""

from flask import Flask
from config import Config



def create_app(config=Config):
    """
    end point of the app
    """
    # Initiate flask object and its config
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    from route import page_not_found
    app.register_error_handler(404, page_not_found)

    # run route from the app context
    with app.app_context():
        # Import routes
        from route import geo_bp
        app.register_blueprint(geo_bp)
        
        return app

app = create_app()
app.run(host='0.0.0.0')