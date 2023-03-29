const mainEl = document.getElementById("main");

window.onload = async () => {
    const feeds = await getFeeds();

    feeds.forEach(feed => {
        mainEl.appendChild(createCard(feed));
    });
}

async function getFeeds() {
    const res = await fetch("/feeds");
    const json = await res.json();
    return json.feeds;
}

function createCard(podcast) {
    const el = document.createElement("div");
    el.classList.add("card");
    el.innerHTML = `
        <img class="card-image" src="${podcast[5]}" alt="${podcast[1]}" />
        <div class="card-body">
            <a href="viewfeed/${podcast[0]}" class="title">
                ${truncateString(podcast[1], 40)}
            </a>
            
        </div>
    `;
    return el;
}

function truncateString(str, length = 150) {
    if (str.length <= length) return str;
    return str.slice(0, length - 2).concat("...");
}