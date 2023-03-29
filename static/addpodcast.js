window.onload = () => main();

function main() {
    const searchForm = document.getElementById("searchForm");
    const submitter = document.getElementById("searchSubmitBtn");

    searchForm.addEventListener("submit", async e => {
        e.preventDefault();
        const formData = new FormData(searchForm, submitter);
        // console.log(formData.get("query"));

        const url = new URL("/get-podcast-by-name", window.location.origin);
        url.searchParams.append("query", formData.get("query"));

        const res = await fetch(url.href);
        const json = await res.json();
        renderResults(json);
    });
}

async function addPodcast(e) {
    // console.log(e.dataset.podId);
    const url = new URL("/add-podcast", window.location.origin);
    url.searchParams.append("pod_id", e.dataset.podId);

    const res = await fetch(url.href);
    const json = await res.json();
    // console.log(url);

    if (!json.status) {
        console.error("An Error Occured while adding the podcast");
    } else {
        console.log("Added Podcast");
    }
    // console.log("Adding Podcast!");
}

function renderResults(results) {
    const resultEl = document.querySelector(".results");
    resultEl.textContent = "";
    let html = "";
    results.forEach(pod => {
        const podEl = `
        <div class="res-podcast">
            <img class="pod-artwork" src="${pod.artwork}" alt="${pod.title} artwork" />
            <div class="pod-text">
                <div class="pod-main-text">
                    <div class="pod-title">${pod.title}</div>
                    <a href="${pod.link}" class="pod-link" target="_blank">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
                        </svg>
                    </a>
                </div>        
                <div class="pod-subtext">
                    <div class="pod-author">${pod.author}</div>
                    <div class="pod-episodes">${pod.episodeCount} Eps</div>
                </div>
                <div class="pod-desc">${pod.description}</div>
                <div class="pod-tags">
                    ${pod.categories && Object.values(pod.categories).reduce((acc, tag) => acc += '<div class="tag">' + tag + '</div>', "")}
                </div>
                <div class="pod-actions">
                    <button class="pod-add-btn" data-pod-id="${pod.id}" onclick="addPodcast(this);">+ Add Podcast</button>
                </div>
            </div>
        </div>
        `;
        html += podEl;
    });
    resultEl.innerHTML = html;
}