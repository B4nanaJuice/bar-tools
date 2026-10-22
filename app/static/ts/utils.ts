// Models
export interface CocktailIngredient extends Ingredient {
    quantity: number,
    unit: string
}

export interface CocktailTag {
    id: number,
    name: string,
    color: string
}

export interface Cocktail {
    id: number,
    name: string,
    description: string,
    image_url: string,
    glass: Glass,
    ingredients: CocktailIngredient[],
    tags: CocktailTag[]
}

export interface Glass {
    id: number,
    name: string
}

export interface Ingredient {
    id: number,
    name: string,
    is_available: boolean,
    color: string,
    category: IngredientCategory
}

export interface IngredientCategory {
    id: number,
    name: string
}

export interface OrderItem {
    id?: number,
    quantity: number,
    cocktail: Cocktail
}

export interface OrderStatus {
    id: number,
    state: string
}

export interface Order {
    id: number,
    customer_name: string,
    created_at: Date,
    items: OrderItem[],
    status: OrderStatus
}

// API Fetching
export async function APIGet(url: string): Promise<any> {
    let params: {method: string; headers: any} = {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }
    
    const rawResponse: Response = await fetch(url, params);
    const content: any = await rawResponse.json();
    content.status = rawResponse.status;

    if (!rawResponse.ok) {
        console.error(rawResponse);
        errorNotification("Woops", content.message);
        throw new Error("Something went wrong...");
    }

    return content;
}

export async function APIPost(url: string, body: Object | null = null): Promise<any> {
    let params: {method: string; headers: any; body: string} = {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    }
    
    const rawResponse: Response = await fetch(url, params);
    const content: any = await rawResponse.json();
    content.status = rawResponse.status;

    if (!rawResponse.ok) {
        console.error(rawResponse);
        errorNotification("Woops", content.message);
        throw new Error("Something went wrong...");
    }

    return content;
}

// Notifications
export function createNotification(type: 'success' | 'error', title: string, description: string, timeout: number = 3) {
    // Create element
    let notification: HTMLDivElement = document.createElement('div');
    notification.classList.add('notification', `notification-${type}`);

    // Add closing button
    notification.innerHTML = `
        <button class="icon-only" onclick="this.parentElement.remove();">
            <svg width="20" height="20" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M25 1L1 25M1 1L25 25" stroke="#1B1107" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </button>
    `;

    // Add notification title
    let notificationTitle: HTMLHeadingElement = document.createElement('h2');
    notificationTitle.classList.add('notification-title');
    notificationTitle.innerText = title;
    notification.appendChild(notificationTitle);

    // Add notification description
    let notificationDesc: HTMLParagraphElement = document.createElement('p');
    notificationDesc.classList.add('notification-description');
    notificationDesc.innerHTML = description;
    notification.appendChild(notificationDesc);

    // Add auto closing timer
    notification.innerHTML += `
        <div class="progress-bar" style="height: 4px; margin-top: 12px;">
            <div class="bar" style="height: 4px;"></div>
        </div>
    `;

    document.querySelector('.notifications')!.appendChild(notification);

    setTimeout(() => {
        (notification.querySelector('.progress-bar .bar') as HTMLDivElement).style.transition = `width ${timeout}s ease`;
        (notification.querySelector('.progress-bar .bar') as HTMLDivElement).style.width = '100%';

        setTimeout(() => {
            notification.remove();
        }, timeout * 1000);
    }, 100);
}

export function successNotification(title: string, description: string) {
    createNotification('success', title, description);
}

export function errorNotification(title: string, description: string) {
    createNotification('error', title, description);
}

// Popups
export function createPopup(title: string, body: string, actionLabel: string = "Valider", callback: CallableFunction | null = null) {
    // Get element
    let popup: HTMLDivElement = <HTMLDivElement>document.querySelector('.popup');

    // Set popup title
    let popupTitle: HTMLHeadingElement = <HTMLHeadingElement>popup.querySelector('.popup-title');
    popupTitle.innerText = title;

    // Set popup body
    let popupBody: HTMLHeadingElement = <HTMLHeadingElement>popup.querySelector('.popup-body');
    popupBody.innerHTML = body;

    // Set popup action
    let popupAction: HTMLButtonElement = <HTMLButtonElement>popup.querySelector('.primary-button');
    popupAction.onclick = (e) => {
        if (callback) callback();
        closePopup();
    };

    let popupActionLabel: HTMLParagraphElement = <HTMLParagraphElement>popupAction.querySelector('p');
    popupActionLabel.innerText = actionLabel;

    // Show popup
    popup.classList.add('popup-open');
}

export function closePopup() {
    let popup: HTMLDivElement = <HTMLDivElement>document.querySelector('.popup');
    popup.classList.remove('popup-open');
}

// Auto text resize
export function generateCardTitle(node: HTMLElement, content: string) {

    let parent: HTMLElement = <HTMLElement>node.parentElement;
    let padding: number = 32;
    let maxSize: number = parent.offsetWidth - padding;
    let fontSize: number = parseInt(window.getComputedStyle(node).getPropertyValue('font-size').replace("px", "")); // "36px" or "24px"
    let testBox: HTMLElement = <HTMLElement>document.getElementById('adaptive-test-box');

    testBox.innerText = content;
    testBox.style.fontSize = `${fontSize}px`;
    while (testBox.offsetWidth > maxSize) {
        fontSize--;
        testBox.style.fontSize = `${fontSize}px`;
    }

    node.style.fontSize = `${fontSize}px`;
}