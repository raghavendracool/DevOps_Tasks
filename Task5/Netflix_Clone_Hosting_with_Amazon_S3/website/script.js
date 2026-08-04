document.addEventListener("DOMContentLoaded", () => {
  const config = window.VIDEO_CONFIG;
  const grid = document.getElementById("movieGrid");
  const modal = document.getElementById("modal");
  const player = document.getElementById("videoPlayer");
  const title = document.getElementById("videoTitle");
  const closeButton = document.getElementById("closeButton");

  config.videos.forEach((video) => {
    const card = document.createElement("article");
    card.className = "movie";
    card.innerHTML = `
      <img src="${video.poster}" alt="${video.title}">
      <div>
        <h3>${video.title}</h3>
        <p>Stream from Amazon S3</p>
      </div>
    `;
    card.addEventListener("click", () => {
      title.textContent = video.title;
      player.src = `${config.bucketBaseUrl}/${video.file}`;
      modal.classList.remove("hidden");
      player.play().catch(() => {});
    });
    grid.appendChild(card);
  });

  function closeModal() {
    player.pause();
    player.removeAttribute("src");
    player.load();
    modal.classList.add("hidden");
  }

  closeButton.addEventListener("click", closeModal);
  modal.addEventListener("click", (event) => {
    if (event.target === modal) closeModal();
  });
});
