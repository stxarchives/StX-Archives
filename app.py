import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from supabase import create_client, Client
from dotenv import load_dotenv
from functools import wraps
from werkzeug.utils import secure_filename
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

import time

maintenance_cache = {
    'status': False,
    'last_checked': 0
}

@app.before_request
def check_maintenance():
    # Never block or query DB for static files
    if request.path.startswith('/static'):
        return

    global maintenance_cache
    current_time = time.time()
    
    # Check database only once every 60 seconds
    if current_time - maintenance_cache['last_checked'] > 60:
        is_maintenance = False
        if supabase:
            try:
                res = supabase.table('site_settings').select('value').eq('key', 'maintenance_mode').execute()
                if res.data and res.data[0]['value'] == 'true':
                    is_maintenance = True
            except:
                pass
        elif os.path.exists('.maintenance'):
            is_maintenance = True
            
        maintenance_cache['status'] = is_maintenance
        maintenance_cache['last_checked'] = current_time

    if maintenance_cache['status']:
        if request.path.startswith('/admin'):
            return
        return render_template('maintenance.html'), 503

CATEGORIES = [
    "Facilities & Infrastructure",
    "Academic Policies",
    "Fee Discrepancies",
    "Staff Conduct",
    "Other Incident"
]

@app.route('/')
def index():
    category_counts = {c: 0 for c in CATEGORIES}
    
    recent_experiences = []
    
    if supabase:
        try:
            response = supabase.table('experiences').select('category').execute()
            for row in response.data:
                cat = row.get('category')
                if cat in category_counts:
                    category_counts[cat] += 1
            
            recent_response = supabase.table('experiences').select('*').order('id', desc=True).limit(5).execute()
            recent_experiences = recent_response.data
        except Exception as e:
            print(f"Supabase error: {e}")
            for exp in mock_experiences:
                cat = exp.get('category')
                if cat in category_counts:
                    category_counts[cat] += 1
            recent_experiences = mock_experiences[:5]
    else:
        for exp in mock_experiences:
            cat = exp.get('category')
            if cat in category_counts:
                category_counts[cat] += 1
        recent_experiences = mock_experiences[:5]
                
    return render_template('index.html', category_counts=category_counts, recent_experiences=recent_experiences)

@app.route('/timeline')
def timeline():
    events = [] 
    if supabase:
        try:
            response = supabase.table('incidents').select('*').order('id', desc=False).execute()
            events = response.data
        except Exception as e:
            print(f"Supabase error fetching timeline: {e}")
            events = mock_timeline
    else:
        events = mock_timeline
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
            evidence_list = mock_evidence
    else:
        evidence_list = mock_evidence
            
    return render_template('archive.html', evidence=evidence_list)

app.config['UPLOAD_FOLDER_TEACHERS'] = 'static/uploads/teachers'

@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
    if request.method == 'POST':
        if 'user_logged_in' not in session and 'admin_logged_in' not in session:
            flash('You must be logged in to add a teacher.', 'error')
            return redirect(url_for('login'))
            
        name = request.form.get('name')
        subject = request.form.get('subject')
        description = request.form.get('description')
        
        image_url = ""
        
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                if supabase:
                    try:
                        file_bytes = file.read()
                        # Upload to Supabase Storage
                        res = supabase.storage.from_("uploads").upload(
                            file=file_bytes,
                            path=f"teachers/{filename}",
                            file_options={"content-type": file.content_type}
                        )
                        # Get public URL
                        public_url = supabase.storage.from_("uploads").get_public_url(f"teachers/{filename}")
                        image_url = public_url
                    except Exception as e:
                        print(f"Error uploading to Supabase Storage: {e}")
                        # Fallback to local save
                        filepath = os.path.join(app.config['UPLOAD_FOLDER_TEACHERS'], filename)
                        file.seek(0)
                        file.save(filepath)
                        image_url = '/' + filepath
                else:
                    filepath = os.path.join(app.config['UPLOAD_FOLDER_TEACHERS'], filename)
                    file.save(filepath)
                    image_url = '/' + filepath

        new_teacher = {
            "name": name,
            "subject": subject,
            "description": description,
            "image_url": image_url or "https://via.placeholder.com/800x600?text=No+Image"
        }
        
        if supabase:
            try:
                # Add default reactions/votes for new inserts
                new_teacher["reactions"] = {'🔥': 0, '👏': 0, '😂': 0, '😢': 0, '😡': 0}
                new_teacher["helpful_votes"] = {'yes': 0, 'no': 0}
                supabase.table('teachers').insert(new_teacher).execute()
                flash('Teacher profile submitted successfully to Supabase.', 'success')
                return redirect(url_for('teachers'))
            except Exception as e:
                print(f"Error adding teacher to Supabase: {e}")
                flash('Falling back to local data.', 'error')

        # Fallback
        new_teacher["id"] = len(mock_teachers) + 1
        new_teacher["reactions"] = {'🔥': 0, '👏': 0, '😂': 0, '😢': 0, '😡': 0}
        new_teacher["helpful_votes"] = {'yes': 0, 'no': 0}
        mock_teachers.insert(0, new_teacher)
        flash('Teacher profile submitted successfully (local).', 'success')
        return redirect(url_for('teachers'))
        
    teachers_data = mock_teachers
    if supabase:
        try:
            response = supabase.table('teachers').select('*').order('id', desc=True).execute()
            if response.data:
                teachers_data = response.data
        except Exception as e:
            print(f"Supabase error fetching teachers: {e}")
            
    return render_template('teachers.html', teachers=teachers_data)

