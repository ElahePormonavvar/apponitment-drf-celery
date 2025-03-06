//setup nav
const navBtn = document.getElementById("nav-btn");
const navbar = document.getElementById("navbar");
const navClose = document.getElementById("nav-close");
//show nav
navBtn.addEventListener("click", () => {
    navbar.classList.add("show-nav");
});

navClose.addEventListener("click", () => {
    navbar.classList.remove("show-nav");
});

const API_BASE_URL = 'http://127.0.0.1:8000';
// login
async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch(`${API_BASE_URL}/accounts/login/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        const data = await response.json();
        accessToken = data.access;
        localStorage.setItem('accessToken', accessToken);
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('appointments').style.display = 'block';
        fetchAppointments();
    } else {
        alert('نام کاربری یا رمز عبور اشتباه است');
    }
}


document.addEventListener('DOMContentLoaded', function () {
    fetch('http://127.0.0.1:8000/api/appointments/')
        .then(response => response.json())
        .then(data => {
            const appointmentsDiv = document.getElementById('appointments');
            data.forEach(appointment => {
                const appointmentDiv = document.createElement('div');
                appointmentDiv.className = 'appointment';
                appointmentDiv.innerHTML = `
                    <strong>کاربر:</strong> ${appointment.patient}<br>
                    <strong>تاریخ:</strong> ${new Date(appointment.appointment_date).toLocaleString()}<br>
                    
                `;
                appointmentsDiv.appendChild(appointmentDiv);
            });
        })
        .catch(error => console.error('Error fetching appointments:', error));
});


