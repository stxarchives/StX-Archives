import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from supabase import create_client, Client
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key-change-in-production")

url: str = os.getenv("SUPABASE_URL", "")
key: str = os.getenv("SUPABASE_KEY", "")

# Initialize Supabase only if credentials are provided
supabase: Client = None
if url and key:
    supabase = create_client(url, key)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please log in as admin to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def check_maintenance():
    if os.path.exists('.maintenance'):
        # Allow access to static files and admin routes
        if request.path.startswith('/static') or request.path.startswith('/admin'):
            return
        # Display maintenance page for everything else
        return render_template('maintenance.html'), 503

@app.route('/')
def index():
    categories = [
        "Facilities & Infrastructure",
        "Academic Policies",
        "Fee Discrepancies",
        "Staff Conduct",
        "Other Incident"
    ]
    category_counts = {c: 0 for c in categories}
    
    if supabase:
        try:
            response = supabase.table('experiences').select('category').execute()
            for row in response.data:
                cat = row.get('category')
                if cat in category_counts:
                    category_counts[cat] += 1
        except Exception as e:
            print(f"Supabase error: {e}")
    else:
        for exp in mock_experiences:
            cat = exp.get('category')
            if cat in category_counts:
                category_counts[cat] += 1
                
    return render_template('index.html', category_counts=category_counts)

@app.route('/timeline')
def timeline():
    # Example logic: events = supabase.table('timeline').select('*').execute().data
    events = [] 
    return render_template('timeline.html', events=events)

@app.route('/archive')
def archive():
    evidence_list = []
    if supabase:
        try:
            response = supabase.table('evidence').select('*').order('id', desc=True).execute()
            evidence_list = response.data
        except Exception as e:
            print(f"Supabase error fetching evidence: {e}")
            
    return render_template('archive.html', evidence=evidence_list)

@app.route('/document')
def document():
    return render_template('document.html')

# Mock database for local testing if Supabase isn't connected yet
mock_experiences = [
    {
        "id": 1,
        "name": "Anonymous",
        "category": "Fee Discrepancies",
        "date": "2026-07-10",
        "title": "Book Prices Are Insane & Photo Double-Charging",
        "details": "I went to buy the required books and they are priced like gold. To make it worse, they charged ₹510 for a diary, a useless portfolio, and 3 passport size photos. But then, they had the nerve to ask us for another ₹30 for those exact same 3 photographs again!",
        "is_verified": True,
        "is_anonymous": True
    },
    {
        "id": 2,
        "name": "Anonymous",
        "category": "Facilities & Infrastructure",
        "date": "2026-07-08",
        "title": "Paying to become a laborer",
        "details": "They took ₹630 from me to become a student council member. My duties? Moving benches and doing chores for the school administration. It's paid child labor.",
        "is_verified": False,
        "is_anonymous": True
    },
    {
        "id": 3,
        "name": "Anonymous",
        "category": "Facilities & Infrastructure",
        "date": "2026-07-13",
        "title": "Broken Infrastructure Everywhere",
        "details": "The school is falling apart. There are broken washrooms, broken windows in almost every single classroom, damaged benches, and the drinking water quality is extremely bad.",
        "is_verified": True,
        "is_anonymous": True
    },
    {
        "id": 4,
        "name": "Anonymous",
        "category": "Policies & Rules",
        "date": "2026-07-12",
        "title": "Forced Religious Practices & Discrimination",
        "details": "The school administrators are forcing students to sing and dance to Christian songs, practically forcing a change of religion. Additionally, there is blatant religious discrimination regarding holidays; they give holidays for Muslim and Christian celebrations but deny them for Hindu celebrations, such as refusing to give a holiday on Hanuman Jayanti.",
        "is_verified": True,
        "is_anonymous": True
    },
    {
        "id": 5,
        "name": "Anonymous",
        "category": "Fee Discrepancies",
        "date": "2026-07-11",
        "title": "Extortion for Farewell & Books",
        "details": "They collect farewell contributions from all students from Class 9 to Class 12, taking over ₹1500+ and increasing the price as the class level gets higher. Despite this massive collection, they then forced students to dance at the farewell themselves, and the food provided was of terrible quality. Why take so much money if the students have to do everything themselves? Furthermore, the required Physical Education book is still not available in the school.",
        "is_verified": True,
        "is_anonymous": True
    },
    {
        "id": 6,
        "name": "Anonymous",
        "category": "Facilities & Infrastructure",
        "date": "2026-07-09",
        "title": "Unhealthy Canteen Food",
        "details": "Despite being a school that should promote health, the canteen itself sells unhealthy junk food to students.",
        "is_verified": True,
        "is_anonymous": True
    }
]

