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
    if (!rawResponse.ok) {
        console.error(rawResponse);
        throw new Error("Something went wrong...");
    }

    const content: any = await rawResponse.json();
    content.status = rawResponse.status;

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
    if (!rawResponse.ok) {
        console.error(rawResponse);
        throw new Error("Something went wrong...");
    }

    const content: any = await rawResponse.json();
    content.status = rawResponse.status;

    return content;
}