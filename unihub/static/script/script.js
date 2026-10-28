// ──────────────────────────────────────────────
// UniHub WebGL 3D Engine & Interactive Logic
// ──────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function () {

    // ──────────────────────────────────────────────
    // 1. WebGL Interactive 3D Background (Three.js)
    // ──────────────────────────────────────────────
    init3DBackground();

    // ──────────────────────────────────────────────
    // 2. Swiper 3D Coverflow Carousels (> 3 items)
    // ──────────────────────────────────────────────
    init3DCarousels();

    // ──────────────────────────────────────────────
    // 3. Card 3D Tilt on Mouse Movement
    // ──────────────────────────────────────────────
    init3DTilt();

    // ──────────────────────────────────────────────
    // 4. Scroll Reveal Animations
    // ──────────────────────────────────────────────
    initScrollAnimations();

    // ──────────────────────────────────────────────
    // 5. Smooth Anchor Scrolling & Subscription Form
    // ──────────────────────────────────────────────
    initUIInteractions();
});

/**
 * Creates an interactive 3D WebGL background featuring
 * floating geometric polyhedra, particle constellations,
 * and mouse-responsive lighting & camera parallax.
 */
function init3DBackground() {
    const canvas = document.getElementById('webgl-3d-bg');
    if (!canvas || typeof THREE === 'undefined') return;

    // Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 28;

    const renderer = new THREE.WebGLRenderer({
        canvas: canvas,
        alpha: true,
        antialias: true,
        powerPreference: 'high-performance'
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0x38bdf8, 1.2);
    dirLight1.position.set(20, 25, 15);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x818cf8, 0.8);
    dirLight2.position.set(-20, -15, -10);
    scene.add(dirLight2);

    // Mouse-tracking point light
    const mouseLight = new THREE.PointLight(0x38bdf8, 2.5, 35);
    mouseLight.position.set(0, 0, 10);
    scene.add(mouseLight);

    // 3D Objects Group (Floating Polyhedra)
    const floatingGroup = new THREE.Group();
    scene.add(floatingGroup);

    // Common glossy glass-like materials
    const matGlass = new THREE.MeshStandardMaterial({
        color: 0x1d4ed8,
        roughness: 0.15,
        metalness: 0.65,
        transparent: true,
        opacity: 0.55
    });

    const matGold = new THREE.MeshStandardMaterial({
        color: 0xf59e0b,
        roughness: 0.2,
        metalness: 0.8,
        transparent: true,
        opacity: 0.7
    });

    const matCyan = new THREE.MeshStandardMaterial({
        color: 0x06b6d4,
        roughness: 0.25,
        metalness: 0.6,
        transparent: true,
        opacity: 0.5
    });

    const matWire = new THREE.MeshBasicMaterial({
        color: 0x93c5fd,
        wireframe: true,
        transparent: true,
        opacity: 0.35
    });

    const meshes = [];

    // 1. Torus Knot (Hero center background)
    const torusKnotGeo = new THREE.TorusKnotGeometry(4.2, 1.1, 100, 16);
    const torusKnot = new THREE.Mesh(torusKnotGeo, matGlass);
    torusKnot.position.set(12, 2, -5);
    floatingGroup.add(torusKnot);
    meshes.push({ mesh: torusKnot, rotX: 0.003, rotY: 0.005, floatSpeed: 0.0015, baseY: 2 });

    // Wireframe halo around torus
    const wireHalo = new THREE.Mesh(new THREE.TorusGeometry(6, 0.08, 16, 100), matWire);
    wireHalo.position.set(12, 2, -5);
    floatingGroup.add(wireHalo);
    meshes.push({ mesh: wireHalo, rotX: 0.006, rotY: 0.002, floatSpeed: 0.001, baseY: 2 });

    // 2. Icosahedron (Top left)
    const icoGeo = new THREE.IcosahedronGeometry(2.6, 0);
    const ico = new THREE.Mesh(icoGeo, matCyan);
    ico.position.set(-14, 8, -2);
    floatingGroup.add(ico);
    meshes.push({ mesh: ico, rotX: 0.005, rotY: 0.006, floatSpeed: 0.002, baseY: 8 });

    const icoWire = new THREE.Mesh(icoGeo, matWire);
    ico.add(icoWire);

    // 3. Octahedron (Bottom right)
    const octGeo = new THREE.OctahedronGeometry(2.4, 0);
    const oct = new THREE.Mesh(octGeo, matGold);
    oct.position.set(16, -10, -3);
    floatingGroup.add(oct);
    meshes.push({ mesh: oct, rotX: -0.004, rotY: 0.005, floatSpeed: 0.0018, baseY: -10 });

    // 4. Dodecahedron (Bottom left)
    const dodGeo = new THREE.DodecahedronGeometry(2.2, 0);
    const dod = new THREE.Mesh(dodGeo, matGlass);
    dod.position.set(-16, -9, -4);
    floatingGroup.add(dod);
    meshes.push({ mesh: dod, rotX: 0.004, rotY: -0.003, floatSpeed: 0.0022, baseY: -9 });

    // 5. Floating Ring (Center deep)
    const ringGeo = new THREE.TorusGeometry(3.5, 0.4, 16, 80);
    const ring = new THREE.Mesh(ringGeo, matCyan);
    ring.position.set(-2, 12, -10);
    floatingGroup.add(ring);
    meshes.push({ mesh: ring, rotX: -0.005, rotY: 0.004, floatSpeed: 0.0012, baseY: 12 });

    // 3D Particle Constellation System
    const particleCount = 700;
    const particleGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const c1 = new THREE.Color(0x38bdf8);
    const c2 = new THREE.Color(0x60a5fa);
    const c3 = new THREE.Color(0xfbbf24);

    for (let i = 0; i < particleCount * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 75;
        positions[i + 1] = (Math.random() - 0.5) * 55;
        positions[i + 2] = (Math.random() - 0.5) * 45;

        const rand = Math.random();
        const chosenColor = rand > 0.7 ? c3 : (rand > 0.35 ? c1 : c2);
        colors[i] = chosenColor.r;
        colors[i + 1] = chosenColor.g;
        colors[i + 2] = chosenColor.b;
    }

    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const particleMat = new THREE.PointsMaterial({
        size: 0.28,
        vertexColors: true,
        transparent: true,
        opacity: 0.65,
        blending: THREE.AdditiveBlending
    });

    const particleSystem = new THREE.Points(particleGeo, particleMat);
    scene.add(particleSystem);

    // Mouse tracking for 3D Camera and Point Light
    let targetMouseX = 0;
    let targetMouseY = 0;
    let currentMouseX = 0;
    let currentMouseY = 0;

    window.addEventListener('mousemove', (e) => {
        targetMouseX = (e.clientX / window.innerWidth) * 2 - 1;
        targetMouseY = -(e.clientY / window.innerHeight) * 2 + 1;

        mouseLight.position.x = targetMouseX * 18;
        mouseLight.position.y = targetMouseY * 12;
    });

    // Window Resize Handler
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Animation Loop
    let clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);
        const elapsedTime = clock.getElapsedTime();

        // Rotate individual 3D meshes
        meshes.forEach(item => {
            item.mesh.rotation.x += item.rotX;
            item.mesh.rotation.y += item.rotY;
            item.mesh.position.y = item.baseY + Math.sin(elapsedTime * 1.5 + item.baseY) * 0.8;
        });

        // Rotate particle constellation
        particleSystem.rotation.y = elapsedTime * 0.02;
        particleSystem.rotation.x = elapsedTime * 0.01;

        // Smooth 3D Camera Parallax
        currentMouseX += (targetMouseX - currentMouseX) * 0.04;
        currentMouseY += (targetMouseY - currentMouseY) * 0.04;

        camera.position.x = currentMouseX * 4;
        camera.position.y = currentMouseY * 3 - (window.scrollY * 0.005);
        camera.lookAt(0, 0, 0);

        renderer.render(scene, camera);
    }

    animate();
}

