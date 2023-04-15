const DOWNLOAD_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg>`;
const SPINNER_SVG = `<svg width="24" height="24" stroke="#000" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><style>.spinner_V8m1{transform-origin:center;animation:spinner_zKoa 2s linear infinite}.spinner_V8m1 circle{stroke-linecap:round;animation:spinner_YpZS 1.5s ease-in-out infinite}@keyframes spinner_zKoa{100%{transform:rotate(360deg)}}@keyframes spinner_YpZS{0%{stroke-dasharray:0 150;stroke-dashoffset:0}47.5%{stroke-dasharray:42 150;stroke-dashoffset:-16}95%,100%{stroke-dasharray:42 150;stroke-dashoffset:-59}}</style><g class="spinner_V8m1"><circle cx="12" cy="12" r="9.5" fill="none" stroke-width="3"></circle></g></svg>`;

async function getPodcast(feedId) {
    const res = await fetch(`/get-podcast-info/${feedId}`);
    const json = await res.json();
    // console.log(json);
    renderPodcast(json.podcast);
    renderEpisodes(json.episodes);
}

function renderPodcast(podcastData) {
    // @temp
    const html = `<div class="art">
        <img class="podcast-artwork" src="" alt="${podcastData[1]} Artwork" />
    </div>
    <div class="info-text">
        <div class="title">${podcastData[1]}</div>
        <div class="author">${podcastData[4]}</div>
        <div class="description">${podcastData[3]}</div>
    </div>`;
    document.querySelector(".info-banner").innerHTML = html;

    fetch(`/podcast/artwork/${podcastData[0]}`).then(res => res.json()).then(json => {
        document.querySelector(`.podcast-artwork`).src = `../${json.url}`; // @temp
    });
}

function renderEpisodes(episodes) {
    const epEl = document.querySelector("tbody.episodes");
    while (epEl.children.length > 0) epEl.children[0].remove();

    episodes.forEach((ep, idx) => {
        let row = buildRow(ep, episodes.length - idx);
        epEl.appendChild(row);
    });

}

function formatDate(timestamp) {
    const date = new Date(timestamp * 1000);

    return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
    });
}

function buildRow(data, idx) {
    const row = document.createElement("tr");
    row.classList.add(`row_${data[0]}`);

    const downloaded = Boolean(data[11]);
    const prop = [idx, data[1], formatDate(data[4]), downloaded ? "Downloaded" : "Not Downloaded", "--toolbox--"];

    prop.forEach(item => {
        const td = document.createElement("td");
        // @temp
        if (item === "--toolbox--") {
            if (!downloaded) {
                const downloadBtn = document.createElement("button");
                downloadBtn.classList.add(...["download-btn"]);
                downloadBtn.dataset.id = data[0];
                downloadBtn.innerHTML = DOWNLOAD_SVG;
                downloadBtn.addEventListener("click", e => {
                    e.target.disabled = true;
                    e.target.innerHTML = SPINNER_SVG;

                    fetch(`/episode/download/${e.target.dataset.id}`).then(res => res.json()).then(json => {
                        if (json.status === 200) {
                            console.log("Downloaded!");
                            addToast("Download Finished", "success");
                            document.querySelector(`.row_${e.target.dataset.id} td:nth-of-type(4)`).textContent = "Downloaded";
                            e.target.remove();
                        } else if (json.status === 418) {
                            addToast("Download Failed", "danger");
                            e.target.innerHTML = DOWNLOAD_SVG;
                        }
                    }).catch(err => {
                        console.error("An Error Occurred while Downloading the Episode!", err);
                        e.target.innerHTML = DOWNLOAD_SVG;
                    });
                });
                td.appendChild(downloadBtn);
            }
        } else {
            const textEl = document.createTextNode(item);
            td.appendChild(textEl);
        }
        row.appendChild(td);
    });

    return row;
}

window.onload = async () => {
    getPodcast(window.feedId);

    const displayErr = (msg, err) => {
        if (err) console.error(`${msg}\n`, err);
        addToast("An Error Occurred", "danger");
    }

    const refreshBtn = document.getElementById("refreshBtn");
    refreshBtn.addEventListener("click", e => {
        fetch(`/podcast/verify/${window.feedId}`).then(res => res.json()).then(json => {
            if (json.status === 200) {
                addToast("Verified Files!", "success");
                document.querySelector("tbody.episodes").innerHTML = "";
                getPodcast(window.feedId);
            } else {
                displayErr();
            }
        }).catch(err => {
            displayErr("An Error Occurred while verifying files!", err);
        });
    });

    const openDirBtn = document.getElementById("openDirBtn");
    openDirBtn.addEventListener("click", e => {
        fetch(`/podcast/open_dir/${window.feedId}`).then(res => res.json()).then(json => {
            if (json.status != 200) {
                displayErr();
            }
        }).catch(err => {
            displayErr("An Error Occurred while Opening Explorer!", err);

        });
    });

    const downloadBtn = document.getElementById("downloadBtn");
    downloadBtn.addEventListener("click", e => {
        fetch(`/podcast/download/${window.feedId}`).then(res => res.json()).then(json => {
            document.querySelectorAll(".download-btn").forEach(item => item.innerHTML = SPINNER_SVG);

            if (json.status === 200) {
                console.log("Downloaded!");
                addToast("Download Finished", "success");
                // document.querySelectorAll(".download-btn").forEach(item => item.remove());
                document.querySelector("tbody.episodes").innerHTML = "";
                getPodcast(window.feedId);
            } else if (json.status === 418) {
                addToast("Download Failed", "danger");
                document.querySelectorAll(".download-btn").forEach(item => item.innerHTML = DOWNLOAD_SVG);
            }
        });
    });
}