@app.route('/teacher/<int:teacher_id>')
def teacher_detail(teacher_id):
    teacher = None
    if supabase:
        try:
            response = supabase.table('teachers').select('*').eq('id', teacher_id).execute()
            if response.data:
                teacher = response.data[0]
        except Exception as e:
            print(f"Supabase error fetching teacher detail: {e}")
            
    if not teacher:
        teacher = next((t for t in mock_teachers if t['id'] == teacher_id), None)
        
    if not teacher:
        flash('Teacher not found.', 'error')
        return redirect(url_for('teachers'))
    return render_template('teacher_detail.html', teacher=teacher)

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
        "category": "Academic Policies",
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
    }
]

for exp in mock_experiences:
    exp['reactions'] = {'🔥': 0, '👏': 0, '😂': 0, '😢': 0, '😡': 0}
    exp['helpful_votes'] = {'yes': 0, 'no': 0}

@app.route('/api/experience/<int:exp_id>/react', methods=['POST'])
def react_experience(exp_id):
    session_key = f'reacted_exp_{exp_id}'
    data = request.json
    emoji = data.get('emoji')
    
    exp = None
    if supabase:
        try:
            response = supabase.table('experiences').select('*').eq('id', exp_id).execute()
            if response.data:
                exp = response.data[0]
        except Exception as e:
            print(f"Supabase error fetching exp for react: {e}")
            
    if not exp:
        exp = next((e for e in mock_experiences if e['id'] == exp_id), None)
        
    if not exp or 'reactions' not in exp or emoji not in exp['reactions']:
        return jsonify({'success': False, 'error': 'Experience or valid emoji not found'}), 404
        
    current_reaction = session.get(session_key)
    if current_reaction is True:
        session.pop(session_key, None)
        current_reaction = None
        
    if current_reaction:
        if current_reaction == emoji:
            exp['reactions'][emoji] = max(0, exp['reactions'][emoji] - 1)
            session.pop(session_key, None)
            action = 'reverted'
            selected = None
        else:
            exp['reactions'][current_reaction] = max(0, exp['reactions'][current_reaction] - 1)
            exp['reactions'][emoji] = exp['reactions'].get(emoji, 0) + 1
            session[session_key] = emoji
            action = 'changed'
            selected = emoji
    else:
        exp['reactions'][emoji] = exp['reactions'].get(emoji, 0) + 1
        session[session_key] = emoji
        action = 'added'
        selected = emoji
        
    if supabase:
        try:
            supabase.table('experiences').update({'reactions': exp['reactions']}).eq('id', exp_id).execute()
        except Exception as e:
            print(f"Supabase error updating react: {e}")
            
    return jsonify({'success': True, 'reactions': exp['reactions'], 'action': action, 'selected': selected})

