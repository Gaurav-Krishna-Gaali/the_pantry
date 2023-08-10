# admin.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
# from app import db
# from app import Products, Category

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
