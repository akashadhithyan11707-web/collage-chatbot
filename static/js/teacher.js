/**
 * Teacher Dashboard JavaScript
 * Handles student management operations
 */

// Modal functions
function openAddStudentModal() {
    document.getElementById('addStudentModal').classList.add('show');
    document.getElementById('addStudentForm').reset();
}

function closeAddStudentModal() {
    document.getElementById('addStudentModal').classList.remove('show');
}

function openEditModal(studentId, name, rollNumber, department, age, bloodGroup, subjects, parentDetails) {
    document.getElementById('editStudentId').value = studentId;
    document.getElementById('editName').value = name || '';
    document.getElementById('editRollNumber').value = rollNumber || '';
    document.getElementById('editDepartment').value = department || '';
    document.getElementById('editAge').value = age || '';
    document.getElementById('editBloodGroup').value = bloodGroup || '';
    
    // Handle subjects
    if (subjects && Array.isArray(subjects) && subjects.length > 0) {
        document.getElementById('editSubjects').value = subjects.join(', ');
    } else {
        document.getElementById('editSubjects').value = '';
    }
    
    // Handle parent details
    if (parentDetails && typeof parentDetails === 'object') {
        document.getElementById('editParentName').value = parentDetails.name || '';
        document.getElementById('editParentRelationship').value = parentDetails.relationship || '';
        document.getElementById('editParentPhone').value = parentDetails.phone || '';
        document.getElementById('editParentEmail').value = parentDetails.email || '';
    } else {
        document.getElementById('editParentName').value = '';
        document.getElementById('editParentRelationship').value = '';
        document.getElementById('editParentPhone').value = '';
        document.getElementById('editParentEmail').value = '';
    }
    
    document.getElementById('editStudentModal').classList.add('show');
}

function openEditModalWithData(studentId, studentData) {
    let subjects = [];
    let parentDetails = {};
    
    try {
        if (studentData.subjects) {
            if (typeof studentData.subjects === 'string') {
                subjects = JSON.parse(studentData.subjects);
            } else {
                subjects = studentData.subjects;
            }
        }
    } catch (e) {
        subjects = [];
    }
    
    try {
        if (studentData.parent_details) {
            if (typeof studentData.parent_details === 'string') {
                parentDetails = JSON.parse(studentData.parent_details);
            } else {
                parentDetails = studentData.parent_details;
            }
        }
    } catch (e) {
        parentDetails = {};
    }
    
    openEditModal(
        studentId,
        studentData.name || '',
        studentData.roll_number || '',
        studentData.department || '',
        studentData.age || null,
        studentData.blood_group || '',
        subjects,
        parentDetails
    );
}

function closeEditModal() {
    document.getElementById('editStudentModal').classList.remove('show');
}

function openResetPasswordModal(studentId) {
    document.getElementById('resetStudentId').value = studentId;
    document.getElementById('resetPassword').value = '';
    document.getElementById('resetPasswordModal').classList.add('show');
}

function closeResetPasswordModal() {
    document.getElementById('resetPasswordModal').classList.remove('show');
}

function openMarksModal(studentId) {
    document.getElementById('marksStudentId').value = studentId;
    document.getElementById('marksSemester').value = '';
    document.getElementById('marksSubject').value = '';
    document.getElementById('marksValue').value = '';
    document.getElementById('updateMarksModal').classList.add('show');
}

function closeMarksModal() {
    document.getElementById('updateMarksModal').classList.remove('show');
}

function openArrearsModal(studentId) {
    document.getElementById('arrearsStudentId').value = studentId;
    document.getElementById('arrearsSubject').value = '';
    document.getElementById('arrearsStatus').value = '';
    document.getElementById('updateArrearsModal').classList.add('show');
}

function closeArrearsModal() {
    document.getElementById('updateArrearsModal').classList.remove('show');
}

function openSubjectNotesModal(studentId) {
    document.getElementById('subjectNotesStudentId').value = studentId;
    document.getElementById('subjectName').value = '';
    document.getElementById('subjectNotesLink').value = '';
    document.getElementById('updateSubjectNotesModal').classList.add('show');
}

function closeSubjectNotesModal() {
    document.getElementById('updateSubjectNotesModal').classList.remove('show');
}

function openNotesLinkModal(studentId, currentLink) {
    document.getElementById('notesStudentId').value = studentId;
    document.getElementById('notesLink').value = currentLink || '';
    document.getElementById('updateNotesLinkModal').classList.add('show');
}

