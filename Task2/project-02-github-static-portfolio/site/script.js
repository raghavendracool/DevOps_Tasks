const yearElement = document.getElementById("year");
const menuButton = document.getElementById("menu-button");
const navLinks = document.getElementById("nav-links");
const contactButton = document.getElementById("contact-button");
const contactStatus = document.getElementById("contact-status");

yearElement.textContent = new Date().getFullYear();

menuButton.addEventListener("click", () => {
    navLinks.classList.toggle("open");
});

document.querySelectorAll("#nav-links a").forEach((link) => {
    link.addEventListener("click", () => {
        navLinks.classList.remove("open");
    });
});

contactButton.addEventListener("click", async () => {
    const email = "your-email@example.com";

    try {
        await navigator.clipboard.writeText(email);
        contactStatus.textContent = "Email address copied.";
    } catch (error) {
        contactStatus.textContent = `Copy failed. Email: ${email}`;
    }
});
