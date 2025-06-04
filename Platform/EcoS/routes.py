from datetime import datetime, timedelta ,timezone
from concurrent.futures import ThreadPoolExecutor
from flask import render_template, redirect, url_for, flash, send_file, request, session, jsonify
from EcoS.forms import LoginForm, MapForm, UpdateAccountForm
from EcoS.entities import User
from EcoS.Sent_hub import evalscripts, get_access_token
from EcoS import app, db, bcrypt , get_locale
from flask_login import login_user, logout_user, login_required, current_user
from PIL import Image
import secrets, os, io, requests, smtplib, uuid, json
from flask_babel import Babel, _,lazy_gettext 
from dotenv import load_dotenv
from sqlalchemy import text, func


executor = ThreadPoolExecutor()



@app.route('/setlang')
def setlang():
    lang = request.args.get('lang', 'en')
    session['lang'] = lang
    return redirect(request.referrer)

@app.context_processor
def inject_babel():
    return dict(_=lazy_gettext)

@app.context_processor
def inject_locale():
    # This makes the function available directly, allowing you to call it in the template
    return {'get_locale': get_locale}


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():

            # # store in session
            # session['full_address'] = address_info['address']
            # session['city'] = address_info['city']
            # session['region'] = address_info['region']
            # session['country'] = address_info['country']
            # session['weather_data']=weather_data
            # session['weather_summary'] = weather_summary
            # session['soil_data']=soil_data
            # session['soil_summary'] = soil_summar

    return render_template('home.html', current_locale=get_locale())


@app.route("/users")
@login_required
def users():
    if current_user.is_authenticated:
        if current_user.privilege == 'admin':
            users = User.query.filter_by(privilege="user").all()
            return render_template('users.html', title=_('Users'), users=users, current_locale=session.get('lang'))
        else:
            flash(_("You Don't have the admin privilege"), 'warning')
            return redirect(url_for('home'))
        
