chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    if (changeInfo.status === "loading" && tab.url?.startsWith("http")) {
        try {
            const response = await fetch("http://127.0.0.1:5000/check_url", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: tab.url })
            });

            const result = await response.json();

            if (result.phishing) {
                chrome.tabs.update(tabId, {
                    url: chrome.runtime.getURL("block.html")
                });
            }
        } catch (e) {
            console.error("API error", e);
        }
    }
});

/* 👇 THIS PART IS CRITICAL */
chrome.runtime.onMessage.addListener((message, sender) => {
    if (message.action === "close_tab") {
        if (sender.tab && sender.tab.id) {
            chrome.tabs.remove(sender.tab.id);
        }
    }
});
