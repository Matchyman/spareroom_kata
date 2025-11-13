import './App.css'
import {getPrices, postBasket} from './checkout.tsx'
import {useEffect, useState} from 'react'

interface Item {
  code: string
  price: number
}

interface BasketItem {
  code: string
  quant: number
}

function App() {
  const [items, setItems] = useState<Item[]>([])
  const [quantities, setQuantities] = useState<Record<string, number>>({})
  const [basket, setBasket] = useState<BasketItem[]>([])
  const [subtotal, setSubtotal] = useState<number|null>(null)
  
  const handleItemSubmit = async (e: React.FormEvent<HTMLFormElement>, itemCode: string) => {
    e.preventDefault()
    const quantity = quantities[itemCode] || 0
    
    if (quantity <= 0) return
    
    setBasket(prevBasket => {
      const existingItemIndex = prevBasket.findIndex(item => item.code === itemCode)
      
      if (existingItemIndex !== -1) {
        const updatedBasket = [...prevBasket]
        updatedBasket[existingItemIndex] = {
          code: itemCode,
          quant: updatedBasket[existingItemIndex].quant + quantity
        }
        return updatedBasket
      } else {
        return [...prevBasket, { code: itemCode, quant: quantity }]
      }
    })
    
    setQuantities(prev => ({ ...prev, [itemCode]: 0 }))
  }
  
  const handleQuantityChange = (itemCode: string, value: string) => {
    setQuantities(prev => ({ ...prev, [itemCode]: parseInt(value) || 0 }))
  }

  const handleBasketSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    if (basket.length === 0) return
    
    const total = await postBasket(basket)
    setSubtotal(total["total"])
    setBasket([])
  }
  
  useEffect(() => {
    getPrices().then(setItems)
  }, [])
  
  return (
    <div className='App'>
      <h1>Items</h1>
      <ul>
        {
          items.map(item => (
            <li key={item.code}>
              <form onSubmit={(e) => handleItemSubmit(e, item.code)}>
                <span> {item.code}: {item.price} </span>
                <input
                  min="0"
                  type='number'
                  placeholder="0"
                  value={quantities[item.code] || ''}
                  onChange={(e) => handleQuantityChange(item.code, e.target.value)}
                />
                <button type="submit">Add</button>
              </form>
            </li>
          ))
        }
      </ul>
      
      <h2>Basket</h2>
      <form onSubmit={handleBasketSubmit}>
        <pre>{JSON.stringify(basket, null, 2)}</pre>
        <button type="submit" disabled={basket.length === 0}>Submit Basket</button>
      </form>

      {subtotal !== null && (
        <>
          <h2>Subtotal</h2>
          <p>Your Subtotal is {subtotal}</p>
        </>
      )}
      

    </div>
  )
}

export default App