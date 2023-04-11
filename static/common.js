class NavBar extends HTMLElement {
    constructor() {
        super();

        const url = new URL(window.location);
        const list = document.createElement("ul");
        const items = [["/add/new", "Add Podcast"], ["/", "View Podcasts"], ["/settings", "Settings"]];

        items.forEach(item => {
            const li = document.createElement("li");
            const a = document.createElement("a");
            a.href = item[0];
            if (url.pathname == item[0]) li.classList.add("active");
            a.appendChild(document.createTextNode(item[1]));
            li.appendChild(a);
            list.appendChild(li);
        });

        this.appendChild(list);
    }
}

class HeadEl extends HTMLElement {
    constructor() {
        super();

        const logo = document.createElement("div");
        logo.classList.add("logo");
        const logoText = document.createTextNode("Podcast Manager");
        logo.appendChild(logoText);
        this.appendChild(logo);
    }
}

// <toast data-text="Some Text" data-type="success" />
class Toast extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        const text = document.createTextNode(this.dataset.text);
        const closeBtn = document.createElement("button");
        closeBtn.addEventListener("click", e => this.close());
        closeBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16"><path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/></svg>`;

        this.appendChild(text);
        this.appendChild(closeBtn);
        this.classList.add(this.dataset.type);

        setTimeout(() => {
            if (!this) return;
            this.close();
        }, 5000);
    }

    close() {
        this.classList.remove("show");
        setTimeout(() => this.remove(), 900);
    }
}

customElements.define("nav-bar", NavBar, { extends: "section" });
customElements.define("head-el", HeadEl, { extends: "header" });
customElements.define("toast-el", Toast);

function addToast(text, color) {
    const toast = document.createElement("toast-el");
    toast.dataset.text = text;
    toast.dataset.type = color;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add("show"), 10);
}