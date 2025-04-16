# routes/__init__.py

from flask import Flask

def register_blueprints(app: Flask):
    # Importa los blueprints desde cada módulo.
    from .auth import auth_bp
    from .patients import patients_bp
    from .doctors import doctors_bp
    from .histories import histories_bp
    from .observations import observations_bp
    from .main import main_bp

    # Registra cada blueprint en la aplicación.
    app.register_blueprint(auth_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(histories_bp)
    app.register_blueprint(observations_bp)
    app.register_blueprint(main_bp)

# También puedes exponer los blueprints individualmente, si deseas.
__all__ = [
    "auth_bp",
    "patients_bp",
    "doctors_bp",
    "histories_bp",
    "observations_bp",
    "main_bp",
    "register_blueprints",
]