@app.route('/api/experience/<int:exp_id>/vote', methods=['POST'])
def vote_experience(exp_id):
    session_key = f'voted_exp_{exp_id}'
    data = request.json
    vote = data.get('vote')
    
    exp = None
    if supabase:
        try:
            response = supabase.table('experiences').select('*').eq('id', exp_id).execute()
            if response.data:
                exp = response.data[0]
        except Exception as e:
            print(f"Supabase error fetching exp for vote: {e}")
            
    if not exp:
        exp = next((e for e in mock_experiences if e['id'] == exp_id), None)
        
    if not exp or 'helpful_votes' not in exp or vote not in exp['helpful_votes']:
        return jsonify({'success': False, 'error': 'Experience or vote type not found'}), 404
        
    current_vote = session.get(session_key)
    if current_vote:
        if current_vote == vote:
            exp['helpful_votes'][vote] = max(0, exp['helpful_votes'][vote] - 1)
            session.pop(session_key, None)
            action = 'reverted'
            selected = None
        else:
            exp['helpful_votes'][current_vote] = max(0, exp['helpful_votes'][current_vote] - 1)
            exp['helpful_votes'][vote] = exp['helpful_votes'].get(vote, 0) + 1
            session[session_key] = vote
            action = 'changed'
            selected = vote
    else:
        exp['helpful_votes'][vote] = exp['helpful_votes'].get(vote, 0) + 1
        session[session_key] = vote
        action = 'added'
        selected = vote
        
    if supabase:
        try:
            supabase.table('experiences').update({'helpful_votes': exp['helpful_votes']}).eq('id', exp_id).execute()
        except Exception as e:
            print(f"Supabase error updating vote: {e}")
            
    return jsonify({'success': True, 'helpful_votes': exp['helpful_votes'], 'action': action, 'selected': selected})

@app.route('/api/teacher/<int:teacher_id>/react', methods=['POST'])
def react_teacher(teacher_id):
    session_key = f'reacted_teacher_{teacher_id}'
    data = request.json
    emoji = data.get('emoji')
    
    teacher = None
    if supabase:
        try:
            response = supabase.table('teachers').select('*').eq('id', teacher_id).execute()
            if response.data:
                teacher = response.data[0]
        except Exception as e:
            print(f"Supabase error fetching teacher for react: {e}")
            
    if not teacher:
        teacher = next((t for t in mock_teachers if t['id'] == teacher_id), None)
        
    if not teacher or 'reactions' not in teacher or emoji not in teacher['reactions']:
        return jsonify({'success': False, 'error': 'Teacher or valid emoji not found'}), 404
        
    current_reaction = session.get(session_key)
    if current_reaction is True:
        session.pop(session_key, None)
        current_reaction = None
        
    if current_reaction:
        if current_reaction == emoji:
            teacher['reactions'][emoji] = max(0, teacher['reactions'][emoji] - 1)
            session.pop(session_key, None)
            action = 'reverted'
            selected = None
        else:
            teacher['reactions'][current_reaction] = max(0, teacher['reactions'][current_reaction] - 1)
            teacher['reactions'][emoji] = teacher['reactions'].get(emoji, 0) + 1
            session[session_key] = emoji
            action = 'changed'
            selected = emoji
    else:
        teacher['reactions'][emoji] = teacher['reactions'].get(emoji, 0) + 1
        session[session_key] = emoji
        action = 'added'
        selected = emoji
        
    if supabase:
        try:
            supabase.table('teachers').update({'reactions': teacher['reactions']}).eq('id', teacher_id).execute()
        except Exception as e:
            print(f"Supabase error updating teacher react: {e}")
            
    return jsonify({'success': True, 'reactions': teacher['reactions'], 'action': action, 'selected': selected})

@app.route('/api/teacher/<int:teacher_id>/vote', methods=['POST'])
def vote_teacher(teacher_id):
    session_key = f'voted_teacher_{teacher_id}'
    data = request.json
    vote = data.get('vote')
    
    teacher = None
    if supabase:
        try:
            response = supabase.table('teachers').select('*').eq('id', teacher_id).execute()
            if response.data:
                teacher = response.data[0]
        except Exception as e:
            print(f"Supabase error fetching teacher for vote: {e}")
            
    if not teacher:
        teacher = next((t for t in mock_teachers if t['id'] == teacher_id), None)
        
    if not teacher or 'helpful_votes' not in teacher or vote not in teacher['helpful_votes']:
        return jsonify({'success': False, 'error': 'Teacher or vote type not found'}), 404
        
    current_vote = session.get(session_key)
    if current_vote:
        if current_vote == vote:
            teacher['helpful_votes'][vote] = max(0, teacher['helpful_votes'][vote] - 1)
            session.pop(session_key, None)
            action = 'reverted'
            selected = None
        else:
            teacher['helpful_votes'][current_vote] = max(0, teacher['helpful_votes'][current_vote] - 1)
            teacher['helpful_votes'][vote] = teacher['helpful_votes'].get(vote, 0) + 1
            session[session_key] = vote
            action = 'changed'
            selected = vote
    else:
        teacher['helpful_votes'][vote] = teacher['helpful_votes'].get(vote, 0) + 1
        session[session_key] = vote
        action = 'added'
        selected = vote
        
    if supabase:
        try:
            supabase.table('teachers').update({'helpful_votes': teacher['helpful_votes']}).eq('id', teacher_id).execute()
        except Exception as e:
            print(f"Supabase error updating teacher vote: {e}")
            
    return jsonify({'success': True, 'helpful_votes': teacher['helpful_votes'], 'action': action, 'selected': selected})

