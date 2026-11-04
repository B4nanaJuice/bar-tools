import { APIGet, APIPost, Cocktail, createPopup, errorNotification, successNotification } from "./utils.js";

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

// COCKTAIL INFORMATION
function resizeImage(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
        const image: HTMLImageElement = new Image();
        const objectUrl: string = URL.createObjectURL(file);

        image.onload = () => {
            const canvas: HTMLCanvasElement = document.createElement('canvas');
            const width: number = 220, height: number = 220;

            canvas.width = width;
            canvas.height = height;

            const ctx = canvas.getContext('2d');
            if (!ctx) {
                URL.revokeObjectURL(objectUrl);
                errorNotification("Canvas non disponible", "Il y a eu un problème lors du chargement du canvas.");
                reject();
                return;
            }

            const size = Math.min(image.width, image.height);
            const sx = (image.width - size) / 2;
            const sy = (image.height - size) / 2;

            ctx.drawImage(image, sx, sy, size, size, 0, 0, width, height);

            const base64: string = canvas.toDataURL("image/jpeg", 0.85);
            URL.revokeObjectURL(objectUrl);
            resolve(base64);
        };

        image.onerror = () => {
            URL.revokeObjectURL(objectUrl);
            errorNotification("Erreur de l'image", "Impossible de charger l'image.");
            reject();
            return;
        }

        image.src = objectUrl;
    });
}

async function sendImage(cocktailId: number, base64Image: string) {
    const result: {message: string, image: string} = await APIPost(
        '/api/update-cocktail-image',
        {
            "cocktail_id": cocktailId,
            "image": base64Image
        }
    );

    successNotification("Image changée !", result.message);
    (document.querySelector('.image-preview') as HTMLImageElement).src = result.image; 
}

export function updateCocktailImage(cocktailId: number, file: File) {
    (async () => {
        // Check if file is image
        if (!file) return;
        const allowedTypes: Array<string> = ["image/png", "image/jpeg", "image/webp"];
        if (!allowedTypes.includes(file.type)) return errorNotification("Mauvais type", "Le fichier n'a pas la bonne extension.");
        if (file.size > 5*1024*1024) return errorNotification("Fichier trop volumineux", "La taille du fichier ne dois pas dépasser 5Mo.");
        // Resize image and convert to base64
        let base64Image = await resizeImage(file);
        // Send base64 to API
        await sendImage(cocktailId, base64Image);
    })();
}