function closeNotesLinkModal() {
    document.getElementById('updateNotesLinkModal').classList.remove('show');
}

function openChatbotQuestionsModal(studentId) {
    document.getElementById('chatbotQuestionsStudentId').value = studentId;
    document.getElementById('chatbotQuestionsContainer').innerHTML = '';
    document.getElementById('chatbotQuestionsModal').classList.add('show');
    
    // Load existing questions
    loadChatbotQuestions(studentId);
}

function closeChatbotQuestionsModal() {
    document.getElementById('chatbotQuestionsModal').classList.remove('show');
}

async function loadChatbotQuestions(studentId) {
    try {
        const response = await fetch(`/teacher/get-chatbot-questions/${studentId}`);
        const data = await response.json();
        
        if (data.success && data.questions && data.questions.length > 0) {
            data.questions.forEach((qa, index) => {
                addChatbotQuestionRow(qa.question || '', qa.answer || '');
            });
        } else {
            addChatbotQuestionRow('', '');
        }
    } catch (error) {
        console.error('Error loading chatbot questions:', error);
        addChatbotQuestionRow('', '');
    }
}

function addChatbotQuestion(question = '', answer = '') {
    addChatbotQuestionRow(question, answer);
}

function addChatbotQuestionRow(question = '', answer = '') {
    const container = document.getElementById('chatbotQuestionsContainer');
    const questionIndex = container.children.length;
    
    const questionDiv = document.createElement('div');
    questionDiv.className = 'form-group';
    questionDiv.style.border = '1px solid #ddd';
    questionDiv.style.padding = '15px';
    questionDiv.style.marginBottom = '15px';
    questionDiv.style.borderRadius = '5px';
    questionDiv.style.backgroundColor = '#f9f9f9';
    
    questionDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <strong>Question ${questionIndex + 1}</strong>
            <button type="button" class="btn btn-danger" onclick="removeChatbotQuestion(this)" style="padding: 5px 10px; font-size: 12px;">Remove</button>
        </div>
        <div class="form-group">
            <label>Question *</label>
            <input type="text" class="chatbot-question-input" placeholder="Enter question..." value="${escapeHtml(question)}" required>
        </div>
        <div class="form-group">
            <label>Answer *</label>
            <textarea class="chatbot-answer-input" placeholder="Enter answer..." rows="3" required>${escapeHtml(answer)}</textarea>
        </div>
    `;
    
    container.appendChild(questionDiv);
}

function removeChatbotQuestion(button) {
    if (document.getElementById('chatbotQuestionsContainer').children.length > 1) {
        button.closest('.form-group').remove();
        updateQuestionNumbers();
    } else {
        alert('You must have at least one question.');
    }
}

function updateQuestionNumbers() {
    const container = document.getElementById('chatbotQuestionsContainer');
    Array.from(container.children).forEach((div, index) => {
        const strong = div.querySelector('strong');
        if (strong) {
            strong.textContent = `Question ${index + 1}`;
        }
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Close modals when clicking outside
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.classList.remove('show');
        }
    });
}

// Add Student
document.getElementById('addStudentForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading"></span> Adding...';
    
    try {
        const response = await fetch('/teacher/add-student', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showNotification('Student added successfully!', 'success');
            closeAddStudentModal();
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to add student', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    } catch (error) {
        showNotification('An error occurred. Please try again.', 'error');
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
});

// Edit Student
document.getElementById('editStudentForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const studentId = document.getElementById('editStudentId').value;
    const formData = new FormData(this);
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading"></span> Updating...';
    
    try {
        const response = await fetch(`/teacher/edit-student/${studentId}`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showNotification('Student updated successfully!', 'success');
            closeEditModal();
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to update student', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    } catch (error) {
        showNotification('An error occurred. Please try again.', 'error');
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
});

// Reset Password
document.getElementById('resetPasswordForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const studentId = document.getElementById('resetStudentId').value;
    const formData = new FormData(this);
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading"></span> Resetting...';
    
    try {
        const response = await fetch(`/teacher/reset-password/${studentId}`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showNotification('Password reset successfully!', 'success');
            closeResetPasswordModal();
        } else {
            showNotification(data.error || 'Failed to reset password', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    } catch (error) {
        showNotification('An error occurred. Please try again.', 'error');
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
});

// Delete Student
async function deleteStudent(studentId) {
    if (!confirm('Are you sure you want to delete this student? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`/teacher/delete-student/${studentId}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showNotification('Student deleted successfully!', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(data.error || 'Failed to delete student', 'error');
        }
    } catch (error) {
        showNotification('An error occurred. Please try again.', 'error');
    }
}

