console.log('tabs.js loaded!');

document.addEventListener('DOMContentLoaded', function() {
  console.log('DOMContentLoaded fired!');
  
  const tabContainers = document.querySelectorAll('.tab-container');
  console.log('Found tab containers:', tabContainers.length);
  
document.addEventListener('DOMContentLoaded', function() {
  // Initialize all tab containers
  const tabContainers = document.querySelectorAll('.tab-container');
  
  tabContainers.forEach(container => {
    const buttons = container.querySelectorAll('.tab-button');
    const contents = container.querySelectorAll('.tab-content');
    
    // Set first tab as active by default
    if (buttons.length > 0 && contents.length > 0) {
      buttons[0].classList.add('active');
      contents[0].classList.add('active');
    }
    
    // Add click handlers
    buttons.forEach((button, index) => {
      button.addEventListener('click', () => {
        // Remove active class from all buttons and contents
        buttons.forEach(btn => btn.classList.remove('active'));
        contents.forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked button and corresponding content
        button.classList.add('active');
        contents[index].classList.add('active');
        
        // Store preference in localStorage
        const tabId = container.getAttribute('data-tab-group');
        if (tabId) {
          localStorage.setItem(`tab-${tabId}`, index);
        }
      });
    });
    
    // Restore saved tab preference
    const tabId = container.getAttribute('data-tab-group');
    if (tabId) {
      const savedIndex = localStorage.getItem(`tab-${tabId}`);
      if (savedIndex !== null && buttons[savedIndex] && contents[savedIndex]) {
        buttons.forEach(btn => btn.classList.remove('active'));
        contents.forEach(content => content.classList.remove('active'));
        buttons[savedIndex].classList.add('active');
        contents[savedIndex].classList.add('active');
      }
    }
  });
});