@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(_('User has been deleted successfully'), 'success')
    else:
        flash(_('User not found'), 'danger')
    return redirect(url_for('users'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.mdp, form.mdp.data):
            flash(_("Welcome Back %(username)s!", username=user.username), 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(_('Login Unsuccessful, please check your email and password'), 'danger')
    return render_template('login.html', title=_('Login'), form=form, current_locale=session.get('lang'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # Delete previous picture if it exists
    if current_user.img:
        prev_picture_path = os.path.join(app.root_path, 'static/profile_pics', current_user.img)
        if os.path.exists(prev_picture_path):
            os.remove(prev_picture_path)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(_('Your account has been updated!'), 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for('static', filename='profile_pics/' + current_user.img)
    return render_template('account.html', title=_('Account'), img_file=img_file, form=form, current_locale=session.get('lang'))








@app.route("/dashboard")
@login_required
def dashboard():
    """Main admin dashboard route"""
    if current_user.privilege != 'admin':
        flash(_("You don't have admin privileges"), 'warning')
        return redirect(url_for('home'))
    
    return render_template('dashboard.html', title=_('Admin Dashboard'), current_locale=session.get('lang'))

@app.route("/api/dashboard/stats")
@login_required
def dashboard_stats():
    """API endpoint for dashboard statistics"""
    if current_user.privilege != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Total Active Alerts
        total_alerts = db.session.execute(
            text("SELECT COUNT(*) FROM pollution_alerts WHERE detected_at >= NOW() - INTERVAL '24 hours'")
        ).scalar() or 0
        
        # Average River Pollution Score (NDWI/NDMI aggregate)
        avg_pollution = db.session.execute(
            text("""
                SELECT AVG((ndwi.mean + swir.mean) / 2) as avg_score
                FROM ndwi_data ndwi 
                JOIN swir_data swir ON ndwi.tile_id = swir.tile_id 
                WHERE ndwi.observation_date >= CURRENT_DATE - INTERVAL '7 days'
            """)
        ).scalar() or 0
        
        # Number of Full Dumpsters
        full_dumpsters = db.session.execute(
            text("SELECT COUNT(*) FROM dump_sites WHERE status = 'full'")
        ).scalar() or 0
        
        # Tiles Processed Today
        tiles_today = db.session.execute(
            text("SELECT COUNT(*) FROM tiles WHERE DATE(created_at) = CURRENT_DATE")
        ).scalar() or 0
        
        # Zones with Anomalies
        anomaly_zones = db.session.execute(
            text("""
                SELECT COUNT(DISTINCT tile_id) 
                FROM pollution_alerts 
                WHERE detected_at >= CURRENT_DATE - INTERVAL '7 days'
            """)
        ).scalar() or 0
        
        return jsonify({
            'total_alerts': total_alerts,
            'avg_pollution_score': round(float(avg_pollution), 2) if avg_pollution else 0,
            'full_dumpsters': full_dumpsters,
            'tiles_processed': tiles_today,
            'anomaly_zones': anomaly_zones
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/dashboard/pollution-trends")
@login_required
def pollution_trends():
    """API endpoint for pollution trend data"""
    if current_user.privilege != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get NDWI/NDMI data for the last 30 days
        trends = db.session.execute(
            text("""
                SELECT 
                    DATE(ndwi.observation_date) as date,
                    AVG(ndwi.mean) as ndwi_avg,
                    AVG(swir.mean) as swir_avg,
                    COUNT(*) as measurements
                FROM ndwi_data ndwi
                JOIN swir_data swir ON ndwi.tile_id = swir.tile_id 
                    AND ndwi.observation_date = swir.observation_date
                WHERE ndwi.observation_date >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY DATE(ndwi.observation_date)
                ORDER BY date
            """)
        ).fetchall()
        
        return jsonify([{
            'date': row.date.isoformat(),
            'ndwi': round(float(row.ndwi_avg), 3) if row.ndwi_avg else 0,
            'swir': round(float(row.swir_avg), 3) if row.swir_avg else 0,
            'measurements': row.measurements
        } for row in trends])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/dashboard/dump-sites")
@login_required
def dump_sites_api():
    """API endpoint for dump site data"""
    if current_user.privilege != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        sites = db.session.execute(
            text("""
                SELECT id, name, latitude, longitude, status, description, 
                       updated_at, tile_url
                FROM dump_sites 
                ORDER BY updated_at DESC
            """)
        ).fetchall()
        
        return jsonify([{
            'id': row.id,
            'name': row.name,
            'latitude': row.latitude,
            'longitude': row.longitude,
            'status': row.status,
            'description': row.description,
            'last_updated': row.updated_at.isoformat() if row.updated_at else None,
            'tile_url': row.tile_url
        } for row in sites])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/dashboard/alerts")
@login_required
def alerts_api():
    """API endpoint for pollution alerts"""
    if current_user.privilege != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        severity_filter = request.args.get('severity', '')
        
        query = """
            SELECT pa.id, pa.alert_type, pa.severity, pa.detected_at, 
                   pa.description, pa.triggered_by, t.name as tile_name
            FROM pollution_alerts pa
            JOIN tiles t ON pa.tile_id = t.id
        """
        
        params = {}
        if severity_filter:
            query += " WHERE pa.severity = :severity"
            params['severity'] = severity_filter
            
        query += " ORDER BY pa.detected_at DESC LIMIT :limit OFFSET :offset"
        params['limit'] = per_page
        params['offset'] = (page - 1) * per_page
        
        alerts = db.session.execute(text(query), params).fetchall()
        
        return jsonify([{
            'id': row.id,
            'type': row.alert_type,
            'severity': row.severity,
            'detected_at': row.detected_at.isoformat(),
            'description': row.description,
            'triggered_by': row.triggered_by,
            'tile_name': row.tile_name
        } for row in alerts])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/dashboard/tiles")
@login_required
def tiles_api():
    """API endpoint for tile data with imagery URLs"""
    if current_user.privilege != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        tiles = db.session.execute(
            text("""
                SELECT id, name, description , tile_url, updated_at, created_at
                FROM dump_sites 
                ORDER BY updated_at DESC
                LIMIT 50
            """)
        ).fetchall()
        
        return jsonify([{
            'id': row.id,
            'name': row.name,
            'description': row.description,
            'tile_url': row.tile_url,
            'updated_at': row.updated_at,
            'created_at': row.created_at.isoformat()
        } for row in tiles])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/dashboard/update-dump-status", methods=['POST'])
@login_required
def update_dump_status():
    """API endpoint to update dump site status"""
    if current_user.privilege != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        site_id = data.get('site_id')
        new_status = data.get('status')
        
        if new_status not in ['full', 'empty']:
            return jsonify({'error': 'Invalid status'}), 400
            
        db.session.execute(
            text("UPDATE dump_sites SET status = :status, updated_at = NOW() WHERE id = :id"),
            {'status': new_status, 'id': site_id}
        )
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route("/api/dashboard/alerts-summary")
@login_required
def alerts_summary_api():
    if current_user.privilege != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        counts = db.session.execute(text("""
            SELECT severity, COUNT(*) 
            FROM pollution_alerts 
            GROUP BY severity
        """)).fetchall()

        summary = {'Low': 0, 'Medium': 0, 'High': 0}
        for severity, count in counts:
            summary[severity] = count

        return jsonify({
            'low': summary['Low'],
            'medium': summary['Medium'],
            'high': summary['High']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Always use last 10 days
to_date = datetime.now(timezone.utc)
from_date = to_date - timedelta(days=30)

# Format to Sentinel Hub's expected format
formatted_from = from_date.strftime("%Y-%m-%dT%H:%M:%SZ")
formatted_to = to_date.strftime("%Y-%m-%dT%H:%M:%SZ")

@app.route("/api/dashboard/river-layer-url")
@login_required
def river_layer_url():
    try:
        layer = request.args.get('layer', 'true_color')
        print("Requested layer:", layer)

        evalscript = evalscripts.get(layer)
        if not evalscript:
            print("❌ Invalid evalscript for:", layer)
            return jsonify({"error": "Invalid layer"}), 400

        token = get_access_token()
        if not token:
            print("❌ Access token retrieval failed")
            return jsonify({"error": "Token failure"}), 500

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        min_lat = float(request.args.get('minLat'))
        min_lon = float(request.args.get('minLon'))
        max_lat = float(request.args.get('maxLat'))
        max_lon = float(request.args.get('maxLon'))

        payload = {
            "input": {
                "bounds": {
                    "bbox": [min_lon, min_lat, max_lon, max_lat],
                    "properties": {
                        "crs": "http://www.opengis.net/def/crs/EPSG/0/4326"
                    }
                },
                "data": [{
                    "type": "S2L2A",
                    "dataFilter": {
                        "timeRange": {
                                "from": formatted_from,
                                "to": formatted_to
                        }
                    }
                }]
            },
            "output": {
                "width": 512,
                "height": 512
            },
            "evalscript": evalscript
        }

        response = requests.post("https://services.sentinel-hub.com/api/v1/process", headers=headers, json=payload)

        print("🌐 API status code:", response.status_code)
        if not response.ok:
            print("❌ Sentinel Hub error:", response.text)
            return jsonify({
                "error": "Sentinel Hub returned error",
                "detail": response.text
            }), response.status_code

        return send_file(io.BytesIO(response.content), mimetype='image/png')

    except Exception as e:
        print("❌ Exception:", str(e))
        return jsonify({"error": "Unexpected error", "detail": str(e)}), 500