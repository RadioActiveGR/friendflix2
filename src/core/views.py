from flask import Blueprint, render_template
from src.accounts.models import Event, User
from sqlalchemy import desc
import copy
from flask_login import login_required, current_user

core_bp = Blueprint("core", __name__)


@core_bp.route("/")
@login_required
def home():
    user = current_user.id
    events = Event.query.filter_by(creator_id=user).order_by(desc('id')).all()

    return render_template("core/index.html", events=events)
