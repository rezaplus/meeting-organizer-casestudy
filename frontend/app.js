document.getElementById('meeting-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    let meetingId = document.getElementById('meeting-id').value;
    let meeting = {
        subject: document.getElementById('subject').value,
        date: document.getElementById('date').value,
        start_time: document.getElementById('start-time').value,
        end_time: document.getElementById('end-time').value,
        participants: document.getElementById('participants').value
    };

    if (meetingId) {
        fetch(`http://localhost:5000/api/meetings/${meetingId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(meeting)
        })
        .then(response => response.json())
        .then(data => {
            loadMeetings();
            clearForm();
        });
    } else {
        fetch('http://localhost:5000/api/meetings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(meeting)
        })
        .then(response => response.json())
        .then(data => {
            loadMeetings();
            clearForm();
        });
    }
});

function loadMeetings() {
    fetch('http://localhost:5000/api/meetings')
    .then(response => response.json())
    .then(meetings => {
        let meetingList = document.getElementById('meeting-list');
        meetingList.innerHTML = '';
        meetings.forEach(meeting => {
            let li = document.createElement('li');
            li.className = 'list-group-item';
            li.innerHTML = `
                ${meeting.subject} - ${meeting.date} - ${meeting.start_time} to ${meeting.end_time} - ${meeting.participants}
                <button class="btn btn-warning btn-sm ms-2" onclick="editMeeting('${meeting._id}')">Edit</button>
                <button class="btn btn-danger btn-sm ms-2" onclick="deleteMeeting('${meeting._id}')">Delete</button>
            `;
            meetingList.appendChild(li);
        });
    });
}

function editMeeting(id) {
    fetch(`http://localhost:5000/api/meetings/${id}`)
    .then(response => response.json())
    .then(meeting => {
        document.getElementById('meeting-id').value = meeting._id;
        document.getElementById('subject').value = meeting.subject;
        document.getElementById('date').value = meeting.date;
        document.getElementById('start-time').value = meeting.start_time;
        document.getElementById('end-time').value = meeting.end_time;
        document.getElementById('participants').value = meeting.participants;
    });
}

function deleteMeeting(id) {
    fetch(`http://localhost:5000/api/meetings/${id}`, {
        method: 'DELETE'
    })
    .then(() => {
        loadMeetings();
    });
}

function clearForm() {
    document.getElementById('meeting-id').value = '';
    document.getElementById('subject').value = '';
    document.getElementById('date').value = '';
    document.getElementById('start-time').value = '';
    document.getElementById('end-time').value = '';
    document.getElementById('participants').value = '';
}

loadMeetings();