mock_users = []


@app.route('/experience', methods=['GET', 'POST'])
def experience():
    if request.method == 'POST':
        if 'user_logged_in' not in session:
            flash('You must be logged in to post an experience.', 'error')
            return redirect(url_for('login'))
        
        if not session.get('email_verified'):
            flash('You must verify your email address before posting.', 'error')
            return redirect(url_for('experience'))
            
        # Get form data
        name = request.form.get('name', 'Anonymous')
        email = request.form.get('email', '')
        is_anonymous = request.form.get('is_anonymous') == 'on'
        category = request.form.get('category')
        date = request.form.get('date')
        title = request.form.get('title')
        details = request.form.get('details')
        
        new_exp = {
            "name": name if name else "Anonymous",
            "email": email,
            "is_anonymous": is_anonymous,
            "category": category,
            "date": date,
            "title": title,
            "details": details,
            "is_verified": False
        }
        
        if supabase:
            try:
                supabase.table('experiences').insert(new_exp).execute()
                flash('Your experience has been submitted and is pending verification.', 'success')
            except Exception as e:
                flash(f'Error submitting: {str(e)}', 'error')
        else:
            # Fallback to mock data for local testing
            new_exp["id"] = len(mock_experiences) + 1
            mock_experiences.insert(0, new_exp)
            flash('Your experience has been submitted (saved to local mock DB pending Supabase setup).', 'success')
            
        return redirect(url_for('experience'))

    # GET request - fetch experiences
    experiences = []
    category_filter = request.args.get('category')
    
    if supabase:
        try:
            query = supabase.table('experiences').select('*')
            if category_filter:
                query = query.eq('category', category_filter)
            response = query.order('id', desc=True).execute()
            experiences = response.data
            
            # Process timestamps for rendering
            from datetime import datetime, timezone
            for exp in experiences:
                if exp.get('created_at'):
                    try:
                        # Parse ISO string
                        dt = datetime.fromisoformat(exp['created_at'].replace('Z', '+00:00'))
                        now = datetime.now(timezone.utc)
                        diff = now - dt
                        exp['can_edit'] = diff.total_seconds() <= 900 # 15 minutes
                    except:
                        exp['can_edit'] = False
                else:
                    exp['can_edit'] = False
        except Exception as e:
            print(f"Supabase error: {e}")
            experiences = mock_experiences
    else:
        if category_filter:
            experiences = [e for e in mock_experiences if e.get('category') == category_filter]
        else:
            experiences = mock_experiences

    return render_template('experience.html', experiences=experiences, current_category=category_filter)

