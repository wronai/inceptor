// Custom JavaScript for Inceptor documentation

document.addEventListener('DOMContentLoaded', function() {
    // Add copy button to code blocks
    const codeBlocks = document.querySelectorAll('pre > code');
    
    codeBlocks.forEach(function(codeBlock) {
        // Skip if already has a copy button
        if (codeBlock.parentElement.querySelector('.copy-code-button')) {
            return;
        }
        
        const button = document.createElement('button');
        button.className = 'md-clipboard md-icon';
        button.title = 'Copy to clipboard';
        button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 21H8V7h11m0-2H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2m-3-4H4a2 2 0 0 0-2 2v14h2V3h12V1z"></path></svg>';
        
        button.addEventListener('click', function() {
            navigator.clipboard.writeText(codeBlock.textContent).then(function() {
                // Change button appearance temporarily
                button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21 7L9 19l-5.5-5.5 1.41-1.41L9 16.17 19.59 5.59 21 7z"></path></svg>';
                button.title = 'Copied!';
                
                setTimeout(function() {
                    button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 21H8V7h11m0-2H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2m-3-4H4a2 2 0 0 0-2 2v14h2V3h12V1z"></path></svg>';
                    button.title = 'Copy to clipboard';
                }, 2000);
            });
        });
        
        const wrapper = document.createElement('div');
        wrapper.className = 'code-wrapper';
        codeBlock.parentNode.insertBefore(wrapper, codeBlock);
        wrapper.appendChild(codeBlock);
        wrapper.appendChild(button);
    });

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                });
                
                // Update URL without jumping
                history.pushState(null, null, targetId);
            }
        });
    });

    // Add active class to current nav item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.md-nav__link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('md-nav__link--active');
            
            // Expand parent navigation items
            let parent = link.parentElement;
            while (parent && !parent.classList.contains('md-nav')) {
                if (parent.classList.contains('md-nav__item')) {
                    parent.classList.add('md-nav__item--active');
                    const toggle = parent.querySelector('.md-nav__toggle');
                    if (toggle) toggle.checked = true;
                }
                parent = parent.parentElement;
            }
        }
    });
});
