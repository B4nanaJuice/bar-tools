import { APIGet, APIPost, Cocktail, createPopup, successNotification } from "./utils.js";

// CONFIG
export function updateIngredientCategory(ingredientId: number, category: string) {
    (async () => {
        const result = await APIPost(
            '/api/update-ingredient-category',
            {
                "ingredient_id": ingredientId,
                "category": category
            }
        );

        successNotification("Catégorie changée", result.message);
    })();
}

export function updateIngredientColor(ingredientId: number, color: string) {
    (async () => {
        const result = await APIPost(
            '/api/update-ingredient-color',
            {
                "ingredient_id": ingredientId,
                "color": color.replace("#", "")
            }
        );

        successNotification("Couleur changée", result.message);
        (document.querySelector(`.pill-ingredient-${ingredientId}`) as HTMLSpanElement).style.backgroundColor = `#${result.color}`;
    })();
}

export function updateTagColor(tagId: number, color: string) {
    (async () => {
        const result = await APIPost(
            '/api/update-tag-color',
            {
                "tag_id": tagId,
                "color": color.replace("#", "")
            }
        );

        successNotification("Couleur changée", result.message);
        (document.querySelector(`.pill-tag-${tagId}`) as HTMLSpanElement).style.backgroundColor = `#${result.color}`;
    })();
}

// ORDER MANAGEMENT
export function showRecipe(cocktailId: number) {
    (async () => {
        const result: {cocktail: Cocktail} = await APIGet(`/api/get-cocktail?cocktail-id=${cocktailId}`);

        createPopup(
            result.cocktail.name,
            `
                <ul>
                    ${result.cocktail.ingredients.map(ing => `<li>${ing.quantity} ${ing.unit} ${ing.name}</li>`).join('')}
                </ul>
            `
        );
    })();
}

export function updateOrderStatus(orderId: number, status: string) {
    (async () => {
        const result: {message: string, state: string} = await APIPost(
            '/api/update-order-status',
            {
                "order_id": orderId,
                "status": status
            }
        );

        successNotification("Statut changé", result.message);
        let orderRow: HTMLTableRowElement = <HTMLTableRowElement>document.querySelector(`.order-${orderId}`);
        result.state == "finished" ? orderRow.classList.add("finished-order") : orderRow.classList.remove("finished-order");
    })();
}