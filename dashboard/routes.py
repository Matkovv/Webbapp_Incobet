from flask import Blueprint, render_template

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def show_dashboard():
    # Cały kod w funkcji musi być odpowiednio wcięty
    return render_template('dashboard.html')
