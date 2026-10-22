import { APIGet, createPopup, Cocktail, OrderItem, APIPost, successNotification, OrderStatus } from "./utils.js";

export function showCocktailDetails(cocktailId: number) {
    (async () => {
        const result: {cocktail: Cocktail} = await APIGet(`/api/get-cocktail?cocktail-id=${cocktailId}`);
        
        createPopup(
            result.cocktail.name,
            `
                <div class="pill-box">
                    ${result.cocktail.tags.map(tag => `<span class="pill" style="background-color: ${tag.color}">${tag.name}</span>`).join('')}
                </div>
                <ul style="margin-top: 24px;">
                    ${result.cocktail.ingredients.map(ing => `<li>${ing.name}</li>`).join('')}
                </ul>
            `,
            "Ajouter",
            () => { addCocktailToOrder(result.cocktail); }
        );
    })();
}

export function addCocktailToOrder(cocktail: Cocktail) {
    let order: Array<OrderItem> = getCurrentOrder();
    let targetItem: OrderItem | undefined = order.find(o => o.cocktail.id == cocktail.id);

    if (targetItem) {
        addCocktailQuantity(cocktail, 1);

    } else {
        targetItem = <OrderItem>{ cocktail: cocktail, quantity: 1 };
        order.push(targetItem);
        localStorage.setItem("order", JSON.stringify(order));
        refreshOrderTable();
    }
}

export function getCurrentOrder(): Array<OrderItem> {
    console.log(localStorage.getItem("order"));
    return <Array<OrderItem>>JSON.parse(localStorage.getItem("order") || "[]");
}

export function addCocktailQuantity(cocktail: Cocktail, quantity: number) {
    let order: Array<OrderItem> = getCurrentOrder();
    for (let item of order) {
        if (item.cocktail.id == cocktail.id) {
            item.quantity = Math.min(Math.max(1, item.quantity + quantity), 9);
        }
    }
    localStorage.setItem("order", JSON.stringify(order));
    refreshOrderTable();
}

export function setCocktailQuantity(cocktail: Cocktail, quantity: number) {
    let order: Array<OrderItem> = getCurrentOrder();
    for (let item of order) {
        if (item.cocktail.id == cocktail.id) {
            item.quantity = Math.min(Math.max(1, quantity), 9);
        }
    }
    localStorage.setItem("order", JSON.stringify(order));
    refreshOrderTable();
}

export function removeCocktailFromOrder(cocktail: Cocktail) {
    let order: Array<OrderItem> = getCurrentOrder();
    order = order.filter(o => o.cocktail.id != cocktail.id);
    localStorage.setItem("order", JSON.stringify(order));
    refreshOrderTable();
}