@app.route('/edit_experience/<int:exp_id>', methods=['POST'])
def edit_experience(exp_id):
    if 'user_logged_in' not in session:
        flash('You must be logged in.', 'error')
        return redirect(url_for('login'))
        
    details = request.form.get('details')
    user_email = session.get('user_email')
    
    if supabase:
        try:
            # Fetch current experience
            response = supabase.table('experiences').select('*').eq('id', exp_id).execute()
            if not response.data:
                flash('Experience not found.', 'error')
                return redirect(url_for('experience'))
                
            exp = response.data[0]
            
            if exp.get('email') != user_email:
                flash('You can only edit your own posts.', 'error')
                return redirect(url_for('experience'))
                
            from datetime import datetime, timezone
            if exp.get('created_at'):
                dt = datetime.fromisoformat(exp['created_at'].replace('Z', '+00:00'))
                now = datetime.now(timezone.utc)
                diff = now - dt
                if diff.total_seconds() > 900:
                    flash('You can only edit posts within 15 minutes of posting.', 'error')
                    return redirect(url_for('experience'))
            
            edit_count = exp.get('edit_count', 0) or 0
            
            now_iso = datetime.now(timezone.utc).isoformat()
            
            supabase.table('experiences').update({
                'details': details,
                'edit_count': edit_count + 1,
                'last_edited_at': now_iso
            }).eq('id', exp_id).execute()
            
            flash('Experience updated successfully.', 'success')
        except Exception as e:
            flash(f'Error updating experience: {str(e)}', 'error')
            
    return redirect(url_for('experience'))

@app.route('/policies')
def policies():
    return render_template('policies.html')

@app.route('/principals-note')
def principals_note():
    return render_template('principals_note.html')



@app.route('/hall-of-shame')
def hall_of_shame():
    return render_template('hall_of_shame.html')

@app.route('/fee-scam')
def fee_scam():
    return render_template('fee_scam.html')

@app.route('/vip-treatment')
def vip_treatment():
    return render_template('vip_treatment.html')

@app.route('/admin')
@admin_required
def admin():
    experiences = []
    evidence_list = []
    incidents_list = []
    
    analytics = {
        "total": 0,
        "verified": 0,
        "pending": 0,
        "maintenance": os.path.exists('.maintenance')
    }
    
    if supabase:
        try:
            response = supabase.table('experiences').select('*').order('id', desc=True).execute()
            experiences = response.data
            
            ev_response = supabase.table('evidence').select('*').order('id', desc=True).execute()
            evidence_list = ev_response.data
            
            inc_response = supabase.table('incidents').select('*').order('id', desc=False).execute()
            incidents_list = inc_response.data
            
            analytics['total'] = len(experiences)
            analytics['verified'] = sum(1 for e in experiences if e.get('is_verified'))
            analytics['pending'] = analytics['total'] - analytics['verified']
        except Exception as e:
            print(f"Supabase error: {e}")
            experiences = mock_experiences
    else:
        experiences = mock_experiences
        analytics['total'] = len(experiences)
        analytics['verified'] = sum(1 for e in experiences if e.get('is_verified'))
        analytics['pending'] = analytics['total'] - analytics['verified']
        
    return render_template('admin.html', experiences=experiences, evidence=evidence_list, incidents=incidents_list, analytics=analytics)

@app.route('/admin/verify/<int:exp_id>', methods=['POST'])
@admin_required
def verify_experience(exp_id):
    if supabase:
        try:
            # Get current status to toggle
            current = supabase.table('experiences').select('is_verified').eq('id', exp_id).execute().data[0]
            new_status = not current['is_verified']
            supabase.table('experiences').update({'is_verified': new_status}).eq('id', exp_id).execute()
            flash('Experience verification status updated.', 'success')
        except Exception as e:
            flash(f'Error updating status: {str(e)}', 'error')
    else:
        for exp in mock_experiences:
            if exp['id'] == exp_id:
                exp['is_verified'] = not exp['is_verified']
                flash('Status updated (local mock data).', 'success')
                break
                
    return redirect(url_for('admin'))

@app.route('/admin/delete_experience/<int:exp_id>', methods=['POST'])
@admin_required
def delete_experience(exp_id):
    if supabase:
        try:
            supabase.table('experiences').delete().eq('id', exp_id).execute()
            flash('Experience deleted successfully.', 'success')
        except Exception as e:
            flash(f'Error deleting experience: {str(e)}', 'error')
    else:
        global mock_experiences
        mock_experiences = [exp for exp in mock_experiences if exp['id'] != exp_id]
        flash('Experience deleted (local mock data).', 'success')
        
    return redirect(url_for('admin'))

