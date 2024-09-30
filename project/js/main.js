// FAQ accordion
document.addEventListener('DOMContentLoaded', () => {
    const faqContainer = document.querySelector('.faq-content');

    faqContainer.addEventListener('click', (e) => {
        const groupHeader = e.target.closest('.faq-group-header');
        if (!groupHeader) return;

        const group = groupHeader.parentElement;
        const groupBody = group.querySelector('.faq-group-body');
        const icon = groupHeader.querySelector('i');

        // Toggle icon
        icon.classList.toggle('fa-plus');
        icon.classList.toggle('fa-minus');

        // toggle visibility of body
        groupBody.classList.toggle('open');

        // close other open FAQ bodies
        const otherGroups = faqContainer.querySelectorAll('.faq-group');
        otherGroups.forEach((otherGroup) => {
            if (otherGroup !== group) {
                const otherGroupBody = otherGroup.querySelector('.faq-group-body');
                const otherIcon = otherGroup.querySelector('.faq-group-header i');
                otherGroupBody.classList.remove('open');
                otherIcon.classList.remove('fa-minus');
                otherIcon.classList.add('fa-plus');
            }
        });
    });
});

// Mobile menu
document.addEventListener('DOMContentLoaded', () => {
    const hamburgerButton = document.querySelector('.hamburger-button');
    const mobileMenu = document.querySelector('.mobile-menu');

    hamburgerButton.addEventListener('click', () =>
        mobileMenu.classList.toggle('active')
    );
});

// About Us Modal
document.addEventListener('DOMContentLoaded', function () {
    function showAboutUsModal() {
        const aboutUsModal = document.getElementById('aboutUsModal');
        aboutUsModal.classList.remove('modal-hidden');
        aboutUsModal.classList.add('modal-visible');
    }

    function closeAboutUsModal() {
        const aboutUsModal = document.getElementById('aboutUsModal');
        aboutUsModal.classList.remove('modal-visible');
        aboutUsModal.classList.add('modal-hidden');
    }

    document.querySelectorAll('#aboutUsLink, #aboutUsLinkMobile, #footerAboutUsLink').forEach(element => {
        element.addEventListener('click', function (event) {
            event.preventDefault();
            showAboutUsModal();
        });
    });

    document.querySelector('#aboutUsModal .icon-close').addEventListener('click', function () {
        closeAboutUsModal();
    });

    window.addEventListener('click', function (event) {
        const aboutUsModal = document.getElementById('aboutUsModal');
        if (event.target === aboutUsModal) {
            closeAboutUsModal();
        }
    });
});

// Logging
document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM fully loaded and parsed");

    const btnSignInDesktop = document.querySelector('#signInBtnDesktop');
    const btnGetStarted = document.querySelector('#getStartedBtn');
    const modalWrapper = document.querySelector('#loginModal');
    const closeModalIcon = document.querySelector('.close');
    const loginForm = document.querySelector('.form-box.login');
    const registerForm = document.querySelector('.form-box.register');
    const registerLink = document.querySelector('.register-link');
    const loginLink = document.querySelector('.login-link');
    const loginFormElement = document.querySelector('#loginForm');
    const registerFormElement = document.querySelector('#registerForm');
    const subscriptionForm = document.querySelector('#subscriptionForm')

    function showModal() {
        modalWrapper.classList.remove('modal-hidden');
        modalWrapper.classList.add('modal-visible');
        loginForm.classList.add('active');
        registerForm.classList.remove('active');
    }

    function closeModal() {
        modalWrapper.classList.remove('modal-visible');
        modalWrapper.classList.add('modal-hidden');
        loginFormElement.reset();
        registerFormElement.reset();
    }

    // Event listener for opening the modal for sign in
    btnSignInDesktop.addEventListener('click', function (event) {
        event.preventDefault();
        console.log("Sign In button clicked");
        showModal();
    });

    // Event listener for getting started, which checks login status
    btnGetStarted.addEventListener('click', async function (event) {
        event.preventDefault();

        const response = await fetch('/check-login-status');
        const isLoggedIn = await response.json();

        if (isLoggedIn) {
            window.location.href = 'chatbot';
        } else {
            showModal();
        }
    });

    // Event listener for closing the modal
    closeModalIcon.addEventListener('click', closeModal);

    // Toggle between login and register forms
    registerLink.addEventListener('click', function (event) {
        event.preventDefault();
        loginForm.classList.remove('active');
        registerForm.classList.add('active');
    });

    loginLink.addEventListener('click', function (event) {
        event.preventDefault();
        registerForm.classList.remove('active');
        loginForm.classList.add('active');
    });

    // Close the modal when clicking outside of it
    window.addEventListener('click', function (event) {
        if (event.target === modalWrapper) {
            closeModal();
        }
    });

    // Handle register form submission
    registerFormElement.addEventListener('submit', async function (event) {
        event.preventDefault();
        console.log("Register form submitted");

        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const termsAccepted = document.querySelector('#terms').checked;

        if (!termsAccepted) {
            alert('You must agree to the terms and conditions.');
            return;
        }

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email, password })
            });

            const result = await response.json();
            console.log(result);

            if (response.ok) {
                alert('Registration successful! Please log in.');
                registerFormElement.reset();
            } else {
                alert(result.message || 'Registration failed.');
            }
        } catch (error) {
            console.log('test')
        }
    });

    // Handle login form submission
    loginFormElement.addEventListener('submit', async function (event) {
        event.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const result = await response.json();

            if (response.ok) {
                alert('Login successful!');
                localStorage.setItem('isLoggedIn', 'true'); // or use a global variable
                window.location.href = 'chatbot';
            } else {
                alert(result.message || 'Login failed.');
            }
        } catch (error) {
            alert('An error occurred. Please try again.');
        }
    });

    subscriptionForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const email = document.getElementById('subscriptionMail').value;
        console.log(email)
        try {
            const response = await fetch('/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });

            const result = await response.json();

            if (response.ok) {
                console.log("Subscription successful!", result);
                alert(result.message);
            } else {
                console.log("Subscription failed!", result);
                alert(result.message);
            }
        } catch (error) {
            console.error('An error occurred:', error);
            alert('An error occurred. Please try again.');
        }
    })
});


//subscription 
