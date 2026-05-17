# ================================
# Auteur  : TIENDREBEOGO Sakinatou
# Rôle    : Authentification et sécurité
# Module  : auth.py
# Projet  : Modélisation Thermodynamique PIC
# ================================

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()

class Utilisateur(UserMixin, db.Model):
    """Modèle de la table utilisateurs."""
    id          = db.Column(db.Integer, primary_key=True)
    nom         = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(150), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(200), nullable=False)
    calculs     = db.relationship('Calcul', backref='utilisateur', lazy=True)

    def set_password(self, mdp):
        """Hache le mot de passe avant de le stocker."""
        self.mot_de_passe = generate_password_hash(mdp)

    def check_password(self, mdp):
        """Vérifie le mot de passe."""
        return check_password_hash(self.mot_de_passe, mdp)


class Calcul(db.Model):
    """Modèle de la table historique des calculs."""
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    gaz         = db.Column(db.String(50))
    temperature = db.Column(db.Float)
    pression    = db.Column(db.Float)
    quantite    = db.Column(db.Float)
    V_parfait   = db.Column(db.Float)
    V_vdw       = db.Column(db.Float)
    ecart       = db.Column(db.Float)
    date        = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))