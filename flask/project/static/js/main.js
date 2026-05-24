// ── Modal ─────────────────────────────────────────────────────────────────────

function openModal() {
    document.getElementById('modal-title').textContent = 'Add Student';
    document.getElementById('student-form').action = '/add';
    document.getElementById('student-form').reset();
    document.getElementById('modal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('modal').classList.add('hidden');
}

function loadEdit(id) {
    fetch(`/edit/${id}`)
        .then(r => r.json())
        .then(d => {
            document.getElementById('modal-title').textContent = 'Edit Student';
            document.getElementById('student-form').action = `/update/${id}`;
            document.getElementById('name').value    = d.name    || '';
            document.getElementById('email').value   = d.email   || '';
            document.getElementById('phone').value   = d.phone   || '';
            document.getElementById('age').value     = d.age     || '';
            document.getElementById('grade').value   = d.grade   || '';
            document.getElementById('subject').value = d.subject || '';
            document.getElementById('modal').classList.remove('hidden');
        });
}

window.addEventListener('click', e => {
    if (e.target === document.getElementById('modal')) closeModal();
});

// ── View Profile Panel ────────────────────────────────────────────────────────

function viewStudent(id) {
    fetch(`/view/${id}`)
        .then(r => r.json())
        .then(d => {
            document.getElementById('panel-avatar').textContent = d.name[0].toUpperCase();
            document.getElementById('panel-body').innerHTML = `
                <div class="panel-row"><span>Name</span>    <span>${d.name}</span></div>
                <div class="panel-row"><span>Email</span>   <span>${d.email}</span></div>
                <div class="panel-row"><span>Phone</span>   <span>${d.phone || '—'}</span></div>
                <div class="panel-row"><span>Age</span>     <span>${d.age}</span></div>
                <div class="panel-row"><span>Grade</span>   <span>${d.grade}</span></div>
                <div class="panel-row"><span>Subject</span> <span>${d.subject || '—'}</span></div>
                <div class="panel-row"><span>Enrolled</span><span>${d.created_at ? d.created_at.slice(0,10) : '—'}</span></div>
            `;
            document.getElementById('view-panel').classList.remove('hidden');
            document.getElementById('panel-overlay').classList.remove('hidden');
        });
}

function closePanel() {
    document.getElementById('view-panel').classList.add('hidden');
    document.getElementById('panel-overlay').classList.add('hidden');
}

// ── Auto-dismiss toasts ───────────────────────────────────────────────────────

document.querySelectorAll('.toast').forEach(t => {
    setTimeout(() => t.remove(), 4000);
});