export function refreshOrderTable() {

    let orderSection: HTMLDivElement = <HTMLDivElement>document.querySelector('.navbar-orders');
    let orderTable: HTMLTableElement = <HTMLTableElement>orderSection.querySelector('table');
    let orderForm: HTMLDivElement = <HTMLDivElement>orderSection.querySelector('.form-row');
    let currentOrder: OrderItem[] = getCurrentOrder();

    orderTable.style.display = currentOrder.length == 0 ? 'none' : 'block';
    orderForm.style.display = currentOrder.length == 0 ? 'none' : 'flex';

    orderTable.innerHTML = `
        <tr>
            <th>Cocktail</th>
            <th class="text-right" style="width: 20%">Quantité</th>
            <th class="text-right" style="width: 10%">Supprimer</th>
        </tr>
    `;

    let cartSize: number = 0;

    for (let orderItem of currentOrder) {

        cartSize += orderItem.quantity;
        let tableRow: HTMLTableRowElement = document.createElement('tr');

        let cocktailNameCell: HTMLTableCellElement = document.createElement('td');
        cocktailNameCell.innerText = orderItem.cocktail.name;
        tableRow.appendChild(cocktailNameCell);

        let quantityChoiceCell: HTMLTableCellElement = document.createElement('td');
        quantityChoiceCell.classList.add("text-right");
        let quantityChoiceCellDiv: HTMLDivElement = document.createElement('div');

        let removeQuantityButton: HTMLButtonElement = document.createElement('button');
        removeQuantityButton.innerHTML = `
            <svg width="16" height="2" viewBox="0 0 16 2" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 1H15" stroke="#FCF9FE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
        removeQuantityButton.classList.add("icon-only");
        if (orderItem.quantity == 1) removeQuantityButton.classList.add("muted");
        removeQuantityButton.addEventListener("click", (event: PointerEvent) => {
            addCocktailQuantity(orderItem.cocktail, -1);
        });

        let addQuantityButton: HTMLButtonElement = document.createElement('button');
        addQuantityButton.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 1V15M1 8H15" stroke="#FCF9FE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
        addQuantityButton.classList.add("icon-only");
        if (orderItem.quantity == 9) addQuantityButton.classList.add("muted");
        addQuantityButton.addEventListener("click", (event: PointerEvent) => {
            addCocktailQuantity(orderItem.cocktail, 1);
        });

        let quantityIndicator: HTMLParagraphElement = document.createElement('p');
        quantityIndicator.style.width = '32px';
        quantityIndicator.style.margin = '0 12px';
        quantityIndicator.style.textAlign = 'center';
        quantityIndicator.innerText = `${orderItem.quantity}`;

        quantityChoiceCellDiv.appendChild(removeQuantityButton);
        quantityChoiceCellDiv.appendChild(quantityIndicator);
        quantityChoiceCellDiv.appendChild(addQuantityButton);
        quantityChoiceCell.appendChild(quantityChoiceCellDiv);
        tableRow.appendChild(quantityChoiceCell);

        let removeCocktailCell: HTMLTableCellElement = document.createElement('td');
        removeCocktailCell.classList.add("text-right");
        let removeCocktailCellDiv: HTMLDivElement = document.createElement('div');

        let removeCocktailButton: HTMLButtonElement = document.createElement('button');
        removeCocktailButton.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 20 22" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 5H3M3 5H19M3 5V19C3 19.5304 3.21071 20.0391 3.58579 20.4142C3.96086 20.7893 4.46957 21 5 21H15C15.5304 21 16.0391 20.7893 16.4142 20.4142C16.7893 20.0391 17 19.5304 17 19V5M6 5V3C6 2.46957 6.21071 1.96086 6.58579 1.58579C6.96086 1.21071 7.46957 1 8 1H12C12.5304 1 13.0391 1.21071 13.4142 1.58579C13.7893 1.96086 14 2.46957 14 3V5M8 10V16M12 10V16" stroke="#FCF9FE" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
        removeCocktailButton.classList.add("icon-only");
        removeCocktailButton.addEventListener("click", (event: PointerEvent) => {
            removeCocktailFromOrder(orderItem.cocktail);
        });

        removeCocktailCellDiv.appendChild(removeCocktailButton);
        removeCocktailCell.appendChild(removeCocktailCellDiv);
        tableRow.appendChild(removeCocktailCell);

        orderTable.appendChild(tableRow);
    }

    let cartSizeIndicator: HTMLDivElement = <HTMLDivElement>document.querySelector(".cart-size");
    cartSizeIndicator.style.display = cartSize == 0 ? 'none' : 'block';
    cartSizeIndicator.innerText = cartSize > 9 ? '9+' : `${cartSize}`;
}

export function checkOrder(): boolean {
    let order: Array<OrderItem> = getCurrentOrder();
    if (order.length < 1) return false;

    let name: string = (document.querySelector('.order-name input') as HTMLInputElement).value;
    if (name.trim().length < 1) return false;

    return true;
}

export function placeOrder() {
    if (!checkOrder()) return;

    let order: Array<OrderItem> = getCurrentOrder();
    let orderNameInput: HTMLInputElement = <HTMLInputElement>document.querySelector('.order-name input');
    createPopup(
        "Valider la commande ?",
        `
            <ul>
                ${order.map(o => `<li>${o.quantity} ${o.quantity}</li>`).join('')}
            </ul>
        `,
        "Valider",
        () => {(async () => {
            const result = await APIPost(
                "/api/send-order",
                {name: orderNameInput.value, order: order}
            );

            successNotification("Commande passée !", "Ta commande a bien été validée !");
            localStorage.setItem("Order", JSON.stringify([]));
            followNewOrder(result.orderId);
            document.querySelector('.navbar')!.classList.remove('navbar-for-orders');
            orderNameInput.value = '';
            refreshOrderTable();
        })}
    );
}

function followNewOrder(orderId: number) {
    // Add new order to local storage
    let orders: number[] = <number[]>JSON.parse(localStorage.getItem("orders") || "[]");
    orders.push(orderId);
    localStorage.setItem('orders', JSON.stringify(orders));
    // Create new order status bar
    addOrderStatus(orderId);
}

export function addOrderStatus(orderId: number) {
    // Add html elements to the navbar
    let div: HTMLDivElement = <HTMLDivElement>document.createElement('div');
    div.classList.add(`order-${orderId}`);
    div.innerHTML = `
        <h1 style="font-weight: 300; margin-top: 48px;">Commande n° ${orderId} : <span class="status-${orderId}" style="font-weight: 900;"></span></h1>
        <div class="progress-bar progress-bar-${orderId}" style="width: 100%; margin: auto;">
            <div class="bar"></div>
        </div>
    `;
    document.querySelector('.order-status')!.appendChild(div);
    // Refresh the status
    refreshOrderStatus(orderId);
}

function refreshOrderStatus(orderId: number) {
    // Fetch API until status is finished (recursive function)
    (async () => {
        const result: {state: OrderStatus} = await APIGet(`/api/get-order-status?order-id=${orderId}`);
        let statusLabel: HTMLSpanElement = <HTMLSpanElement>document.querySelector(`.status-${orderId}`);
        let progressBar: HTMLDivElement = <HTMLDivElement>document.querySelector(`.progress-bar-${orderId} .bar`);

        switch (result.state.state) {
            case "new":
                statusLabel.innerText = "En attente";
                progressBar.style.width = "20%";
                setTimeout(() => { refreshOrderStatus(orderId); }, 5000);
                break;

            case "pending":
                statusLabel.innerText = "En cours";
                progressBar.style.width = "60%";
                setTimeout(() => { refreshOrderStatus(orderId); }, 5000);
                break;

            case "finished":
                statusLabel.innerText = "Terminée";
                progressBar.style.width = "100%";
                break;
        }
    })();
}