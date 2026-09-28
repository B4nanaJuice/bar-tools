function addTagToSearch(selectNode, tagType) {

    let tag = document.createElement('span');
    tag.classList.add(tagType);
    tag.id = selectNode.value;
    tag.index = selectNode.selectedIndex;
    tag.innerText = selectNode.options[selectNode.selectedIndex].text;

    tag.onclick = function(e) {
        selectNode.options[e.target.index].hidden = null;
        e.target.remove(); 
    };
    selectNode.options[selectNode.selectedIndex].hidden = "hidden";
    selectNode.selectedIndex = 0;

    document.querySelector(`.${tagType}-list`).appendChild(tag);
}

function startSearch() {
                            
    let ingredients = [...document.querySelector('.ingredient-list').querySelectorAll('span')].map(c => c.id);
    let tags = [...document.querySelector('.tag-list').querySelectorAll('span')].map(c => c.id);
    let name = document.querySelector('.name-search input').value;

    let target = new URL(window.location);
    target.searchParams.delete('page')

    ingredients.length != 0 ? target.searchParams.set('ingredients', ingredients.join(',')) : target.searchParams.delete('ingredients');
    tags.length != 0 ? target.searchParams.set('tags', tags.join(',')) : target.searchParams.delete('tags');
    name != "" ? target.searchParams.set('name', name) : target.searchParams.delete('name');

    window.location = target;
}