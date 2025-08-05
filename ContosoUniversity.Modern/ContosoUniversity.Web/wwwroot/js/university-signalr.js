// Create connection to SignalR hub
const connection = new signalR.HubConnectionBuilder()
    .withUrl("/universityhub")
    .withAutomaticReconnect()
    .configureLogging(signalR.LogLevel.Information)
    .build();

// Start the connection
async function startConnection() {
    try {
        await connection.start();
        console.log("SignalR connected");
    } catch (err) {
        console.error(err);
        setTimeout(startConnection, 5000); // Retry after 5 seconds
    }
}

// Connection lifecycle events
connection.onclose(async () => {
    console.log("SignalR disconnected");
    await startConnection();
});

// Student notifications
connection.on("StudentAdded", (firstName, lastName) => {
    console.log(`New student added: ${firstName} ${lastName}`);
    displayNotification(`New student added: ${firstName} ${lastName}`);
    
    // Refresh the list if on students page
    if (window.location.pathname.includes('/Students')) {
        refreshList();
    }
});

connection.on("StudentUpdated", (id, firstName, lastName) => {
    console.log(`Student updated: ${firstName} ${lastName}`);
    displayNotification(`Student updated: ${firstName} ${lastName}`);
    
    // Refresh the list if on students page
    if (window.location.pathname.includes('/Students')) {
        refreshList();
    }
});

connection.on("StudentDeleted", (id) => {
    console.log(`Student deleted: ${id}`);
    displayNotification(`Student deleted`);
    
    // Refresh the list if on students page
    if (window.location.pathname.includes('/Students')) {
        refreshList();
    }
});

// Course notifications
connection.on("CourseAdded", (title, credits) => {
    console.log(`New course added: ${title}`);
    displayNotification(`New course added: ${title}`);
    
    // Refresh the list if on courses page
    if (window.location.pathname.includes('/Courses')) {
        refreshList();
    }
});

connection.on("CourseUpdated", (id, title) => {
    console.log(`Course updated: ${title}`);
    displayNotification(`Course updated: ${title}`);
    
    // Refresh the list if on courses page
    if (window.location.pathname.includes('/Courses')) {
        refreshList();
    }
});

connection.on("CourseDeleted", (id) => {
    console.log(`Course deleted: ${id}`);
    displayNotification(`Course deleted`);
    
    // Refresh the list if on courses page
    if (window.location.pathname.includes('/Courses')) {
        refreshList();
    }
});

// Instructor notifications
connection.on("InstructorAdded", (firstName, lastName) => {
    console.log(`New instructor added: ${firstName} ${lastName}`);
    displayNotification(`New instructor added: ${firstName} ${lastName}`);
    
    // Refresh the list if on instructors page
    if (window.location.pathname.includes('/Instructors')) {
        refreshList();
    }
});

connection.on("InstructorUpdated", (id, firstName, lastName) => {
    console.log(`Instructor updated: ${firstName} ${lastName}`);
    displayNotification(`Instructor updated: ${firstName} ${lastName}`);
    
    // Refresh the list if on instructors page
    if (window.location.pathname.includes('/Instructors')) {
        refreshList();
    }
});

connection.on("InstructorDeleted", (id) => {
    console.log(`Instructor deleted: ${id}`);
    displayNotification(`Instructor deleted`);
    
    // Refresh the list if on instructors page
    if (window.location.pathname.includes('/Instructors')) {
        refreshList();
    }
});

// Department notifications
connection.on("DepartmentAdded", (name) => {
    console.log(`New department added: ${name}`);
    displayNotification(`New department added: ${name}`);
    
    // Refresh the list if on departments page
    if (window.location.pathname.includes('/Departments')) {
        refreshList();
    }
});

connection.on("DepartmentUpdated", (id, name) => {
    console.log(`Department updated: ${name}`);
    displayNotification(`Department updated: ${name}`);
    
    // Refresh the list if on departments page
    if (window.location.pathname.includes('/Departments')) {
        refreshList();
    }
});

connection.on("DepartmentDeleted", (id) => {
    console.log(`Department deleted: ${id}`);
    displayNotification(`Department deleted`);
    
    // Refresh the list if on departments page
    if (window.location.pathname.includes('/Departments')) {
        refreshList();
    }
});

// Helper functions
function displayNotification(message) {
    const notifContainer = document.getElementById('notification-container');
    if (!notifContainer) return;
    
    const notif = document.createElement('div');
    notif.className = 'alert alert-info alert-dismissible fade show';
    notif.role = 'alert';
    
    notif.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    notifContainer.appendChild(notif);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notif.parentNode) {
            notif.classList.remove('show');
            setTimeout(() => notif.remove(), 500);
        }
    }, 5000);
}

function refreshList() {
    // This can be improved with a partial refresh using AJAX
    location.reload();
}

// Start the SignalR connection
document.addEventListener('DOMContentLoaded', () => {
    startConnection();
});
