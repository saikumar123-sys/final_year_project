from extensions import db
from flask_login import UserMixin
from datetime import datetime

# ---------------- USER ----------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # admin / industry

    wallet_address = db.Column(db.String(100))
    private_key = db.Column(db.String(200))  # for academic demo only

    emissions = db.relationship('Emission', backref='industry', lazy=True)
    is_approved = db.Column(db.Boolean, default=False)
    is_suspended = db.Column(db.Boolean, default=False)


# ---------------- BASELINE (ADMIN CONTROLLED CAP) ----------------
class Baseline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sector = db.Column(db.String(100), nullable=False)
    gas_type = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    allowed_emission = db.Column(db.Float, nullable=False)


# ---------------- EMISSION REPORT ----------------
class Emission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    year = db.Column(db.Integer, nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    gas_type = db.Column(db.String(50), nullable=False)

    reported_amount = db.Column(db.Float, nullable=False)
    baseline_amount = db.Column(db.Float, nullable=False)

    credits_earned = db.Column(db.Float, default=0)
    penalty = db.Column(db.Float, default=0)
    status = db.Column(db.String(50))  # Approved / Penalty

    blockchain_tx = db.Column(db.String(200))  # mint tx hash
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- MARKET CONFIG (PRICE ENGINE) ----------------
class MarketConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_price = db.Column(db.Float, default=500)
    adjustment_factor = db.Column(db.Float, default=0.5)


# ---------------- MARKET ORDERS ----------------
class MarketOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    amount = db.Column(db.Float, nullable=False)
    price_per_credit = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(50), default='Open')
    approval_status = db.Column(db.String(50), default='Pending')

    tx_hash = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # VERY IMPORTANT PART (THIS FIXES THE ERROR)
    seller = db.relationship('User', foreign_keys=[seller_id], backref='sell_orders')
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='buy_orders')




# ---------------- CREDIT RETIREMENT (OFFSET PROOF) ----------------
class CreditRetirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    credits_retired = db.Column(db.Float)
    tx_hash = db.Column(db.String(200))
    retired_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- EMISSION DOCUMENT UPLOAD ----------------
class EmissionDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(300), nullable=False)
    original_name = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(50), default='PENDING VERIFICATION')  # PENDING VERIFICATION / APPROVED / REJECTED
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)

    industry = db.relationship('User', backref='documents')
