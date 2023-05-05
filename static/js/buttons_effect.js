

const buttons_group = document.querySelectorAll('.btn')
const bootstrap_classes = ['btn btn-success', 'btn btn-secondary', 'btn btn-dark', 'btn btn-info', 'btn btn-danger']
const indexes = [...Array(5).keys()]
console.log(indexes)
let button
let index

const range = ({min, max}) => {
  return Array.from({length: max - min + 1}, (value, key) => key + min)
}

setInterval(() => {
    button = buttons_group[Math.floor(Math.random() * buttons_group.length)]
    index = indexes[Math.floor(Math.random() * indexes.length)]
    new_style = bootstrap_classes[index]
    button.className = new_style
    button.style.transition = 'linear 1s'
    console.log(new_style)
    
}, 500)
