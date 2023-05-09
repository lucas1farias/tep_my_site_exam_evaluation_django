

const all_list_items = document.querySelectorAll('li')
console.log(all_list_items)

all_list_items.forEach(tag => {
  tag.className = 'thread'
})