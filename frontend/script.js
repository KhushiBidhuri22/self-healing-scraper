const API_BASE = "https://self-healing-scraper-1.onrender.com";


async function loadDashboard() {
    const healthScore = document.getElementById("healthScore");
    const healthRingValue = document.getElementById("healthRingValue");
    const healthStatus = document.getElementById("healthStatus");

    try {
        healthStatus.textContent = "Checking scraper health...";

        const [itemsResponse, driftResponse] = await Promise.all([
            fetch(`${API_BASE}/items?limit=100`),
            fetch(`${API_BASE}/drift`)
        ]);

        if (!itemsResponse.ok) {
            throw new Error("Products API request failed");
        }

        if (!driftResponse.ok) {
            throw new Error("Drift API request failed");
        }

        const itemsData = await itemsResponse.json();
        const driftData = await driftResponse.json();

        const products = itemsData.items || [];
        const repairs = driftData.repairs || [];
        const metrics = driftData.metrics || {};

        updateProducts(products);
        updateRepairs(repairs);
        updateStats(products, repairs, metrics);
        updateHealth(products);

    } catch (error) {
        console.error("Dashboard error:", error);

        healthScore.textContent = "--%";
        healthRingValue.textContent = "--%";
        healthStatus.textContent = "Unable to connect to scraper API";

        document.getElementById("productsList").innerHTML =
            '<div class="loading">Unable to load products.</div>';

        document.getElementById("repairsList").innerHTML =
            '<div class="loading">Unable to load repairs.</div>';

        document.getElementById("productBadge").textContent = "Offline";
        document.getElementById("repairBadge").textContent = "Offline";
    }
}


function updateProducts(products) {
    const container = document.getElementById("productsList");
    const badge = document.getElementById("productBadge");

    container.innerHTML = "";

    badge.textContent = `${products.length} products`;

    if (products.length === 0) {
        container.innerHTML =
            '<div class="loading">No products found.</div>';
        return;
    }

    products.forEach((product) => {
        const card = document.createElement("div");

        card.className = "product-card";

        card.innerHTML = `
            <div>
                <strong>${escapeHtml(product.name || "Unknown Product")}</strong>
            </div>

            <span class="product-price">
                ${escapeHtml(product.price || "N/A")}
            </span>
        `;

        container.appendChild(card);
    });
}


function updateRepairs(repairs) {
    const container = document.getElementById("repairsList");
    const badge = document.getElementById("repairBadge");

    container.innerHTML = "";

    badge.textContent = `${repairs.length} repairs`;

    if (repairs.length === 0) {
        container.innerHTML =
            '<div class="loading">No repairs recorded yet.</div>';
        return;
    }

    repairs
        .slice()
        .reverse()
        .forEach((repair) => {
            const row = document.createElement("div");

            row.className = "repair-row";

            row.innerHTML = `
                <div class="repair-main">
                    <strong>
                        ${escapeHtml(repair.field || "Unknown field")}
                    </strong>

                    <small>
                        ${escapeHtml(repair.old_selector || "N/A")}
                        →
                        ${escapeHtml(repair.new_selector || "N/A")}
                    </small>
                </div>

                <div class="repair-score">
                    ${repair.score ?? 0}
                </div>
            `;

            container.appendChild(row);
        });
}


function updateStats(products, repairs, metrics) {
    document.getElementById("productCount").textContent =
        products.length;

    document.getElementById("repairCount").textContent =
        metrics.total_repairs ?? repairs.length;

    const versions = products
        .map((product) => product.selector_version)
        .filter((version) => version !== undefined);

    const currentVersion =
        versions.length > 0
            ? Math.max(...versions)
            : "--";

    document.getElementById("selectorVersion").textContent =
        currentVersion;
}


function updateHealth(products) {
    let validProducts = 0;

    products.forEach((product) => {
        const hasName =
            product.name &&
            product.name.trim() !== "";

        const hasPrice =
            product.price &&
            product.price.trim() !== "";

        if (hasName && hasPrice) {
            validProducts++;
        }
    });

    const health =
        products.length > 0
            ? Math.round((validProducts / products.length) * 100)
            : 0;

    document.getElementById("healthScore").textContent =
        `${health}%`;

    document.getElementById("healthRingValue").textContent =
        `${health}%`;

    const statusElement =
        document.getElementById("healthStatus");

    if (health >= 90) {
        statusElement.textContent =
            "Scraper is healthy and operating normally.";
    } else if (health >= 50) {
        statusElement.textContent =
            "Scraper is degraded and may require attention.";
    } else {
        statusElement.textContent =
            "Scraper is critically degraded.";
    }
}


function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


loadDashboard();