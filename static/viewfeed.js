// async function getEpisodes(feedId) {
//     const res = await fetch(`/get-podcast-episodes/${feedId}`);
//     const json = await res.json();
//     console.log(json);
//     renderEpisodes(json);
// }

async function getPodcast(feedId) {
    const res = await fetch(`/get-podcast-info/${feedId}`);
    const json = await res.json();
    console.log(json);
    renderPodcast(json.podcast);
    renderEpisodes(json.episodes);
}

function renderPodcast(podcastData) {
    // @temp
    const html = `<div class="art">
        <img class="podcast-artwork" src="${podcastData[5]}" alt="" />
    </div>
    <div class="info-text">
        <div class="title">${podcastData[1]}</div>
        <div class="author">${podcastData[4]}</div>
        <div class="description">${podcastData[3]}</div>
    </div>`;
    document.querySelector(".info-banner").innerHTML = html;
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
    const prop = [idx, data[1], formatDate(data[4]), "Not Downloaded", ""];

    prop.forEach(item => {
        const td = document.createElement("td");
        // @temp
        if (item === "") {
            const img = document.createElement("img");
            img.setAttribute("src", "../static/icons/play.svg");
            img.setAttribute("style", "color: dodgerblue;");
            td.appendChild(img);
        } else {
            const textEl = document.createTextNode(item);
            td.appendChild(textEl);
        }
        row.appendChild(td);
    });

    return row;
}

window.onload = async () => {
    // getEpisodes(window.feedId);
    getPodcast(window.feedId);
    // console.log("Working")
}