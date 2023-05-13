const DOWNLOAD_SVG = `<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" width="24" height="24"><path d="M13 10H18L12 16L6 10H11V3H13V10ZM4 19H20V12H22V20C22 20.5523 21.5523 21 21 21H3C2.44772 21 2 20.5523 2 20V12H4V19Z"></path></svg>`;
const SPINNER_SVG = `<svg width="24" height="24" fill="currentColor" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><style>.spinner_V8m1{transform-origin:center;animation:spinner_zKoa 2s linear infinite}.spinner_V8m1 circle{stroke-linecap:round;animation:spinner_YpZS 1.5s ease-in-out infinite}@keyframes spinner_zKoa{100%{transform:rotate(360deg)}}@keyframes spinner_YpZS{0%{stroke-dasharray:0 150;stroke-dashoffset:0}47.5%{stroke-dasharray:42 150;stroke-dashoffset:-16}95%,100%{stroke-dasharray:42 150;stroke-dashoffset:-59}}</style><g class="spinner_V8m1"><circle cx="12" cy="12" r="9.5" fill="none" stroke-width="3"></circle></g></svg>`;

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
                            addToast("Download Queued", "success");
                            document.querySelector(`.row_${e.target.dataset.id} td:nth-of-type(4)`).textContent = "Queued";
                            // e.target.remove();
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
                console.log("Download Queued!");
                addToast("Download Queued", "success");
                // document.querySelectorAll(".download-btn").forEach(item => item.remove());
                document.querySelector("tbody.episodes").innerHTML = "";
                getPodcast(window.feedId);
            } else if (json.status === 418) {
                addToast("Download Failed", "danger");
                document.querySelectorAll(".download-btn").forEach(item => item.innerHTML = DOWNLOAD_SVG);
            }
        });
    });

    const deleteBtn = document.getElementById("deleteBtn");
    deleteBtn.addEventListener("click", e => {
        fetch(`/podcast/delete/${window.feedId}`).then(res => res.json()).then(json => {
            if (json.status === 200) {
                currentOrigin = new URL(window.location).origin;
                window.location = currentOrigin;
            } else {
                displayErr();
            }
        }).catch(err => {
            displayErr("An Error Occurred While Deleting the Podcast!", err);
        });
    });
}