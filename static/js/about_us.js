gsap.registerPlugin(ScrollTrigger);

window.addEventListener('load', () => {
    const aboutItems = gsap.utils.toArray('.about-item');

    aboutItems.forEach((item) => {
        gsap.fromTo(item, 
            { opacity: 0, y: 50 }, // стартовое состояние
            { 
                opacity: 1, 
                y: 0, 
                duration: 0.8, 
                ease: "power2.out",
                scrollTrigger: {
                    trigger: item,
                    start: "top 85%", // когда верх элемента достигает 85% высоты окна
                    toggleActions: "play none none reverse"
                }
            }
        );
    });
});