mock_users = []
mock_evidence = []
mock_timeline = []

mock_teachers = [
    {
        "id": 1,
        "name": "Physics Teacher",
        "subject": "Physics",
        "description": """
<h1 class="text-xl font-bold mb-4">The Legendary Physics Teacher: A Scientific Investigation 💀</h1>
<p class="mb-2">Every school has that one teacher.</p>
<p class="mb-2">The teacher who walks into class with the confidence of a man who has personally solved every problem in the textbook, while the students are still trying to figure out what the question is asking.</p>
<p class="mb-2">And then there is <strong>this guy.</strong></p>
<p class="mb-2">A Physics teacher for Class 11 and 12.</p>
<p class="mb-2">A man responsible for teaching Newton's laws, vectors, gravitation, rotational motion, work, energy and everything else that makes students question their life choices.</p>
<p class="mb-4">Yet somehow, the biggest unsolved problem in this entire classroom is:</p>
<p class="mb-4"><strong>How does this man have so much confidence in that photograph?</strong> 💀</p>

<p class="mb-2">Let's begin with the outfit.</p>
<p class="mb-2">The bow tie is clearly trying to tell us: <strong>“James Bond.”</strong></p>
<p class="mb-4">Unfortunately, the pose is replying: <strong>“Sir, where is my Uber?”</strong> 😭</p>

<p class="mb-2">The suit is formal. The shoes are polished. The bow tie is fighting for survival. And the plants in the background have somehow become the most photogenic characters in the entire picture.</p>
<p class="mb-2">The photographer probably said: <em>“Sir, just pose naturally.”</em></p>
<p class="mb-4">And bro immediately entered <strong>staff-meeting mode.</strong></p>

<p class="mb-2">One hand in the pocket. One hand hanging down. Expression completely undecided. Bro wasn't posing. <strong>He was buffering.</strong> 💀</p>
<p class="mb-2">He teaches vectors, yet his arms are pointing in completely different directions.</p>
<p class="mb-2">He teaches equilibrium, yet this photograph is the most unstable system ever observed.</p>
<p class="mb-4">He teaches gravitation, but somehow the only thing experiencing gravitational collapse is his aura. 📉</p>

<p class="mb-2">Newton gave us three laws of motion. This man has apparently discovered a fourth:</p>
<p class="mb-6"><strong>If the photographer says “pose,” immediately forget how the human body works.</strong></p>

<hr class="my-6 border-gray-200 dark:border-gray-700">

<h2 class="text-lg font-bold mb-4">The Physics Department Has a Problem</h2>
<p class="mb-2">The funniest thing is that this isn't just some random man in a suit. This is a <strong>Physics teacher for Class 11 and 12.</strong> Which makes everything ten times funnier.</p>
<p class="mb-2">He can explain complicated equations, but apparently cannot explain the fundamental equation:</p>
<p class="mb-4"><strong>Photographer + Camera + Pose = Please Try Again.</strong></p>

<p class="mb-2">He teaches rotational motion. Meanwhile, his students' heads are rotating after he explains a numerical for 25 minutes.</p>
<p class="mb-2">He teaches work and energy. Yet somehow the students are doing all the work while the remaining classroom energy disappears.</p>
<p class="mb-4">He teaches time-related concepts. And ironically, he has apparently mastered the art of making <strong>time disappear.</strong> 💀</p>

<p class="mb-2">The syllabus is already finished. The chapters are done. The revision is done. The doubts are done. Everyone thinks the period will finally be peaceful.</p>
<p class="mb-2">Then comes the immortal sentence:</p>
<p class="mb-2"><strong>“Actually, let me tell you something…”</strong></p>
<p class="mb-4">And suddenly another 20 minutes have vanished.</p>

<p class="mb-2">Bro doesn't waste time. <strong>He conducts experiments on it.</strong></p>
<p class="mb-6">At this point, Class 11 and 12 don't need another Physics chapter. They need a stopwatch.</p>

<hr class="my-6 border-gray-200 dark:border-gray-700">

<h2 class="text-lg font-bold mb-4">The Mysterious Classroom Justice System</h2>
<p class="mb-4">Now we reach the most fascinating part of this scientific investigation. According to the completely exaggerated student-lore version of events, the classroom apparently operates under a strange set of disciplinary laws.</p>

<p class="mb-2">Girls: <strong>HAHAHAHAHAHAHAHA!</strong></p>
<p class="mb-4">Sir: “Okay, okay.”</p>

<p class="mb-2">Boys: <em>one tiny sound</em></p>
<p class="mb-4">Sir: <strong>“WHO WAS THAT?”</strong> 💀</p>

<p class="mb-2">A girl could apparently produce enough noise to wake up the entire chemistry department and the class would continue.</p>
<p class="mb-4">A boy drops his pen: <strong>“WHY ARE YOU DISTURBING THE CLASS?”</strong></p>

<p class="mb-4">At this point, the boys aren't afraid of Physics. <strong>They're afraid of breathing too loudly.</strong> 😭</p>

<p class="mb-2">Newton's third law states that every action has an equal and opposite reaction. Apparently that law doesn't apply to classroom discipline. Because in this classroom:</p>
<p class="mb-2"><strong>Girl makes noise → gentle warning.</strong></p>
<p class="mb-4"><strong>Boy makes noise → immediate investigation by the Physics Department.</strong></p>

<p class="mb-6">The boys aren't students anymore. They're <strong>suspects.</strong> 💀</p>

<hr class="my-6 border-gray-200 dark:border-gray-700">

<h2 class="text-lg font-bold mb-4">The Famous Physics-Chemistry Connection</h2>
<p class="mb-4">And then there is the plot twist. Our Physics teacher is engaged to the <strong>Class 10 Chemistry teacher.</strong></p>

<p class="mb-2">Physics + Chemistry. Force + Reaction. Motion + Reaction.</p>
<p class="mb-4">Apparently, the school has accidentally created its own interdisciplinary research project. 💀</p>

<p class="mb-4">The students are studying scientific bonding in the classroom while their teachers are demonstrating it in real life.</p>

<p class="mb-4">At this point, the staff room isn't a staff room. It's a <strong>research laboratory.</strong></p>

<p class="mb-2">The Physics teacher explains forces. The Chemistry teacher explains reactions. Together they have apparently demonstrated:</p>
<p class="mb-4"><strong>Force + Reaction = Engagement.</strong> 😭</p>

<p class="mb-6">Meanwhile, Class 11 and 12 are sitting there wondering: <strong>“Sir, is this in the syllabus?”</strong></p>

<hr class="my-6 border-gray-200 dark:border-gray-700">

<h2 class="text-lg font-bold mb-4">The Great Side-Quest Master</h2>
<p class="mb-4">One of his greatest abilities is apparently finding a completely unnecessary side quest after everything important has already been completed.</p>

<p class="mb-4">Syllabus? Finished. Chapter? Finished. Revision? Finished. Doubts? Finished. Free time? <strong>Not anymore.</strong> 💀</p>

<p class="mb-4">Somehow there is always one more story. One more explanation. One more conversation. One more completely unrelated topic.</p>

<p class="mb-2">Students are sitting there thinking: <strong>“Sir, the period is over.”</strong></p>
<p class="mb-4">And somewhere in the distance: <strong>“Just one last thing...”</strong></p>

<p class="mb-6">That “one last thing” has more sequels than a Marvel movie. 😭</p>

<hr class="my-6 border-gray-200 dark:border-gray-700">

<h2 class="text-lg font-bold mb-4">The Photograph That Started Everything</h2>
<p class="mb-4">But none of this would matter if the photograph wasn't so devastatingly funny.</p>

<p class="mb-4">The bow tie is trying to increase the sophistication. The suit is trying to establish authority. The shoes are trying to maintain professionalism. The plants are trying to make the background respectable.</p>

<p class="mb-4">And the man in the middle is just standing there like: <strong>“Yes. This is definitely my best angle.”</strong></p>

<p class="mb-4">The photographer probably took 200 pictures. Some were probably blurry. Some were probably badly lit. Some probably had someone walking behind him. And somehow...</p>

<p class="mb-4"><strong>THIS ONE SURVIVED QUALITY CONTROL.</strong> 💀</p>

<p class="mb-6">That's the real achievement. Not teaching Physics. Not completing the syllabus. Not surviving Class 11 and 12. <strong>Getting this photograph approved.</strong></p>

<hr class="my-6 border-gray-200 dark:border-gray-700">

<h1 class="text-xl font-bold mb-4">Final Scientific Assessment</h1>
<p class="mb-4">After extensive research, observation and absolutely unnecessary analysis, the results are conclusive:</p>

<ul class="list-disc pl-5 mb-6 space-y-2">
    <li><strong>Physics:</strong> Passed</li>
    <li><strong>Chemistry connection:</strong> Confirmed</li>
    <li><strong>Syllabus:</strong> Finished</li>
    <li><strong>Time wasted:</strong> Unquantifiable</li>
    <li><strong>Classroom discipline:</strong> Highly questionable</li>
    <li><strong>Bow tie:</strong> Fighting for its life</li>
    <li><strong>Pose:</strong> Failed practical</li>
    <li><strong>Background plants:</strong> Carried the photograph</li>
    <li><strong>Self-confidence:</strong> Surprisingly high</li>
    <li><strong>Photographic judgment:</strong> Under investigation</li>
    <li><strong>Aura:</strong> Experiencing free fall</li>
</ul>

<p class="mb-2"><strong>Final Equation:</strong></p>
<h2 class="text-lg font-bold mb-2">Physics + Chemistry + Bow Tie + Awkward Pose + Classroom Side Quests =</h2>
<h2 class="text-xl font-black text-airred mb-6">THE MOST OVERQUALIFIED WAY TO LOOK LIKE YOU'RE STILL WAITING FOR SOMEONE TO TELL YOU WHERE TO STAND. 💀</h2>

<p class="mb-2"><strong>Final result: FAIL.</strong></p>
<p class="mb-2 text-lg"><strong>Sir, please remain after class. We need to discuss your photograph.</strong></p>
""",
        "image_url": "/static/uploads/teachers/physics_teacher.jpg"
    }
]

