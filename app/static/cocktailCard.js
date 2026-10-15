function generateCardTitle(sourceScript, text) {
    let parent = sourceScript.parentElement;
    let padding = 32;
    let maxSize = parent.offsetWidth - padding;
    let target = parent.querySelector('.card-title');
    let fontSize = parseInt(window.getComputedStyle(target).getPropertyValue('font-size').replace("px", "")); // "36px" or "24px"
    let testBox = document.getElementById('adaptive-test-box');

    testBox.innerText = text;
    testBox.style.fontSize = `${fontSize}px`;
    while (testBox.offsetWidth > maxSize) {
        fontSize--;
        testBox.style.fontSize = `${fontSize}px`;
    }

    target.innerText = text;
    target.style.fontSize = `${fontSize}px`;
}

function showCocktailDetails(cocktailId) {
    (async () => {
        const rawResponse = await fetch(`/api/get-cocktail?cocktail-id=${cocktailId}`, {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });

        const content = await rawResponse.json();

        if (rawResponse.status == 200) {
            document.querySelector('.popup-title').innerText = content.cocktail.name;
            document.querySelector('.popup-description').innerHTML = `
                <div class="pill-box">
                    ${content.cocktail.tags.map(tag => `<span class="pill" style="background-color: ${tag.color}">${tag.name}</span>`).join('')}
                </div>
                <ul style="margin-top: 24px;">
                    ${content.cocktail.ingredients.map(ing => `<li>${ing.name}</li>`).join('')}
                </ul>
            `;

            document.querySelector('.popup-content .primary-button').onclick = (e) => {
                addCocktailToOrder(content.cocktail.name, content.cocktail.id);
                document.querySelector('.popup').classList.remove('popup-open');
            }

            document.querySelector('.popup-content .primary-button p').innerText = "Ajouter";

            document.querySelector('.popup').classList.add('popup-open');
        } else {
            createNotification("error", "Woops", "Quelque chose s'est mal passé...");
        }
    })();
}