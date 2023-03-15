async function getEpisodes(feedId) {
    const res = await fetch(`/get-podcast-episodes/${feedId}`);
    const json = await res.json();
    if (json.length > 0) renderEpisodes(json);
}

function renderEpisodes(episodes) {
    const epEl = document.querySelector("tbody.episodes");
    // epEl.children.forEach(child => child.remove());

    epEl.innerHTML = "";

    episodes.forEach((ep, idx) => {
        let row = buildRow(ep, episodes.length - idx);
        epEl.appendChild(row);
    });

}

function buildRow(data, idx) {
    const row = document.createElement("tr");
    const prop = [idx, data[1], data[4], "Not Downloaded", ""];

    prop.forEach(item => {
        const td = document.createElement("td");
        const textEl = document.createTextNode(item);
        td.appendChild(textEl);
        row.appendChild(td);
    });

    return row;
}

window.onload = async () => {
    // console.log(window.feedId);
    getEpisodes(window.feedId);
}