/**
 * Initializes Swiper 3D Coverflow Carousels for sections with > 3 items
 */
function init3DCarousels() {
    if (typeof Swiper === 'undefined') return;

    const carousels = document.querySelectorAll('.swiper-3d-carousel');

    carousels.forEach(carousel => {
        const nextBtn = carousel.querySelector('.swiper-button-next');
        const prevBtn = carousel.querySelector('.swiper-button-prev');
        const paginationEl = carousel.querySelector('.swiper-pagination');

        new Swiper(carousel, {
            effect: 'coverflow',
            grabCursor: true,
            centeredSlides: true,
            slidesPerView: 'auto',
            loop: true,
            observer: true,
            observeParents: true,
            coverflowEffect: {
                rotate: 24,
                stretch: 0,
                depth: 170,
                modifier: 1,
                slideShadows: true,
            },
            autoplay: {
                delay: 3500,
                disableOnInteraction: false,
                pauseOnMouseEnter: true,
            },
            navigation: {
                nextEl: nextBtn,
                prevEl: prevBtn,
            },
            pagination: {
                el: paginationEl,
                clickable: true,
                dynamicBullets: true,
            },
            breakpoints: {
                320: {
                    slidesPerView: 1,
                    coverflowEffect: { rotate: 16, depth: 80 }
                },
                768: {
                    slidesPerView: 2,
                    coverflowEffect: { rotate: 20, depth: 130 }
                },
                1024: {
                    slidesPerView: 3,
                    coverflowEffect: { rotate: 24, depth: 170 }
                }
            }
        });
    });
}

/**
 * Interactive 3D Card Tilt on Mouse Move
 */
function init3DTilt() {
    const tiltElements = document.querySelectorAll('.tilt-3d');

    tiltElements.forEach(element => {
        element.addEventListener('mousemove', function (e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -9;
            const rotateY = ((x - centerX) / centerX) * 9;

            this.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        element.addEventListener('mouseleave', function () {
            this.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        });
    });
}

/**
 * Scroll Entrance Animations
 * Animates elements smoothly onto the display when scrolled into view
 */
function initScrollAnimations() {
    const revealElements = document.querySelectorAll('.reveal-on-scroll');
    if (!revealElements.length) return;

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-revealed');
                }
            });
        }, {
            root: null,
            rootMargin: '0px 0px -40px 0px',
            threshold: 0.08
        });

        revealElements.forEach(el => observer.observe(el));
    } else {
        // Fallback for older browsers
        revealElements.forEach(el => el.classList.add('is-revealed'));
    }
}

/**
 * Smooth Anchor Scroll & Subscription Form Handling
 */
function initUIInteractions() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    const subscribeForm = document.querySelector('.subscribe-form-3d');
    if (subscribeForm) {
        subscribeForm.addEventListener('submit', function (e) {
            const emailInput = subscribeForm.querySelector('input[type="email"]');
            if (emailInput && emailInput.value) {
                if (subscribeForm.getAttribute('action') === '#' || !subscribeForm.getAttribute('action')) {
                    e.preventDefault();
                    alert('Thank you for subscribing! UniHub alerts will be sent to ' + emailInput.value);
                    emailInput.value = '';
                }
            }
        });
    }
}
