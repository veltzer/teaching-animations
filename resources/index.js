const indexView = document.getElementById("index-view");
const playerView = document.getElementById("player-view");
const playerTitle = document.getElementById("player-title");
const playerContent = document.getElementById("player-content");
const backBtn = document.getElementById("back-btn");
const results = document.getElementById("results");
const search = document.getElementById("search");

function render(filter) {
    const q = (filter || "").trim().toLowerCase();
    const visible = DATA.filter(entry => {
        if (!q) return true;
        return entry.title.toLowerCase().includes(q) ||
               entry.description.toLowerCase().includes(q) ||
               entry.slug.toLowerCase().includes(q);
    });

    results.innerHTML = "";
    if (visible.length === 0) {
        const empty = document.createElement("div");
        empty.className = "no-results";
        empty.textContent = "No animations match your search.";
        results.appendChild(empty);
        return;
    }

    for (const entry of visible) {
        const card = document.createElement("div");
        card.className = "card";
        card.addEventListener("click", () => openPlayer(entry));

        const h3 = document.createElement("h3");
        h3.textContent = entry.title;
        card.appendChild(h3);

        const p = document.createElement("p");
        p.textContent = entry.description;
        card.appendChild(p);

        const meta = document.createElement("div");
        meta.className = "meta";
        const sceneCount = entry.scenes.length;
        meta.textContent = sceneCount + " scene" + (sceneCount === 1 ? "" : "s");
        card.appendChild(meta);

        results.appendChild(card);
    }
}

function openPlayer(entry) {
    playerTitle.textContent = entry.title;
    playerContent.innerHTML = "";

    for (const scene of entry.scenes) {
        const block = document.createElement("div");
        block.className = "scene-block";

        const h3 = document.createElement("h3");
        h3.textContent = scene.label;
        block.appendChild(h3);

        const video = document.createElement("video");
        video.src = scene.path;
        video.controls = true;
        video.preload = "metadata";
        block.appendChild(video);

        playerContent.appendChild(block);
    }

    indexView.style.display = "none";
    playerView.style.display = "block";
    window.scrollTo(0, 0);
    location.hash = "#" + entry.slug;
}

function closePlayer() {
    for (const v of playerContent.querySelectorAll("video")) {
        v.pause();
    }
    playerView.style.display = "none";
    indexView.style.display = "block";
    if (location.hash) {
        history.pushState("", document.title, location.pathname);
    }
}

function handleHash() {
    const slug = location.hash.replace(/^#/, "");
    if (!slug) {
        closePlayer();
        return;
    }
    const entry = DATA.find(e => e.slug === slug);
    if (entry) {
        openPlayer(entry);
    }
}

backBtn.addEventListener("click", closePlayer);
search.addEventListener("input", () => render(search.value));
window.addEventListener("hashchange", handleHash);

render("");
handleHash();

(function() {
    const THEME_KEY = "animations-browser-theme";
    const sel = document.getElementById("theme-select");
    const saved = localStorage.getItem(THEME_KEY) || "midnight";

    function applyTheme(name) {
        document.documentElement.setAttribute("data-theme", name);
        sel.value = name;
        localStorage.setItem(THEME_KEY, name);
    }

    sel.addEventListener("change", function() {
        applyTheme(sel.value);
    });

    applyTheme(saved);
})();
