import { APIGet, IngredientCategory, Ingredient, CocktailTag } from "./utils.js";

export function addTagToSearch(tagType: 'ingredient' | 'tag') {
    let selectNode: HTMLSelectElement = <HTMLSelectElement>document.getElementById(`${tagType}-search-select`)!;
    
    let tag: HTMLSpanElement = document.createElement('span');
    tag.classList.add("pill");
    tag.id = selectNode.value;
    tag.style.backgroundColor = <string>selectNode.options[selectNode.selectedIndex].getAttribute("data-color");
    tag.setAttribute("index", selectNode.selectedIndex.toString());
    tag.innerText = selectNode.options[selectNode.selectedIndex].text;

    tag.addEventListener("click", (event: PointerEvent) => {
        selectNode.options[parseInt((event.target as any).getAttribute("index"))].hidden = false;
        (event.target as HTMLElement).remove();
    })

    selectNode.options[selectNode.selectedIndex].hidden = true;
    selectNode.selectedIndex = 0;

    document.querySelector(`.${tagType}-list`)!.appendChild(tag);
}

export function startSearch() {
    let ingredients: string[] = ([...document.querySelectorAll('.ingredient-list span')] as Array<HTMLSpanElement>).map(c => c.id);
    let tags: string[] = ([...document.querySelectorAll('.tag-list span')] as Array<HTMLSpanElement>).map(c => c.id);
    let name: string = (document.querySelector('.name-search input') as HTMLInputElement).value;

    let target: URL = new URL(window.location.toString());
    target.searchParams.delete('page')

    ingredients.length != 0 ? target.searchParams.set('ingredients', ingredients.join(',')) : target.searchParams.delete('ingredients');
    tags.length != 0 ? target.searchParams.set('tags', tags.join(',')) : target.searchParams.delete('tags');
    name != "" ? target.searchParams.set('name', name) : target.searchParams.delete('name');

    target.hash = "body";
    (document.querySelector('.navbar') as HTMLDivElement).classList.remove('navbar-for-search');

    window.location.assign(target);
}

export function loadIngredients() {
    (async () => {
        const ingredients: {status: number, ingredients: Array<Ingredient>} = await APIGet("/api/get-ingredients");
        const ingredientCategories: {status: number, categories: Array<IngredientCategory>} = await APIGet("/api/get-ingredient-categories");
        const categories: {[key: string]: string} = {
            spirit: "Spiritueux",
            liquor: "Crèmes & liqueurs",
            juice: "Jus & bases fruits",
            syrup: "Sirops",
            other: "Autres"
        };

        document.getElementById("ingredient-search-select")!.innerHTML += ingredientCategories.categories
            .map((cat) => `<optgroup label="${categories[cat.name]}">${ingredients.ingredients
                    .filter(ing => ing.category.id == cat.id)
                    .map(ing => `<option value="${ing.id}" data-color="${ing.color}">${ing.name}</option>`)
                    .join('')}
                </optgroup>`)
            .join('');
    })();
}

export function loadTags() {
    (async () => {
        const tags: {status: number, tags: Array<CocktailTag>} = await APIGet("/api/get-tags");

        document.getElementById("tag-search-select")!.innerHTML += tags.tags
            .map((tag) => `<option value="${tag.id}" data-color="${tag.color}">${tag.name}</option>`)
            .join('');
    })();
}

(document.querySelector('.name-search input') as HTMLInputElement).addEventListener("keypress", (e) => {
    if (["Enter"].includes(e.key)) startSearch();
});