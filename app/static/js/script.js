document.addEventListener('DOMContentLoaded', function () {


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

    

    document.addEventListener('DOMContentLoaded', function () {

        // Check if we are on the admin page by looking for the sidebar
        const sidebarLinks = document.querySelectorAll('.sidebar-link');
        const views = document.querySelectorAll('.dashboard-content .view');

        if (sidebarLinks.length > 0 && views.length > 0) {
            sidebarLinks.forEach(link => {
                link.addEventListener('click', function (e) {
                    e.preventDefault();


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