@app.route('/admin/bulk_action', methods=['POST'])
@admin_required
def admin_bulk_action():
    action = request.form.get('action')
    selected_ids = request.form.getlist('selected_ids')
    
    if not selected_ids:
        flash('No items selected.', 'error')
        return redirect(url_for('admin'))
        
    if supabase:
        try:
            if action == 'delete':
                for exp_id in selected_ids:
                    supabase.table('experiences').delete().eq('id', int(exp_id)).execute()
                flash(f'Successfully deleted {len(selected_ids)} experiences.', 'success')
            elif action == 'verify':
                for exp_id in selected_ids:
                    supabase.table('experiences').update({'is_verified': True}).eq('id', int(exp_id)).execute()
                flash(f'Successfully verified {len(selected_ids)} experiences.', 'success')
        except Exception as e:
            flash(f'Bulk action error: {str(e)}', 'error')
    else:
        flash('Bulk actions require Supabase.', 'error')
        
    return redirect(url_for('admin'))

@app.route('/admin/add_experience', methods=['POST'])
@admin_required
def admin_add_experience():
    title = request.form.get('title')
    category = request.form.get('category')
    details = request.form.get('details')
    
    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    new_exp = {
        "name": "Admin Override",
        "email": "admin@stxarchive.com",
        "is_anonymous": False,
        "category": category,
        "date": date_str,
        "title": title,
        "details": details,
        "is_verified": True
    }
    
    if supabase:
        try:
            supabase.table('experiences').insert(new_exp).execute()
            flash('Experience forcefully added.', 'success')
        except Exception as e:
            flash(f'Error adding experience: {str(e)}', 'error')
    else:
        new_exp["id"] = len(mock_experiences) + 1
        mock_experiences.insert(0, new_exp)
        flash('Experience added (local mock data).', 'success')
        
    return redirect(url_for('admin'))

@app.route('/admin/upload_evidence', methods=['POST'])
@admin_required
def upload_evidence():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        image_url = request.form.get('image_url', '')
        description = request.form.get('description')
        
        from datetime import datetime
        date_str = datetime.now().strftime("%B %d, %Y")
        
        new_evidence = {
            "title": title,
            "category": category,
            "image_url": image_url,
            "description": description,
            "date": date_str
        }
        
        if supabase:
            try:
                supabase.table('evidence').insert(new_evidence).execute()
                flash('Evidence uploaded successfully.', 'success')
            except Exception as e:
                flash(f'Error uploading evidence: {str(e)}', 'error')
        else:
            flash('Evidence upload requires Supabase configuration.', 'error')
            
    return redirect(url_for('admin'))

@app.route('/admin/delete_evidence/<int:ev_id>', methods=['POST'])
@admin_required
def delete_evidence(ev_id):
    if supabase:
        try:
            supabase.table('evidence').delete().eq('id', ev_id).execute()
            flash('Evidence deleted successfully.', 'success')
        except Exception as e:
            flash(f'Error deleting evidence: {str(e)}', 'error')
    else:
        flash('Evidence deletion requires Supabase configuration.', 'error')
        
    return redirect(url_for('admin'))

@app.route('/admin/add_timeline', methods=['POST'])
@admin_required
def add_timeline():
    if request.method == 'POST':
        title = request.form.get('title')
        status = request.form.get('status')
        description = request.form.get('description')
        
        from datetime import datetime
        date_str = datetime.now().strftime("%B %Y")
        
        new_timeline = {
            "title": title,
            "status": status,
            "description": description,
            "date": date_str
        }
        
        if supabase:
            try:
                supabase.table('incidents').insert(new_timeline).execute()
                flash('Timeline event added successfully.', 'success')
            except Exception as e:
                flash(f'Error adding timeline event: {str(e)}', 'error')
        else:
            flash('Timeline addition requires Supabase configuration.', 'error')
            
    return redirect(url_for('admin'))

