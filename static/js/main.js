(function () {
    const loadMoreButton = document.querySelector("[data-load-more]");
    const cards = document.getElementById("results-cards");
    const shownCount = document.getElementById("shown-count");

    if (!loadMoreButton || !cards) {
        return;
    }

    const subject = cards.dataset.subject || "";
    let nextOffset = Number(cards.dataset.nextOffset || "0");
    const total = Number(cards.dataset.total || "0");

    const setButtonState = (loading) => {
        loadMoreButton.disabled = loading;
        loadMoreButton.textContent = loading ? "Loading..." : "Show more results";
    };

    const formatList = (items, emptyLabel) => {
        if (!items || items.length === 0) {
            return emptyLabel;
        }
        return items.join(", ");
    };

    const createCard = (record) => {
        const card = document.createElement("div");
        card.className = "subject-card";

        const title = document.createElement("h3");
        title.textContent = record.title || "Untitled";
        card.appendChild(title);

        const subjects = document.createElement("p");
        subjects.textContent = `Subjects: ${formatList(record.subjects, "None")}`;
        card.appendChild(subjects);

        const contributors = document.createElement("p");
        contributors.textContent = `Contributors: ${formatList(record.contributors, "None")}`;
        card.appendChild(contributors);

        const created = document.createElement("p");
        created.textContent = `Created: ${record.created || "Unknown"}`;
        card.appendChild(created);

        return card;
    };

    loadMoreButton.addEventListener("click", async () => {
        if (!subject) {
            return;
        }

        setButtonState(true);
        let hadError = false;

        try {
            const params = new URLSearchParams({
                subject,
                offset: String(nextOffset)
            });
            const response = await fetch(`/load-more?${params.toString()}`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Failed to load more results.");
            }

            const records = data.records || [];
            records.forEach((record) => {
                cards.appendChild(createCard(record));
            });

            nextOffset += records.length;
            if (shownCount) {
                shownCount.textContent = String(nextOffset);
            }

            if (records.length === 0 || nextOffset >= total) {
                loadMoreButton.style.display = "none";
            }
        } catch (err) {
            hadError = true;
            loadMoreButton.textContent = "Couldn't load more results";
            console.error("Load more error:", err);
        } finally {
            if (!hadError) {
                setButtonState(false);
            } else {
                loadMoreButton.disabled = false;
                // Reset button after delay to allow retry
                setTimeout(() => {
                    loadMoreButton.textContent = "Show more results";
                    loadMoreButton.disabled = false;
                }, 3000);
            }
        }
    });
})();
