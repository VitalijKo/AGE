function getCookie(name) {
    if (document.cookie) {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
}

const password = document.querySelector('#password');
const username = document.querySelector('#username');
const emailfield = document.querySelector('#emailfield');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const emailfeedBack = document.querySelector('.email-feedback');
const feedBackField = document.querySelector('.invalid-feedback');
const usernamevalidOut = document.querySelector('.usernamevalidOut');

const handlePasswordToggle = (e) => {
    if (showPasswordToggle.textContent == 'SHOW') {
        showPasswordToggle.textContent = 'HIDE';
        password.setAttribute('type', 'text');
    } else {
        showPasswordToggle.textContent = 'SHOW';
        password.setAttribute('type', 'password');
    }
}

showPasswordToggle.addEventListener('click', handlePasswordToggle);

username.addEventListener('keyup', (e) => {
    usernameValue = e.target.value;
    usernamevalidOut.style.display = 'block';
    username.classList.remove('is-invalid');
    feedBackField.style.display = 'none';

    if (usernameValue.length > 0) {
        usernamevalidOut.textContent = `Checking Username ${usernameValue}`;

        fetch('/participant/username-validate', {
                body: JSON.stringify({ username: usernameValue }),
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
        }).then((res) => res.json()).then(data => {
	        usernamevalidOut.style.display = 'none';

	        if (data.username_error) {
	            username.classList.add('is-invalid');
	            feedBackField.style.display = 'block';
	            feedBackField.innerHTML = `<p>${data.username_error}</p>`;
	        }
        })
    }
})

emailfield.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;

    emailfield.classList.remove('is-invalid');
    emailfeedBack.style.display = 'none';

    if (emailVal.length > 0) {
        fetch('/participant/email-validate', {
                body: JSON.stringify({ email: emailVal }),
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
        }).then((res) => res.json()).then((data) => {
            if (data.email_error) {
                emailfield.classList.add('is-invalid');
                emailfeedBack.style.display = 'block';
                emailfeedBack.innerHTML = `<p>${data.email_error}</p>`;
            }
        })
    }
})