for teacher in mock_teachers:
    teacher['reactions'] = {'🔥': 0, '👏': 0, '😂': 0, '😢': 0, '😡': 0}
    teacher['helpful_votes'] = {'yes': 0, 'no': 0}
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
            new_exp['reactions'] = {'👍': 0, '❤️': 0, '😂': 0, '😮': 0, '😢': 0, '🙏': 0}
            new_exp['helpful_votes'] = {'yes': 0, 'no': 0}
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

    return render_template('experience.html', experiences=experiences, current_category=category_filter, categories=CATEGORIES)

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

def get_page_content(page_id, default_content=""):
    if supabase:
        try:
            res = supabase.table('pages').select('content').eq('id', page_id).execute()
            if res.data:
                return res.data[0]['content']
        except:
            pass
    return default_content

@app.route('/principals-note')
def principals_note():
    content = get_page_content('principals_note', '<div class="max-w-4xl mx-auto px-6 mb-20 text-center text-gray-500 font-bold uppercase tracking-widest">[ Content Redacted / Pending Verification ]</div>')
    return render_template('principals_note.html', content=content)

@app.route('/hall-of-shame')
def hall_of_shame():
    content = get_page_content('hall_of_shame', '<div class="max-w-4xl mx-auto px-6 mb-20 text-center text-gray-500 font-bold uppercase tracking-widest">[ Content Redacted / Pending Verification ]</div>')
    return render_template('hall_of_shame.html', content=content)

