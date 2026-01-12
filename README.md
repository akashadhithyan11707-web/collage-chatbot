# College Chatbot Web Application

A modern, full-stack web application for college enquiries with role-based authentication, student management, and an AI-powered chatbot.

## 🚀 Features

### Authentication System
- **Login**: Email (Gmail) or Phone Number + Password
- **Registration**: Role-based (Student/Teacher)
- **Secure Password Storage**: Passwords are hashed using Werkzeug
- **Session Management**: Secure session handling

### Student Dashboard
- View profile with photo
- Access chatbot for college enquiries
- View personal information (Roll number, Department)
- Profile page (read-only)

### Teacher Dashboard
- **Student Management**:
  - View all students in a table
  - Add new students
  - Edit student details
  - Delete students
  - Reset student passwords
- Full CRUD operations for student data

### Chatbot System
- **Student-only access** to chatbot
- **College Enquiry Topics**:
  - Courses and Programs
  - Fee Structure
  - Admission Process
  - College Timings
  - Contact Information
- Modern chat UI with:
  - Message bubbles
  - Typing animation
  - Auto-scroll
  - Quick question buttons

### UI/UX Features
- Modern, responsive design
- Smooth animations and transitions
- Loading states
- Flash messages for notifications
- Hover effects
- Mobile-friendly layout

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **Database**: SQLite
- **Authentication**: Session-based with password hashing

## 📁 Project Structure

```
CollegeChatbot/
│
├── app.py                 # Flask backend application
├── college.db            # SQLite database (created automatically)
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore file
│
├── static/              # Static files
│   ├── css/
│   │   └── style.css    # Main stylesheet with animations
│   ├── js/
│   │   ├── main.js      # Common JavaScript functions
│   │   ├── chatbot.js   # Chatbot functionality
│   │   └── teacher.js   # Teacher dashboard functions
│   └── images/          # Uploaded student photos
│
└── templates/           # HTML templates
    ├── login.html       # Login page
    ├── register.html    # Registration page
    ├── student_dashboard.html
    ├── teacher_dashboard.html
    ├── chatbot.html     # Chatbot interface
    ├── profile.html     # User profile page
    └── about.html       # About college page
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+** (Check with `python --version`)
- **pip** (Python package installer)
- **Git** (for version control)
- **VS Code** (recommended IDE)

## 🔧 Installation & Setup

### Step 1: Clone or Navigate to Project Directory

```bash
cd "C:\Users\apadt\.cursor\plans\college chatbot"
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# On Windows CMD:
venv\Scripts\activate.bat

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- Werkzeug 3.0.1

### Step 4: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000` or `http://127.0.0.1:5000`

### Step 5: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## 👤 Creating Your First Account

### Register as Teacher (Recommended First Step)

1. Go to `http://localhost:5000/register`
2. Select **Role: Teacher**
3. Enter:
   - Email or Phone Number (e.g., `teacher@college.edu` or `1234567890`)
   - Password (minimum 6 characters)
4. Click **Register**
5. Login with your credentials

### Register as Student

1. Go to `http://localhost:5000/register`
2. Select **Role: Student**
3. Fill in:
   - Email or Phone Number
   - Password
   - Full Name (optional)
   - Roll Number (optional)
   - Department (optional)
   - Student Photo (optional - PNG, JPG, JPEG)
4. Click **Register**
5. Login to access student dashboard and chatbot

### Teacher Can Add Students

1. Login as Teacher
2. Click **+ Add Student** button
3. Fill in student details
4. Upload photo (optional)
5. Click **Add Student**

## 🎯 Usage Guide

### For Students

1. **Login** → Access Student Dashboard
2. **View Dashboard** → See your profile summary
3. **Open Chatbot** → Ask questions about:
   - Courses
   - Fees
   - Admissions
   - Timings
   - Contact Information
4. **View Profile** → See your details (read-only)
5. **About** → Learn about the college

### For Teachers

1. **Login** → Access Teacher Dashboard
2. **View Students** → See all registered students
3. **Add Student** → Create new student accounts
4. **Edit Student** → Update student information
5. **Reset Password** → Change student password
6. **Delete Student** → Remove student account

## 🔒 Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control
- Input validation
- File upload restrictions (image types only, max 16MB)
- SQL injection protection (parameterized queries)

## 🎨 Customization

### Change Colors

Edit `static/css/style.css` and modify CSS variables:

```css
:root {
    --primary-color: #4f46e5;  /* Change primary color */
    --secondary-color: #10b981; /* Change secondary color */
    /* ... more variables */
}
```

### Modify Chatbot Responses

Edit the `chatbot_message()` function in `app.py`:

```python
responses = {
    'course': {
        'keywords': [...],
        'response': 'Your custom response here'
    },
    # Add more responses
}
```

### Change College Information

Edit `templates/about.html` to update college details.

## 🐛 Troubleshooting

### Port Already in Use

If port 5000 is busy, edit `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port
```

### Database Issues

Delete `college.db` and restart the app to recreate the database.

### Photo Upload Not Working

- Ensure `static/images/` folder exists
- Check file permissions
- Verify file size is under 16MB
- Ensure file type is PNG, JPG, or JPEG

### Module Not Found Error

```bash
pip install -r requirements.txt
```

### Virtual Environment Issues

```bash
# Deactivate current environment
deactivate

# Remove and recreate
rm -rf venv  # On Windows: rmdir /s venv
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

## 📝 Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary Key |
| email_phone | TEXT | Unique login identifier |
| password | TEXT | Hashed password |
| role | TEXT | 'student' or 'teacher' |
| name | TEXT | Full name |
| roll_number | TEXT | Student roll number |
| department | TEXT | Department name |
| photo_path | TEXT | Path to uploaded photo |
| created_at | TIMESTAMP | Registration date |

## 🚀 Deployment

### For Production:

1. Change `app.secret_key` in `app.py` to a secure random string
2. Set `debug=False` in `app.run()`
3. Use a production WSGI server (e.g., Gunicorn)
4. Configure proper database backups
5. Set up HTTPS/SSL

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests!

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Check Flask documentation: https://flask.palletsprojects.com/

## 🎓 Learning Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLite Tutorial: https://www.sqlitetutorial.net/
- JavaScript MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript

---

**Built with ❤️ for College Management**

Happy Coding! 🚀
