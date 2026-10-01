function placeOrder() {
                            
    let name = document.querySelector('.order-name input').value;
    if (name == "") {
        createNotification("error", "Champ vide", "Il faut indiquer un nom, sinon comment savoir que c'est ta commande ?");
        return;
    }

    if (localStorage.length < 1) {
        createNotification("error", "Commande vide", "Il faut sélectionner au moins 1 cocktail pour pouvoir passer commande.");
        return;
    }

    document.querySelector('.popup-title').innerText = "Valider la commande ?";
    document.querySelector('.popup-description').innerText = "order items here";

    document.querySelector('.popup-content .primary-button').onclick = (e) => {
        let order = { name: name };
        let toRemove = [];
        for (let i = 0; i < localStorage.length; i++) {
            let key = localStorage.key(i);
            console.log(`key: ${key}`)
            if (key.match(/^[0-9]*_.*$/)) {
                console.log('The key matches !')
                let cocktailId = key.split('_')[0];
                let quantity = localStorage.getItem(key);

                order[cocktailId] = quantity;
                toRemove.push(key);
            }
        }

        // Send command to api
        (async () => {
            const rawResponse = await fetch('/api/send-order', {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(order)
            });

            console.log(rawResponse)

            const content = await rawResponse.json();

            if (rawResponse.status == 200) {
                createNotification("success", "Commande passée", "Ta commande a bien été validée. Attends un peu et les boissons arriveront à toi !");
                document.querySelector('.navbar').classList.remove('navbar-for-cart');
                document.querySelector('.order-name input').value = '';

                for (let i = 0; i < toRemove.length; i++) {
                    localStorage.removeItem(toRemove[i]);
                }

                refreshOrderTable();
            } else {
                createNotification("error", "Woops", content.message);
                refreshOrderTable();
            }
        })();
        document.querySelector('.popup').classList.remove('popup-open');
    }
    document.querySelector('.popup-content .primary-button p').innerText = "Valider";

    document.querySelector('.popup').classList.add('popup-open');
}

function addCocktailToOrder(cocktailName, cocktailId) {
    let key = `${cocktailId}_${cocktailName}`;
    let newQuantity = parseInt(localStorage.getItem(key) || 0) + 1;
    localStorage.setItem(key, newQuantity);

    refreshOrderTable();
}

function refreshOrderTable() {

    let orderTable = document.querySelector('.navbar-cart table');
    orderTable.innerHTML = `
        <tr>
            <th>Cocktail</th>
            <th>Quantité</th>
            <th>Supprimer</th>
        </tr>
    `;

    let cartSize = 0;

    for (let i = 0; i < localStorage.length; i++) {

        let key = localStorage.key(i);
        if (key.match(/^[0-9]*_.*$/)) {
            let [cocktailId, cocktailName] = key.split('_');
            let quantity = parseInt(localStorage.getItem(key) || 1);
            cartSize += parseInt(quantity);

            let tableRow = document.createElement('tr');

            tableRow.innerHTML = `
                <td>${cocktailName}</td>
                <td>
                    <div>
                        <button class="${quantity == 1 ? 'muted' : ''} icon-only" onclick="removeCocktailQuantity('${key}')">
                            <svg width="16" height="2" viewBox="0 0 16 2" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M1 1H15" stroke="#FCF9FE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <p class="order-quantity">${quantity}</p>
                        <button class="icon-only" onclick="addCocktailQuantity('${key}')">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M8 1V15M1 8H15" stroke="#FCF9FE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                </td>
                <td>
                    <div>
                        <button class="icon-only" onclick="removeCocktailFromOrder('${key}')">
                            <svg width="24" height="24" viewBox="0 0 20 22" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M1 5H3M3 5H19M3 5V19C3 19.5304 3.21071 20.0391 3.58579 20.4142C3.96086 20.7893 4.46957 21 5 21H15C15.5304 21 16.0391 20.7893 16.4142 20.4142C16.7893 20.0391 17 19.5304 17 19V5M6 5V3C6 2.46957 6.21071 1.96086 6.58579 1.58579C6.96086 1.21071 7.46957 1 8 1H12C12.5304 1 13.0391 1.21071 13.4142 1.58579C13.7893 1.96086 14 2.46957 14 3V5M8 10V16M12 10V16" stroke="#FCF9FE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                </td>
            `;

            orderTable.appendChild(tableRow);
        }
    }

    cartSize == 0 ? document.querySelector(".cart-size").style.display = 'none' : document.querySelector(".cart-size").style.display = 'block';
    cartSize > 9 ? document.querySelector(".cart-size").innerText = '9+' : document.querySelector(".cart-size").innerText = `${cartSize}`;
}

function addCocktailQuantity(key) {
    let newQuantity = parseInt(localStorage.getItem(key) || 0) + 1;
    localStorage.setItem(key, newQuantity);

    refreshOrderTable();
}

function removeCocktailQuantity(key) {
    let newQuantity = parseInt(localStorage.getItem(key) || 0) - 1;
    localStorage.setItem(key, newQuantity < 1 ? 1 : newQuantity);

    refreshOrderTable();
}

function removeCocktailFromOrder(key) {
    localStorage.removeItem(key)
    refreshOrderTable();
}

refreshOrderTable();