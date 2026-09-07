(function () {
    'use strict';

    var body = document.body;
    var nav = document.getElementById('mainNav');
    var navToggle = document.getElementById('navToggle');
    var mobileNav = document.getElementById('mobileNav');
    var mobileOverlay = document.getElementById('mobileOverlay');
    var mobileClose = document.getElementById('mobileClose');
    var backToTop = document.getElementById('backToTop');
    var chatToggle = document.getElementById('chatToggle');
    var chatBubble = document.getElementById('chatBubble');
    var loader = document.getElementById('siteLoader');

    function setMobileState(isOpen) {
        if (!mobileNav || !mobileOverlay || !navToggle) return;
        mobileNav.classList.toggle('open', isOpen);
        mobileOverlay.classList.toggle('open', isOpen);
        navToggle.setAttribute('aria-expanded', String(isOpen));
        body.classList.toggle('is-locked', isOpen);
    }

    if (loader) {
        window.addEventListener('load', function () {
            window.setTimeout(function () { loader.classList.add('hidden'); }, 250);
        });
    }

    window.addEventListener('scroll', function () {
        if (nav) nav.classList.toggle('scrolled', window.scrollY > 18);
        if (backToTop) backToTop.classList.toggle('visible', window.scrollY > 450);
    }, { passive: true });

    if (navToggle) navToggle.addEventListener('click', function () {
        setMobileState(!mobileNav.classList.contains('open'));
    });
    if (mobileClose) mobileClose.addEventListener('click', function () { setMobileState(false); });
    if (mobileOverlay) mobileOverlay.addEventListener('click', function () { setMobileState(false); });
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') setMobileState(false);
    });
    document.querySelectorAll('.mobile-nav a').forEach(function (link) {
        link.addEventListener('click', function () { setMobileState(false); });
    });

    if (backToTop) backToTop.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    if (chatToggle && chatBubble) chatToggle.addEventListener('click', function () {
        var isOpen = chatBubble.classList.toggle('open');
        chatToggle.setAttribute('aria-expanded', String(isOpen));
    });

    document.querySelectorAll('.chat-option').forEach(function (button) {
        button.addEventListener('click', function () {
            var message = document.getElementById('chatMessage');
            if (message) message.textContent = button.dataset.response;
        });
    });

    var revealObserver = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries, observer) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08 }) : null;
    document.querySelectorAll('.reveal, .reveal-stagger').forEach(function (element) {
        if (revealObserver) revealObserver.observe(element);
        else element.classList.add('in');
    });

    var counterObserver = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries, observer) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            observer.unobserve(entry.target);
            var target = Number(entry.target.dataset.count);
            var start = performance.now();
            function tick(now) {
                var progress = Math.min((now - start) / 1200, 1);
                var eased = 1 - Math.pow(1 - progress, 3);
                entry.target.textContent = Math.round(target * eased).toLocaleString('en-US');
                if (progress < 1) window.requestAnimationFrame(tick);
            }
            window.requestAnimationFrame(tick);
        });
    }, { threshold: 0.3 }) : null;
    document.querySelectorAll('[data-count]').forEach(function (element) {
        if (counterObserver) counterObserver.observe(element);
        else element.textContent = Number(element.dataset.count).toLocaleString('en-US');
    });
}());
