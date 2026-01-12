"""
College Chatbot Web Application
Flask Backend with Authentication and Role-Based Access
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import re
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production-2024'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Database initialization
def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_phone TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'teacher')),
            name TEXT,
            roll_number TEXT,
            department TEXT,
            photo_path TEXT,
            semester_marks TEXT,
            arrears TEXT,
            notes_link TEXT,
            subject_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add new columns if they don't exist (for existing databases)
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN semester_marks TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN arrears TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN notes_link TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN subject_notes TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN age INTEGER')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN blood_group TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN parent_details TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN chatbot_questions TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN subjects TEXT')
    except:
        pass
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('college.db')
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    """Validate phone number format (10 digits)"""
    pattern = r'^\d{10}$'
    return re.match(pattern, phone) is not None

# Routes
@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/student-login')
def student_login():
    """Student login page"""
    if 'user_id' in session and session['role'] == 'student':
        return redirect(url_for('student_dashboard'))
    return render_template('login.html', login_type='student')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page (for teachers and general)"""
    if request.method == 'POST':
        email_phone = request.form.get('email_phone', '').strip()
        password = request.form.get('password', '')
        
        if not email_phone or not password:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE email_phone = ?', (email_phone,)
        ).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['name']
            session['email_phone'] = user['email_phone']
            
            if user['role'] == 'student':
                return redirect(url_for('student_dashboard'))
            else:
                return redirect(url_for('teacher_dashboard'))
        else:
            flash('Invalid email/phone or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        role = request.form.get('role', '').strip()
        email_phone = request.form.get('email_phone', '').strip()
        password = request.form.get('password', '')
        name = request.form.get('name', '').strip()
        roll_number = request.form.get('roll_number', '').strip()
        department = request.form.get('department', '').strip()
        photo = request.files.get('photo')
        
        # Validation
        if not role or role not in ['student', 'teacher']:
            flash('Please select a valid role', 'error')
            return render_template('register.html')
        
        if not email_phone or not password:
            flash('Email/Phone and Password are required', 'error')
            return render_template('register.html')
        
        # Validate email or phone format
        if not (is_valid_email(email_phone) or is_valid_phone(email_phone)):
            flash('Please enter a valid email or 10-digit phone number', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        conn = get_db_connection()
        existing = conn.execute(
            'SELECT id FROM users WHERE email_phone = ?', (email_phone,)
        ).fetchone()
        
        if existing:
            conn.close()
            flash('Email/Phone already registered', 'error')
            return render_template('register.html')
        
        # Handle photo upload (only for students)
        photo_path = None
        if role == 'student' and photo and photo.filename:
            if allowed_file(photo.filename):
                filename = secure_filename(f"{email_phone}_{photo.filename}")
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(photo_path)
                photo_path = f"images/{filename}"
            else:
                conn.close()
                flash('Invalid file type. Please upload PNG, JPG, or JPEG', 'error')
                return render_template('register.html')
        
        # Insert user into database
        hashed_password = generate_password_hash(password)
        
        try:
            conn.execute('''
                INSERT INTO users (email_phone, password, role, name, roll_number, department, photo_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (email_phone, hashed_password, role, name, roll_number, department, photo_path))
            conn.commit()
            conn.close()
            
            flash('Registration successful! Please login', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.close()
            flash(f'Registration failed: {str(e)}', 'error')
    
    return render_template('register.html')

@app.route('/student/dashboard')
def student_dashboard():
    """Student dashboard"""
    if 'user_id' not in session or session['role'] != 'student':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', (session['user_id'],)
    ).fetchone()
    conn.close()
    
    # Parse subject notes, subjects, and parent details
    subject_notes = {}
    subjects = []
    parent_details = {}
    
    if user['subject_notes']:
        try:
            subject_notes = json.loads(user['subject_notes']) if user['subject_notes'] else {}
        except:
            subject_notes = {}
    
    if user['subjects']:
        try:
            subjects = json.loads(user['subjects']) if user['subjects'] else []
        except:
            subjects = []
    
    if user['parent_details']:
        try:
            parent_details = json.loads(user['parent_details']) if user['parent_details'] else {}
        except:
            parent_details = {}
    
    return render_template('student_dashboard.html', user=user, subject_notes=subject_notes, subjects=subjects, parent_details=parent_details)

@app.route('/teacher/dashboard')
def teacher_dashboard():
    """Teacher dashboard"""
    if 'user_id' not in session or session['role'] != 'teacher':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        students = conn.execute(
            'SELECT * FROM users WHERE role = ? ORDER BY created_at DESC', ('student',)
        ).fetchall()
        conn.close()
        
        # Parse JSON fields for each student safely
        students_data = []
        for student in students:
            student_dict = dict(student)
            # Parse subjects
            try:
                if student_dict['subjects']:
                    student_dict['subjects_parsed'] = json.loads(student_dict['subjects'])
                else:
                    student_dict['subjects_parsed'] = []
            except:
                student_dict['subjects_parsed'] = []
            
            # Parse parent details
            try:
                if student_dict['parent_details']:
                    student_dict['parent_details_parsed'] = json.loads(student_dict['parent_details'])
                else:
                    student_dict['parent_details_parsed'] = {}
            except:
                student_dict['parent_details_parsed'] = {}
            
            students_data.append(student_dict)
        
        return render_template('teacher_dashboard.html', students=students_data)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route('/chatbot')
def chatbot():
    """Chatbot page (public access)"""
    return render_template('chatbot.html', is_public=True)

@app.route('/chatbot/message', methods=['POST'])
def chatbot_message():
    """Handle chatbot messages (public access)"""
    user_message = request.json.get('message', '').strip().lower()
    
    # Simple rule-based chatbot responses
    responses = {
        'course': {
            'keywords': ['course', 'courses', 'program', 'programs', 'degree', 'degrees', 'bca', 'bsc', 'bcom', 'bba', 'ca'],
            'response': 'Sri Aravindhar Arts and Science College offers the following courses:\n\nAll courses are 3-year programs with 6 semesters, affiliated to Annamalai University.\n\n📚 COMPUTER SCIENCE DEPARTMENT:\n\n• BCA (Bachelor of Computer Applications)\n  Subjects: Programming in C, Data Structures, Database Management, Web Technologies, Software Engineering, Computer Networks, Operating Systems, Object-Oriented Programming, Java Programming, Python Programming, Mobile Application Development, Cloud Computing\n\n• BSc CS (Bachelor of Science in Computer Science)\n  Subjects: Programming Fundamentals, Data Structures & Algorithms, Database Systems, Computer Networks, Operating Systems, Software Engineering, Web Development, Mobile Computing, Artificial Intelligence, Machine Learning, Cloud Computing, Cyber Security\n\n🔢 MATHEMATICS DEPARTMENT:\n\n• BSc Maths (Bachelor of Science in Mathematics)\n  Subjects: Algebra, Calculus, Differential Equations, Statistics, Probability, Linear Algebra, Discrete Mathematics, Numerical Methods, Mathematical Modeling, Operations Research, Graph Theory, Real Analysis\n\n🔬 SCIENCE DEPARTMENT:\n\n• BSc Chemistry\n  Subjects: Organic Chemistry, Inorganic Chemistry, Physical Chemistry, Analytical Chemistry, Biochemistry, Environmental Chemistry, Industrial Chemistry, Polymer Chemistry, Spectroscopy, Quantum Chemistry, Green Chemistry, Medicinal Chemistry\n\n• BSc Physics\n  Subjects: Mechanics, Thermodynamics, Electromagnetism, Optics, Quantum Mechanics, Nuclear Physics, Solid State Physics, Electronics, Mathematical Physics, Statistical Physics, Astrophysics, Modern Physics\n\n💼 COMMERCE DEPARTMENT:\n\n• BCom (Bachelor of Commerce)\n  Subjects: Financial Accounting, Cost Accounting, Management Accounting, Business Law, Corporate Law, Income Tax, Banking & Insurance, Business Statistics, Business Mathematics, Marketing Management, Human Resource Management, Entrepreneurship\n\n📊 BUSINESS DEPARTMENT:\n\n• BBA (Bachelor of Business Administration)\n  Subjects: Principles of Management, Marketing Management, Financial Management, Human Resource Management, Operations Management, Business Statistics, Business Law, Organizational Behavior, Strategic Management, Entrepreneurship, International Business, Business Communication\n\n• CA (Chartered Accountancy)\n  Subjects: Financial Accounting, Cost Accounting, Management Accounting, Auditing, Taxation, Corporate Law, Business Law, Financial Management, Information Technology, Economics, Business Mathematics, Statistics\n\nFor admission details, contact: 6381706363'
        },
        'fee': {
            'keywords': ['fee', 'fees', 'cost', 'price', 'tuition', 'payment'],
            'response': 'Our semester fee is ₹12,000 per semester. For detailed fee information and payment options, please contact the college office.'
        },
        'admission': {
            'keywords': ['admission', 'admit', 'apply', 'application', 'enroll', 'enrollment'],
            'response': 'Admissions are open! You can apply online through our website or visit the admissions office. Required documents include 10th and 12th mark sheets, ID proof, and passport photos. Application deadline is usually in May.'
        },
        'timing': {
            'keywords': ['time', 'timing', 'schedule', 'hours', 'when', 'open'],
            'response': 'College timings are Monday to Friday, 9:30 AM to 3:30 PM. Office hours are 9:30 AM to 3:30 PM.'
        },
        'contact': {
            'keywords': ['contact', 'phone', 'email', 'address', 'location', 'where'],
            'response': 'You can contact us at:\nPhone: 6381706363\nEmail: akashadhithyan11707@gmail.com\nAddress: Sedharapet, Vannur, Tamil Nadu\nOffice Hours: 9:30 AM - 3:30 PM (Mon-Fri)'
        },
        'greeting': {
            'keywords': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'response': 'Hello! Welcome to Sri Aravindhar Arts and Science College Chatbot.\n\nWe offer 3-year degree programs with 6 semesters across multiple departments.\n\nHow can I help you today? I can assist with:\n- Courses and subjects (7-8+ subjects per course)\n- Fees (₹12,000 per semester)\n- Admissions\n- Timings (9:30 AM - 3:30 PM)\n- Contact Information'
        },
        'college': {
            'keywords': ['college', 'name', 'institution', 'university'],
            'response': 'Sri Aravindhar Arts and Science College, affiliated to Annamalai University.\n\n📍 Location: Sedharapet, Vannur, Tamil Nadu\n\n📅 Duration: All courses are 3-year programs\n\n📚 Semesters: 6 semesters (2 semesters per year)\n\n🎓 Programs Offered:\n- BCA, BSc CS, BSc Maths, BSc Chemistry, BSc Physics\n- BCom, BBA, CA\n\nEach course includes 7-8+ subjects per semester, providing comprehensive education in respective fields.'
        }
    }
    
    # Find matching response
    bot_response = "I'm here to help! Sri Aravindhar Arts and Science College offers 3-year programs with 6 semesters.\n\nYou can ask me about:\n- Courses and Subjects (7-8+ subjects per course)\n- Fees (₹12,000 per semester)\n- Admissions\n- Timings (9:30 AM - 3:30 PM)\n- Contact Information\n- College Name\n\nWhat would you like to know?"
    
    for category, data in responses.items():
        if any(keyword in user_message for keyword in data['keywords']):
            bot_response = data['response']
            break
    
    return jsonify({'response': bot_response})

@app.route('/student/chatbot')
def student_chatbot():
    """Student chatbot page (requires login)"""
    if 'user_id' not in session or session['role'] != 'student':
        flash('Please login to access chatbot', 'error')
        return redirect(url_for('login'))
    return render_template('student_chatbot.html', is_public=False)

@app.route('/student/chatbot/message', methods=['POST'])
def student_chatbot_message():
    """Handle student chatbot messages (requires login)"""
    if 'user_id' not in session or session['role'] != 'student':
        return jsonify({'error': 'Access denied'}), 403
    
    user_message = request.json.get('message', '').strip().lower()
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', (session['user_id'],)
    ).fetchone()
    conn.close()
    
    # Parse student data
    marks = {}
    arrears = []
    subjects = []
    chatbot_questions = []
    
    if user['semester_marks']:
        try:
            marks = json.loads(user['semester_marks']) if user['semester_marks'] else {}
        except:
            marks = {}
    
    if user['arrears']:
        try:
            arrears = json.loads(user['arrears']) if user['arrears'] else []
        except:
            arrears = []
    
    if user['subjects']:
        try:
            subjects = json.loads(user['subjects']) if user['subjects'] else []
        except:
            subjects = []
    
    if user['chatbot_questions']:
        try:
            chatbot_questions = json.loads(user['chatbot_questions']) if user['chatbot_questions'] else []
        except:
            chatbot_questions = []
    
    # Check custom chatbot questions first
    for qa in chatbot_questions:
        if isinstance(qa, dict) and 'question' in qa and 'answer' in qa:
            question_lower = qa['question'].lower()
            if question_lower in user_message or user_message in question_lower:
                return jsonify({'response': qa['answer']})
    
    # Check for marks-related queries
    marks_keywords = ['mark', 'grade', 'score', 'semester', 'cgpa', 'percentage', 'result']
    if any(keyword in user_message for keyword in marks_keywords):
        if marks:
            response = "Here are your semester marks:\n\n"
            for semester, subjects_data in sorted(marks.items()):
                if isinstance(subjects_data, dict):
                    response += f"📚 Semester {semester}:\n"
                    for subject, mark in subjects_data.items():
                        response += f"  • {subject}: {mark}\n"
                    response += "\n"
                else:
                    # Legacy format support
                    response += f"Semester {semester}: {subjects_data}\n"
            return jsonify({'response': response})
        else:
            return jsonify({'response': "No marks available yet. Please contact your teacher for updates."})
    
    # Check for arrears-related queries
    arrears_keywords = ['arrear', 'backlog', 'failed', 'clear', 'clearance']
    if any(keyword in user_message for keyword in arrears_keywords):
        if arrears:
            response = "Here is your arrears status:\n\n"
            for arrear in arrears:
                if isinstance(arrear, dict):
                    subject = arrear.get('subject', 'Unknown')
                    status = arrear.get('status', 'Unknown')
                    response += f"{subject}: {status}\n"
            return jsonify({'response': response})
        else:
            return jsonify({'response': "✅ Great news! You have no arrears."})
    
    # Check for subjects-related queries
    subjects_keywords = ['subject', 'subjects', 'course', 'courses']
    if any(keyword in user_message for keyword in subjects_keywords):
        if subjects:
            response = "Your subjects are:\n\n"
            for i, subject in enumerate(subjects, 1):
                response += f"{i}. {subject}\n"
            return jsonify({'response': response})
        else:
            return jsonify({'response': "No subjects registered yet. Please contact your teacher."})
    
    # Default response
    default_response = f"Hello {user['name'] or 'Student'}! I can help you with:\n- Your marks and grades\n- Arrears status\n- Your subjects\n- Custom questions set by your teacher\n\nWhat would you like to know?"
    return jsonify({'response': default_response})

@app.route('/profile')
def profile():
    """Profile page"""
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    try:
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE id = ?', (session['user_id'],)
        ).fetchone()
        conn.close()
        
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('login'))
        
        # Parse JSON fields safely
        subjects = []
        parent_details = {}
        
        if user['subjects']:
            try:
                subjects = json.loads(user['subjects']) if user['subjects'] else []
            except:
                subjects = []
        
        if user['parent_details']:
            try:
                parent_details = json.loads(user['parent_details']) if user['parent_details'] else {}
            except:
                parent_details = {}
        
        return render_template('profile.html', user=user, subjects=subjects, parent_details=parent_details)
    except Exception as e:
        flash(f'Error loading profile: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route('/about')
def about():
    """About college page (public access)"""
    return render_template('about.html', is_public=True)

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# Teacher routes for student management
@app.route('/teacher/add-student', methods=['POST'])
def add_student():
    """Add new student (teacher only)"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    email_phone = request.form.get('email_phone', '').strip()
    password = request.form.get('password', '')
    name = request.form.get('name', '').strip()
    roll_number = request.form.get('roll_number', '').strip()
    department = request.form.get('department', '').strip()
    photo = request.files.get('photo')
    
    if not email_phone or not password:
        return jsonify({'error': 'Email/Phone and Password are required'}), 400
    
    if not (is_valid_email(email_phone) or is_valid_phone(email_phone)):
        return jsonify({'error': 'Invalid email or phone format'}), 400
    
    conn = get_db_connection()
    existing = conn.execute(
        'SELECT id FROM users WHERE email_phone = ?', (email_phone,)
    ).fetchone()
    
    if existing:
        conn.close()
        return jsonify({'error': 'Email/Phone already exists'}), 400
    
    photo_path = None
    if photo and photo.filename:
        if allowed_file(photo.filename):
            filename = secure_filename(f"{email_phone}_{photo.filename}")
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
            photo_path = f"images/{filename}"
    
    hashed_password = generate_password_hash(password)
    
    try:
        conn.execute('''
            INSERT INTO users (email_phone, password, role, name, roll_number, department, photo_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (email_phone, hashed_password, 'student', name, roll_number, department, photo_path))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Student added successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/teacher/edit-student/<int:student_id>', methods=['POST'])
def edit_student(student_id):
    """Edit student details (teacher only)"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        name = request.form.get('name', '').strip()
        roll_number = request.form.get('roll_number', '').strip()
        department = request.form.get('department', '').strip()
        age = request.form.get('age', '').strip()
        blood_group = request.form.get('blood_group', '').strip()
        
        # Parse parent details
        parent_name = request.form.get('parent_name', '').strip()
        parent_phone = request.form.get('parent_phone', '').strip()
        parent_email = request.form.get('parent_email', '').strip()
        parent_relationship = request.form.get('parent_relationship', '').strip()
        
        parent_details = {}
        if parent_name or parent_phone or parent_email or parent_relationship:
            parent_details = {
                'name': parent_name,
                'phone': parent_phone,
                'email': parent_email,
                'relationship': parent_relationship
            }
        parent_details_json = json.dumps(parent_details) if parent_details else None
        
        # Parse subjects
        subjects_str = request.form.get('subjects', '').strip()
        subjects = []
        if subjects_str:
            subjects = [s.strip() for s in subjects_str.split(',') if s.strip()]
        subjects_json = json.dumps(subjects) if subjects else None
        
        # Convert age to integer if provided
        age_int = None
        if age:
            try:
                age_int = int(age)
            except ValueError:
                age_int = None
        
        conn = get_db_connection()
        try:
            # Verify student exists
            student = conn.execute('SELECT id FROM users WHERE id = ? AND role = ?', (student_id, 'student')).fetchone()
            if not student:
                conn.close()
                return jsonify({'error': 'Student not found'}), 404
            
            conn.execute('''
                UPDATE users SET name = ?, roll_number = ?, department = ?, age = ?, 
                blood_group = ?, parent_details = ?, subjects = ?
                WHERE id = ? AND role = ?
            ''', (name, roll_number, department, age_int, blood_group, parent_details_json, subjects_json, student_id, 'student'))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Student updated successfully'})
        except sqlite3.Error as e:
            conn.close()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/teacher/reset-password/<int:student_id>', methods=['POST'])
def reset_password(student_id):
    """Reset student password (teacher only)"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    new_password = request.form.get('password', '')
    
    if not new_password:
        return jsonify({'error': 'Password is required'}), 400
    
    conn = get_db_connection()
    try:
        hashed_password = generate_password_hash(new_password)
        conn.execute('''
            UPDATE users SET password = ? WHERE id = ? AND role = ?
        ''', (hashed_password, student_id, 'student'))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Password reset successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/teacher/delete-student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """Delete student (teacher only)"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    conn = get_db_connection()
    try:
        # Get photo path to delete file
        student = conn.execute('SELECT photo_path FROM users WHERE id = ?', (student_id,)).fetchone()
        if student and student['photo_path']:
            photo_file = os.path.join('static', student['photo_path'])
            if os.path.exists(photo_file):
                os.remove(photo_file)
        
        conn.execute('DELETE FROM users WHERE id = ? AND role = ?', (student_id, 'student'))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Student deleted successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/teacher/update-marks/<int:student_id>', methods=['POST'])
def update_marks(student_id):
    """Update student semester marks (teacher only)"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    semester = request.form.get('semester', '').strip()
    subject = request.form.get('subject', '').strip()
    marks = request.form.get('marks', '').strip()
    
    if not semester or not marks or not subject:
        return jsonify({'error': 'Semester, subject, and marks are required'}), 400
    
    conn = get_db_connection()
    try:
        student = conn.execute('SELECT semester_marks FROM users WHERE id = ?', (student_id,)).fetchone()
        current_marks = {}
        if student and student['semester_marks']:
            try:
                current_marks = json.loads(student['semester_marks']) if student['semester_marks'] else {}
            except:
                current_marks = {}
        
        # Structure: {semester: {subject: marks}}
        if semester not in current_marks:
            current_marks[semester] = {}
        current_marks[semester][subject] = marks
        marks_json = json.dumps(current_marks)
        
        conn.execute('''
            UPDATE users SET semester_marks = ? WHERE id = ? AND role = ?
        ''', (marks_json, student_id, 'student'))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Marks updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/teacher/update-arrears/<int:student_id>', methods=['POST'])
def update_arrears(student_id):
    """Update student arrears (teacher only)"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    subject = request.form.get('subject', '').strip()
    status = request.form.get('status', '').strip()
    
    if not subject:
        return jsonify({'error': 'Subject is required'}), 400
    
    conn = get_db_connection()
    try:
        student = conn.execute('SELECT arrears FROM users WHERE id = ?', (student_id,)).fetchone()
        current_arrears = []
        if student and student['arrears']:
            try:
                current_arrears = json.loads(student['arrears']) if student['arrears'] else []
            except:
                current_arrears = []
        
        # Remove existing entry for this subject if exists
        current_arrears = [a for a in current_arrears if a.get('subject') != subject]
        
        # Add new entry
        current_arrears.append({'subject': subject, 'status': status})
        arrears_json = json.dumps(current_arrears)
        
        conn.execute('''
            UPDATE users SET arrears = ? WHERE id = ? AND role = ?
        ''', (arrears_json, student_id, 'student'))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Arrears updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/teacher/update-notes-link/<int:student_id>', methods=['POST'])
def update_notes_link(student_id):
    """Update student notes link (teacher only)"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    notes_link = request.form.get('notes_link', '').strip()
    
    conn = get_db_connection()
    try:
        conn.execute('''
            UPDATE users SET notes_link = ? WHERE id = ? AND role = ?
        ''', (notes_link, student_id, 'student'))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Notes link updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/teacher/update-subject-notes/<int:student_id>', methods=['POST'])
def update_subject_notes(student_id):
    """Update subject-wise notes for student (teacher only)"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    subject = request.form.get('subject', '').strip()
    notes_link = request.form.get('notes_link', '').strip()
    
    if not subject or not notes_link:
        return jsonify({'error': 'Subject and notes link are required'}), 400
    
    conn = get_db_connection()
    try:
        student = conn.execute('SELECT subject_notes FROM users WHERE id = ?', (student_id,)).fetchone()
        current_notes = {}
        if student and student['subject_notes']:
            try:
                current_notes = json.loads(student['subject_notes']) if student['subject_notes'] else {}
            except:
                current_notes = {}
        
        current_notes[subject] = notes_link
        notes_json = json.dumps(current_notes)
        
        conn.execute('''
            UPDATE users SET subject_notes = ? WHERE id = ? AND role = ?
        ''', (notes_json, student_id, 'student'))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Subject notes updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/teacher/update-chatbot-questions/<int:student_id>', methods=['POST'])
def update_chatbot_questions(student_id):
    """Update chatbot questions for student (teacher only)"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    questions_json = request.form.get('questions', '').strip()
    
    if not questions_json:
        return jsonify({'error': 'Questions data is required'}), 400
    
    try:
        # Validate JSON format
        questions = json.loads(questions_json)
        if not isinstance(questions, list):
            return jsonify({'error': 'Questions must be an array'}), 400
        
        # Validate each question has question and answer
        for qa in questions:
            if not isinstance(qa, dict) or 'question' not in qa or 'answer' not in qa:
                return jsonify({'error': 'Each question must have "question" and "answer" fields'}), 400
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format'}), 400
    
    conn = get_db_connection()
    try:
        conn.execute('''
            UPDATE users SET chatbot_questions = ? WHERE id = ? AND role = ?
        ''', (questions_json, student_id, 'student'))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Chatbot questions updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/teacher/get-chatbot-questions/<int:student_id>', methods=['GET'])
def get_chatbot_questions(student_id):
    """Get chatbot questions for student (teacher only)"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        conn = get_db_connection()
        student = conn.execute('SELECT chatbot_questions FROM users WHERE id = ?', (student_id,)).fetchone()
        conn.close()
        
        if student and student['chatbot_questions']:
            try:
                questions = json.loads(student['chatbot_questions'])
                return jsonify({'success': True, 'questions': questions})
            except json.JSONDecodeError:
                return jsonify({'success': True, 'questions': []})
        else:
            return jsonify({'success': True, 'questions': []})
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# Teacher profile editing routes
@app.route('/teacher/edit-profile', methods=['GET', 'POST'])
def edit_teacher_profile():
    """Edit teacher profile"""
    if 'user_id' not in session or session['role'] != 'teacher':
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            department = request.form.get('department', '').strip()
            age = request.form.get('age', '').strip()
            blood_group = request.form.get('blood_group', '').strip()
            
            # Convert age to integer if provided
            age_int = None
            if age:
                try:
                    age_int = int(age)
                except ValueError:
                    age_int = None
            
            conn = get_db_connection()
            try:
                conn.execute('''
                    UPDATE users SET name = ?, department = ?, age = ?, blood_group = ?
                    WHERE id = ? AND role = ?
                ''', (name, department, age_int, blood_group, session['user_id'], 'teacher'))
                conn.commit()
                conn.close()
                
                # Update session
                session['name'] = name
                
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('profile'))
            except sqlite3.Error as e:
                conn.close()
                flash(f'Database error: {str(e)}', 'error')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
    
    # GET request - show edit form
    try:
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE id = ? AND role = ?', (session['user_id'], 'teacher')
        ).fetchone()
        conn.close()
        
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('login'))
        
        return render_template('edit_teacher_profile.html', user=user)
    except Exception as e:
        flash(f'Error loading profile: {str(e)}', 'error')
        return redirect(url_for('profile'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error='Internal server error. Please try again later.'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error (in production, use proper logging)
    print(f"Error: {str(e)}")
    return jsonify({'error': 'An error occurred. Please try again.'}), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
