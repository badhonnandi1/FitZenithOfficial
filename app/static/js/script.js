document.addEventListener('DOMContentLoaded', function () {

    // --- HEADER SCROLL & MOBILE MENU ---
    const header = document.getElementById('main-header');
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');

    window.addEventListener('scroll', () => {
        header.classList.toggle('scrolled', window.scrollY > 50);
    });

    mobileMenuToggle.addEventListener('click', () => {
        mobileMenuToggle.classList.toggle('active');
        mobileMenu.classList.toggle('open');
        document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
    });

    mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenuToggle.classList.remove('active');
            mobileMenu.classList.remove('open');
            document.body.style.overflow = '';
        });
    });

    // --- SCROLL-BASED FADE-IN ANIMATION ---
    const scrollObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('[data-scroll-fade]').forEach(el => {
        scrollObserver.observe(el);
    });

    // --- TESTIMONIAL SLIDER ---
    const slider = document.querySelector('.testimonial-slider');
    const slides = document.querySelectorAll('.testimonial-slide');
    const nextBtn = document.querySelector('.slider-nav .next');
    const prevBtn = document.querySelector('.slider-nav .prev');
    let currentIndex = 0;

    function updateSlider() {
        slider.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % slides.length;
        updateSlider();
    });

    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        updateSlider();
    });

    // Optional: Auto-play slider
    // setInterval(() => nextBtn.click(), 7000);

    // --- TILT EFFECT FOR FEATURE CARDS ---
    // A simplified CSS-only version is active by default.
    // For a JS-powered 3D tilt, you would use a library like vanilla-tilt.js
    // and initialize it like this:
    // VanillaTilt.init(document.querySelectorAll("[data-tilt]"), {
    //     max: 15,
    //     speed: 400,
    //     glare: true,
    //     "max-glare": 0.5
    // });
    // This would require adding the library's script to your HTML.
    // The current design uses CSS hover effects for a clean, no-dependency solution.

    // --- ADMIN DASHBOARD VIEW SWITCHER ---
    // This code should be added to your existing script.js file

    document.addEventListener('DOMContentLoaded', function () {

        // Check if we are on the admin page by looking for the sidebar
        const sidebarLinks = document.querySelectorAll('.sidebar-link');
        const views = document.querySelectorAll('.dashboard-content .view');

        if (sidebarLinks.length > 0 && views.length > 0) {
            sidebarLinks.forEach(link => {
                link.addEventListener('click', function (e) {
                    e.preventDefault();

                    // Get the target view from the data attribute
                    const targetViewId = this.getAttribute('data-view');
                    const targetView = document.getElementById(`view-${targetViewId}`);

                    // Update active class on links
                    sidebarLinks.forEach(l => l.classList.remove('active'));
                    this.classList.add('active');

                    // Update active class on views
                    views.forEach(v => v.classList.remove('active'));
                    if (targetView) {
                        targetView.classList.add('active');
                    }
                });
            });
        }

        // ... your existing script.js code (header scroll, mobile menu, etc.)
        // can remain here.
    });
    document.addEventListener('DOMContentLoaded', function() {
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');
        const showRegisterLink = document.getElementById('show-register');
        const showLoginLink = document.getElementById('show-login');
    
        showRegisterLink.addEventListener('click', (e) => {
            e.preventDefault();
            loginForm.classList.add('hidden');
            registerForm.classList.remove('hidden');
        });
    
        showLoginLink.addEventListener('click', (e) => {
            e.preventDefault();
            registerForm.classList.add('hidden');
            loginForm.classList.remove('hidden');
        });
    
        // Add form submission logic here later
    });
    

});



document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const mainHeader = document.getElementById('main-header');

    // Toggle mobile menu
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenuToggle.classList.toggle('active');
            mobileMenu.classList.toggle('open');
        });
    }


    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            mainHeader.classList.add('scrolled');
        } else {
            mainHeader.classList.remove('scrolled');
        }
    });
