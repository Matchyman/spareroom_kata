interface BasketItem {
  code: string
  quant: number
}

export async function getPrices(){
    const response = await fetch("http://localhost:8000/checkout/prices")
    if (!response.ok){
        throw new Error("Failed to get items")
    }
    return response.json();
}


export async function postBasket(basket: BasketItem[]){
    const response = await fetch("http://localhost:8000/checkout/",{
        method: "POST",
        headers:{
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(basket)
    })
    if (!response.ok){
        throw new Error("Failed to get items")
    }
    return response.json()
}