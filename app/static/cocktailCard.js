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

function showCocktailDetails(cocktailName, cocktailId, cocktailTags, cocktailIngredients) {
    document.querySelector('.popup-title').innerText = cocktailName;
    document.querySelector('.popup-description').innerHTML = `
        <p style="font-size: 28px;">Tags</p>
        <p>${cocktailTags.join(' • ')}</p>
        <p style="font-size: 28px; margin-top: 12px;">Ingrédients</p>
        <p>${cocktailIngredients.join(' • ')}</p>
    `;

    document.querySelector('.popup-content .primary-button').onclick = (e) => {
        addCocktailToOrder(cocktailName, cocktailId);
        document.querySelector('.popup').classList.remove('popup-open');
    }

    document.querySelector('.popup-content .primary-button p').innerText = "Ajouter";

    document.querySelector('.popup').classList.add('popup-open');
}