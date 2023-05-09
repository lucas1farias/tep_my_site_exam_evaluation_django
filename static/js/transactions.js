

const stocks_found = document.getElementById('stocks-found')
let logged_user_transactions = document.getElementById('logged-user-transactions')
let search_stock_form = document.getElementById('search-stock-form')


const loop = setInterval(() => {
  console.log('--->', stocks_found.textContent)
  if (stocks_found.textContent != '[]') {
    logged_user_transactions.style.display = 'none'
    search_stock_form.style.display = 'none'
  }
  
}, 1)

function append(nodeList) {
  let data = []
  nodeList.forEach(i => {
    data.push(i.textContent)
  })
  return data
}