@app.route('/admin/delete_timeline/<int:inc_id>', methods=['POST'])
@admin_required
def delete_timeline(inc_id):
    if supabase:
        try:
            supabase.table('incidents').delete().eq('id', inc_id).execute()
            flash('Timeline event deleted successfully.', 'success')
        except Exception as e:
            flash(f'Error deleting timeline event: {str(e)}', 'error')
    else:
        flash('Timeline deletion requires Supabase configuration.', 'error')
        
    return redirect(url_for('admin'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        with open('admin_credentials.txt', 'r') as f:
            creds = f.readlines()
            correct_username = creds[0].split(': ')[1].strip()
            correct_password = creds[1].split(': ')[1].strip()
            
        if username == correct_username and password == correct_password:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid admin credentials', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/change_password', methods=['POST'])
@admin_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    
    with open('admin_credentials.txt', 'r') as f:
        creds = f.readlines()
        correct_username = creds[0].split(': ')[1].strip()
        correct_password = creds[1].split(': ')[1].strip()
        
    if current_password == correct_password:
        with open('admin_credentials.txt', 'w') as f:
            f.write(f"Username: {correct_username}\n")
            f.write(f"Password: {new_password}\n")
        flash('Admin password changed successfully.', 'success')
    else:
        flash('Incorrect current password.', 'error')
        
    return redirect(url_for('admin'))

@app.route('/admin/toggle_maintenance', methods=['POST'])
@admin_required
def toggle_maintenance():
    if os.path.exists('.maintenance'):
        os.remove('.maintenance')
        flash('Maintenance mode DISABLED. Site is live.', 'success')
    else:
        with open('.maintenance', 'w') as f:
            f.write('Maintenance mode active')
        flash('Maintenance mode ENABLED. Public site is offline.', 'error')
    return redirect(url_for('admin'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username:
            flash('Username is required.', 'error')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))

        if supabase:
            try:
                # Basic check for username uniqueness via supabase would require a separate table,
                # but we'll try to just sign up with metadata for now.
                response = supabase.auth.sign_up({
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {
                            "username": username
                        }
                    }
                })
                
                # Supabase returns an empty identities list if the email is already registered (to prevent email enumeration)
                if response.user and not response.user.identities:
                    flash('An account with this email already exists.', 'error')
                    return redirect(url_for('signup'))
                
                # Supabase auth handles verification emails automatically if configured.
                session['user_logged_in'] = True
                session['user_email'] = email
                session['user_username'] = username
                session['email_verified'] = False # Requires them to click email link
                flash('Account created! Please check your email to verify your account.', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error signing up: {str(e)}', 'error')
        else:
            # Fallback mock users
            if any(u['email'] == email for u in mock_users):
                flash('Email already exists.', 'error')
            elif any(u['username'] == username for u in mock_users):
                flash('Username already taken.', 'error')
            else:
                mock_users.append({'email': email, 'password': password, 'username': username, 'is_verified': False})
                session['user_logged_in'] = True
                session['user_email'] = email
                session['user_username'] = username
                session['email_verified'] = False
                flash('Account created (local mode)! Please verify your email to post.', 'success')
                return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if supabase:
            try:
                response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                user = response.user
                session['user_logged_in'] = True
                session['user_email'] = user.email
                session['user_username'] = user.user_metadata.get('username', user.email.split('@')[0])
                
                # Check if email is verified in Supabase
                session['email_verified'] = user.email_confirmed_at is not None
                
                flash('Logged in successfully.', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash('Invalid credentials or error logging in.', 'error')
        else:
            user = next((u for u in mock_users if u['email'] == email and u['password'] == password), None)
            if user:
                session['user_logged_in'] = True
                session['user_email'] = email
                session['user_username'] = user.get('username', email.split('@')[0])
                session['email_verified'] = user.get('is_verified', False)
                
                flash('Logged in successfully (local mode).', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid credentials.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('user_logged_in', None)
    session.pop('user_email', None)
    session.pop('user_username', None)
    session.pop('email_verified', None)
    if supabase:
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
