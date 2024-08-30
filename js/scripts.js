document.addEventListener("DOMContentLoaded", function () {
    const header = `
        <header>
            <nav>
                <div class="logo">
                    <a href="index.html">
                        {arnab.basak}
                    </a>
                </div>
                <ul class="nav-links">
                    <li><a href="index.html">Home</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="projects.html">Projects</a></li>
                </ul>
            </nav>
        </header>
    `;

    const footer = `
        <footer>
            <p>To reach me..</p>
            <div class="social-icons">
                <a href="https://linkedin.com/in/yourprofile" target="_blank"><i class="fab fa-linkedin"></i></a>
                <a href="https://github.com/yourprofile" target="_blank"><i class="fab fa-github"></i></a>
                <a href="https://twitter.com/yourprofile" target="_blank"><i class="fab fa-twitter"></i></a>
                <a href="https://twitter.com/yourprofile" target="_blank"><i class="fab fa-gitlab"></i></a>
            </div>
        </footer>
    `;

    document.body.insertAdjacentHTML("afterbegin", header);
    // document.body.insertAdjacentHTML("beforeend", footer);

    // typing line

    const lines = [
        "Hey, this is Arnab Basak",
        "I am a Software Engineer",
        "Passionate about Building Impactful Solutions"
    ];

    const typingContainer = document.getElementById("typing-container");

    let lineIndex = 0;
    let charIndex = 0;
    let typingSpeed = 100; // ms per character
    let delayBetweenLines = 1200; // ms between lines
    let delayAfterTyping = 1000; // ms after typing a line before restarting

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
                    lineIndex = 0; // Restart from the first line
                }
                charIndex = 0;
                typingContainer.innerHTML = ''; // Clear text after line completion
                setTimeout(typeLine, delayBetweenLines); // Delay before starting the next line
            }, delayAfterTyping);
        }
    }

    typeLine();

});
