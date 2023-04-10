class NavBar extends HTMLElement {
    constructor() {
        super();
        this.innerHTML = `<ul><li><a href="/add/new">Add Podcast</a></li><li><a href="/">View Podcasts</a></li><li><a href="/settings">Settings</a></li></ul>`;
    }
}

class HeadEl extends HTMLElement {
    constructor() {
        super();
        this.innerHTML = `<div class="logo">Podcast Manager</div>`;
    }
}

customElements.define("nav-bar", NavBar, { extends: "section" });
customElements.define("head-el", HeadEl, { extends: "header" });