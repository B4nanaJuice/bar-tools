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