// Update Marks
if (document.getElementById('updateMarksForm')) {
    document.getElementById('updateMarksForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const studentId = document.getElementById('marksStudentId').value;
        const formData = new FormData(this);
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> Updating...';
        
        try {
            const response = await fetch(`/teacher/update-marks/${studentId}`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                showNotification('Marks updated successfully!', 'success');
                closeMarksModal();
                setTimeout(() => location.reload(), 1000);
            } else {
                showNotification(data.error || 'Failed to update marks', 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        } catch (error) {
            showNotification('An error occurred. Please try again.', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

// Update Arrears
if (document.getElementById('updateArrearsForm')) {
    document.getElementById('updateArrearsForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const studentId = document.getElementById('arrearsStudentId').value;
        const formData = new FormData(this);
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> Updating...';
        
        try {
            const response = await fetch(`/teacher/update-arrears/${studentId}`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                showNotification('Arrears updated successfully!', 'success');
                closeArrearsModal();
                setTimeout(() => location.reload(), 1000);
            } else {
                showNotification(data.error || 'Failed to update arrears', 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        } catch (error) {
            showNotification('An error occurred. Please try again.', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

// Update Notes Link
if (document.getElementById('updateNotesLinkForm')) {
    document.getElementById('updateNotesLinkForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const studentId = document.getElementById('notesStudentId').value;
        const formData = new FormData(this);
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> Updating...';
        
        try {
            const response = await fetch(`/teacher/update-notes-link/${studentId}`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                showNotification('Notes link updated successfully!', 'success');
                closeNotesLinkModal();
                setTimeout(() => location.reload(), 1000);
            } else {
                showNotification(data.error || 'Failed to update notes link', 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        } catch (error) {
            showNotification('An error occurred. Please try again.', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

// Update Subject Notes
if (document.getElementById('updateSubjectNotesForm')) {
    document.getElementById('updateSubjectNotesForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const studentId = document.getElementById('subjectNotesStudentId').value;
        const formData = new FormData(this);
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> Adding...';
        
        try {
            const response = await fetch(`/teacher/update-subject-notes/${studentId}`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                showNotification('Subject notes added successfully!', 'success');
                closeSubjectNotesModal();
                setTimeout(() => location.reload(), 1000);
            } else {
                showNotification(data.error || 'Failed to add subject notes', 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        } catch (error) {
            showNotification('An error occurred. Please try again.', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

// Chatbot Questions Form Handler
if (document.getElementById('chatbotQuestionsForm')) {
    document.getElementById('chatbotQuestionsForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const studentId = document.getElementById('chatbotQuestionsStudentId').value;
        const questionInputs = document.querySelectorAll('.chatbot-question-input');
        const answerInputs = document.querySelectorAll('.chatbot-answer-input');
        
        const questions = [];
        for (let i = 0; i < questionInputs.length; i++) {
            const question = questionInputs[i].value.trim();
            const answer = answerInputs[i].value.trim();
            
            if (question && answer) {
                questions.push({ question: question, answer: answer });
            }
        }
        
        if (questions.length === 0) {
            showNotification('Please add at least one question and answer', 'error');
            return;
        }
        
        const formData = new FormData();
        formData.append('questions', JSON.stringify(questions));
        
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> Saving...';
        
        try {
            const response = await fetch(`/teacher/update-chatbot-questions/${studentId}`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                showNotification('Chatbot questions updated successfully!', 'success');
                closeChatbotQuestionsModal();
            } else {
                showNotification(data.error || 'Failed to update chatbot questions', 'error');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        } catch (error) {
            showNotification('An error occurred. Please try again.', 'error');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

// Show notification function (if not already defined)
if (typeof showNotification === 'undefined') {
    function showNotification(message, type = 'success') {
        const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
        
        const flashMessage = document.createElement('div');
        flashMessage.className = `flash-message flash-${type}`;
        flashMessage.innerHTML = `
            <span>${message}</span>
            <button class="close-flash" onclick="this.parentElement.remove()">&times;</button>
        `;
        
        flashContainer.appendChild(flashMessage);
        
        setTimeout(() => {
            flashMessage.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => flashMessage.remove(), 300);
        }, 5000);
    }
    
    function createFlashContainer() {
        const container = document.createElement('div');
        container.className = 'flash-messages';
        document.body.appendChild(container);
        return container;
    }
}
