const mainEl = document.getElementById("main");

window.onload = async () => {
    const feeds = await getFeeds();

    Object.keys(feeds).forEach(key => {
        mainEl.appendChild(createCard(feeds[key]));
    });
}

async function getFeeds() {
    const res = await fetch("/feeds");
    const json = await res.json();
    return json;
}

function createCard(podcast) {
    const el = document.createElement("div");
    el.classList.add("card");
    el.innerHTML = `
        <img class="card-image" src="${podcast.artwork}" alt="${podcast.title}" />
        <div class="card-body">
            <a href="viewfeed/${podcast.id}" class="title">
                ${podcast.title}
            </a>
            <div class="desc">
                ${truncateString(podcast.description)}
            </div>
        </div>
    `;
    return el;
}

function truncateString(str, length = 150) {
    if (str.length <= length) return str;
    return str.slice(0, length - 2).concat("...");
}