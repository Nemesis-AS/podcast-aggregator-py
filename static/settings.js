window.onload = () => { main() };

const formFields = ["download_dir"];

function main() {
    const saveBtn = document.getElementById("saveBtn");
    saveBtn.addEventListener("click", e => {
        saveSettings();
    });

    populateSettings(fetchSettings());
}

function saveSettings() {
    const settings = serializeSettings();
    fetch("/config", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(settings),
    }).then(res => {
        if (res.status === 200) console.log("Settings Saved!");
    });
}

function fetchSettings() {
    fetch("/config").then(res => res.json()).then(json => {
        populateSettings(json);
    });
}

function serializeSettings() {
    let data = {};
    formFields.forEach(field => {
        const el = document.getElementById(field);
        data[field] = el.value;
    });

    return data;
}

function populateSettings(settings) {
    if (!settings) return;
    // @tip Works only for Input type text elements
    Object.keys(settings).forEach(setting => {
        const el = document.getElementById(setting);
        if (!el) return;
        el.value = settings[setting];
    });
}