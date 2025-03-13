
document.addEventListener('DOMContentLoaded', function() {
    // Create the dynamic background container
    const dynamicBg = document.createElement('div');
    dynamicBg.className = 'dynamic-background';
    
    // Create shapes
    for (let i = 1; i <= 4; i++) {
        const shape = document.createElement('div');
        shape.className = `bg-shape shape${i}`;
        dynamicBg.appendChild(shape);
    }
    
    // Add the dynamic background to the body
    document.body.prepend(dynamicBg);
    
    // Optional: Add slight movement on mouse move
    document.addEventListener('mousemove', function(e) {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        const shapes = document.querySelectorAll('.bg-shape');
        shapes.forEach((shape, index) => {
            const factor = (index + 1) * 5;
            shape.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
        });
    });
});