@app.route('/fee-scam')
def fee_scam():
    content = get_page_content('fee_scam', '<div class="max-w-4xl mx-auto px-6 mb-20 text-center text-gray-500 font-bold uppercase tracking-widest">[ Content Redacted / Pending Verification ]</div>')
    return render_template('fee_scam.html', content=content)

@app.route('/vip-treatment')
def vip_treatment():
    content = get_page_content('vip_treatment', '<div class="max-w-4xl mx-auto px-6 mb-20 text-center text-gray-500 font-bold uppercase tracking-widest">[ Content Redacted / Pending Verification ]</div>')
    return render_template('vip_treatment.html', content=content)

@app.route('/admin')
@admin_required
def admin():
    experiences = []
    evidence_list = []
    incidents_list = []
    
    is_maintenance = False
    if supabase:
        try:
            res = supabase.table('site_settings').select('value').eq('key', 'maintenance_mode').execute()
            if res.data and res.data[0]['value'] == 'true':
                is_maintenance = True
        except:
            pass
    elif os.path.exists('.maintenance'):
        is_maintenance = True
        
    analytics = {
        "total": 0,
        "verified": 0,
        "pending": 0,
        "maintenance": is_maintenance
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
            evidence_list = mock_evidence
            incidents_list = mock_timeline
    else:
        experiences = mock_experiences
        evidence_list = mock_evidence
        incidents_list = mock_timeline
        analytics['total'] = len(experiences)
        analytics['verified'] = sum(1 for e in experiences if e.get('is_verified'))
        analytics['pending'] = analytics['total'] - analytics['verified']
        
    pages_content = {}
    if supabase:
        try:
            res = supabase.table('pages').select('*').execute()
            if res.data:
                for p in res.data:
                    pages_content[p['id']] = p['content']
        except:
            pass

    return render_template('admin.html', 
                           experiences=experiences, 
                           evidence=evidence_list,
                           incidents=incidents_list,
                           analytics=analytics,
                           pages=pages_content,
                           maintenance_mode=is_maintenance)

@app.route('/admin/save-page', methods=['POST'])
@admin_required
def save_page():
    page_id = request.form.get('page_id')
    content = request.form.get('content')
    
    if not page_id or content is None:
        flash('Invalid page data.', 'error')
        return redirect(url_for('admin'))
        
    if supabase:
        try:
            # Upsert the page content
            supabase.table('pages').upsert({
                'id': page_id,
                'content': content
            }).execute()
            flash(f'Page "{page_id}" updated successfully!', 'success')
        except Exception as e:
            flash(f'Error saving page: {e}', 'error')
    else:
        flash('Supabase not connected. Cannot save page.', 'error')
        
    return redirect(url_for('admin'))

@app.route('/admin/edit-experience/<int:exp_id>', methods=['POST'])
@admin_required
def admin_edit_experience(exp_id):
    if not supabase:
        flash('Supabase not connected.', 'error')
        return redirect(url_for('admin'))
        
    title = request.form.get('title')
    details = request.form.get('details')
    category = request.form.get('category')
    
    # Optional reactions manipulation
    fake_helpful = request.form.get('fake_helpful', type=int)
    fake_unhelpful = request.form.get('fake_unhelpful', type=int)
    
    r_like = request.form.get('react_like', type=int)
    r_love = request.form.get('react_love', type=int)
    r_haha = request.form.get('react_haha', type=int)
    r_wow = request.form.get('react_wow', type=int)
    r_sad = request.form.get('react_sad', type=int)
    r_pray = request.form.get('react_pray', type=int)
    
    update_data = {
        'title': title,
        'details': details,
        'category': category
    }
    
    try:
        if fake_helpful is not None and fake_unhelpful is not None:
            update_data['helpful_votes'] = {'yes': fake_helpful, 'no': fake_unhelpful}
            
        if all(x is not None for x in [r_like, r_love, r_haha, r_wow, r_sad, r_pray]):
            update_data['reactions'] = {
                '👍': r_like,
                '❤️': r_love,
                '😂': r_haha,
                '😮': r_wow,
                '😢': r_sad,
                '🙏': r_pray
            }
            
        supabase.table('experiences').update(update_data).eq('id', exp_id).execute()
        flash('Experience updated successfully.', 'success')
    except Exception as e:
        flash(f'Error updating experience: {e}', 'error')
        
    return redirect(url_for('admin'))

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
            return redirect(url_for('admin'))
        except Exception as e:
            print(f'Error updating status: {str(e)}')
            
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
            return redirect(url_for('admin'))
        except Exception as e:
            print(f'Error deleting experience: {str(e)}')
            
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
            elif action == 'unverify':
                for exp_id in selected_ids:
                    supabase.table('experiences').update({'is_verified': False}).eq('id', int(exp_id)).execute()
                flash(f'Successfully un-verified {len(selected_ids)} experiences.', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            print(f'Bulk action error: {str(e)}')
            
    global mock_experiences
    selected_ids_int = [int(id) for id in selected_ids]
    
    if action == 'delete':
        mock_experiences = [exp for exp in mock_experiences if exp['id'] not in selected_ids_int]
        flash(f'Successfully deleted {len(selected_ids)} experiences (local mock data).', 'success')
    elif action == 'verify':
        for exp in mock_experiences:
            if exp['id'] in selected_ids_int:
                exp['is_verified'] = True
        flash(f'Successfully verified {len(selected_ids)} experiences (local mock data).', 'success')
        
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
            return redirect(url_for('admin'))
        except Exception as e:
            print(f'Error adding experience: {str(e)}')
            
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
                return redirect(url_for('admin'))
            except Exception as e:
                print(f'Error uploading evidence: {str(e)}')
                
        new_evidence['id'] = len(mock_evidence) + 1
        mock_evidence.insert(0, new_evidence)
        flash('Evidence uploaded (local mock data).', 'success')
            
    return redirect(url_for('admin'))

@app.route('/admin/delete_evidence/<int:ev_id>', methods=['POST'])
@admin_required
def delete_evidence(ev_id):
    if supabase:
        try:
            supabase.table('evidence').delete().eq('id', ev_id).execute()
            flash('Evidence deleted successfully.', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            print(f'Error deleting evidence: {str(e)}')
            
    global mock_evidence
    mock_evidence = [e for e in mock_evidence if e.get('id') != ev_id]
    flash('Evidence deleted (local mock data).', 'success')
        
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
                return redirect(url_for('admin'))
            except Exception as e:
                print(f'Error adding timeline event: {str(e)}')
                
        new_timeline['id'] = len(mock_timeline) + 1
        mock_timeline.append(new_timeline)
        flash('Timeline event added (local mock data).', 'success')
            
    return redirect(url_for('admin'))

@app.route('/admin/delete_timeline/<int:inc_id>', methods=['POST'])
@admin_required
def delete_timeline(inc_id):
    if supabase:
        try:
            supabase.table('incidents').delete().eq('id', inc_id).execute()
            flash('Timeline event deleted successfully.', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            print(f'Error deleting timeline event: {str(e)}')
            
    global mock_timeline
    mock_timeline = [t for t in mock_timeline if t.get('id') != inc_id]
    flash('Timeline event deleted (local mock data).', 'success')
        
    return redirect(url_for('admin'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        correct_username = os.environ.get('ADMIN_USERNAME', 'admin_portal')
        correct_password = os.environ.get('ADMIN_PASSWORD', 'Tk(7p#Lw9$vM2qRz')
        try:
            with open('admin_credentials.txt', 'r') as f:
                creds = f.readlines()
                if len(creds) >= 2:
                    correct_username = creds[0].split(': ')[1].strip()
                    correct_password = creds[1].split(': ')[1].strip()
        except FileNotFoundError:
            pass
            
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
    
    correct_username = os.environ.get('ADMIN_USERNAME', 'admin_portal')
    correct_password = os.environ.get('ADMIN_PASSWORD', 'Tk(7p#Lw9$vM2qRz')
    try:
        with open('admin_credentials.txt', 'r') as f:
            creds = f.readlines()
            if len(creds) >= 2:
                correct_username = creds[0].split(': ')[1].strip()
                correct_password = creds[1].split(': ')[1].strip()
    except FileNotFoundError:
        pass
        
    if current_password == correct_password:
        try:
            with open('admin_credentials.txt', 'w') as f:
                f.write(f"Username: {correct_username}\n")
                f.write(f"Password: {new_password}\n")
            flash('Admin password changed successfully.', 'success')
        except OSError:
            flash('Cannot change password on read-only server. Please update ADMIN_PASSWORD environment variable instead.', 'error')
    else:
        flash('Incorrect current password.', 'error')
        
    return redirect(url_for('admin'))

@app.route('/admin/toggle_maintenance', methods=['POST'])
@admin_required
def toggle_maintenance():
    if supabase:
        try:
            res = supabase.table('site_settings').select('value').eq('key', 'maintenance_mode').execute()
            current = res.data[0]['value'] if res.data else 'false'
            new_val = 'false' if current == 'true' else 'true'
            supabase.table('site_settings').upsert({'key': 'maintenance_mode', 'value': new_val}).execute()
            if new_val == 'true':
                flash('Maintenance mode ENABLED. Public site is offline.', 'error')
            else:
                flash('Maintenance mode DISABLED. Site is live.', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            flash(f'Error toggling maintenance mode: {str(e)}', 'error')
            
    # Fallback to local file
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
                flash('Account created! Please check your email to verify your account before logging in.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                error_msg = str(e)
                if 'Error sending confirmation email' in error_msg or 'rate limit' in error_msg.lower():
                    flash('Server email limits reached. Please email stx.archives@proton.me to create your account manually.', 'error')
                else:
                    flash(f'Error signing up: {error_msg}', 'error')
        else:
            # Fallback mock users
            if any(u['email'] == email for u in mock_users):
                flash('Email already exists.', 'error')
            elif any(u['username'] == username for u in mock_users):
                flash('Username already taken.', 'error')
            else:
                mock_users.append({'email': email, 'password': password, 'username': username, 'is_verified': False})
                flash('Account created (local mode)! Please login.', 'success')
                return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and request.args.get('verified') == 'true':
        flash('Email verified! Please log in with your credentials.', 'success')

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
