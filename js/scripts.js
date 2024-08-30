document.addEventListener("DOMContentLoaded", function () {
    const header = `
          <header class="fixed-header">
              <nav class="navbar">
                  <div class="logo">
                      <a href="index.html">
                          {{arnab.basak}}
                      </a>
                  </div>
                  <ul class="nav-links">
                      <li><a href="about.html">Explore Arnab</a></li>
                  </ul>
              </nav>
              <div class="breadcrumb">
                  <a href="index.html">Home</a>
              </div>
          </header>
      `;
  
    document.body.insertAdjacentHTML("afterbegin", header);
  
    // Update breadcrumb based on current page
  
    const currentPath = window.location.pathname; // Get current page path
    const breadcrumbList = document.querySelector('.breadcrumb'); // Select breadcrumb element
  
    if (currentPath !== '/') { // Check if not on homepage
      const pageTitle = currentPath.split('/').pop().replace('.html', ''); // Extract page title
      breadcrumbList.innerHTML += ` > <a href="${currentPath}">${pageTitle}</a>`; // Add link and title
    }
  
    const lines = [
      "Hey, this is Arnab Basak",
      "I am a Software Engineer",
      "Passionate about Building Impactful Solutions"
    ];
  
    const typingContainer = document.getElementById("typing-container");
  
    let lineIndex = 0;
    let charIndex = 0;
    let typingSpeed = 100;
    let delayBetweenLines = 800;
    let delayAfterTyping = 1000;
  
    function typeLine() {
      if (charIndex < lines[lineIndex].length) {
        let lineElement = document.createElement("div");
        lineElement.classList.add("typing-text");
        lineElement.textContent = lines[lineIndex].slice(0, charIndex + 1);
        typingContainer.innerHTML = '';
        typingContainer.appendChild(lineElement);
        charIndex++;
        setTimeout(typeLine, typingSpeed);
      } else {
        setTimeout(() => {
          lineIndex++;
          if (lineIndex >= lines.length) {
            lineIndex = 0;
          }
          charIndex = 0;
          typingContainer.innerHTML = '';
          setTimeout(typeLine, delayBetweenLines);
        }, delayAfterTyping);
      }
    }
  
    typeLine();
  });