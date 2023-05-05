

let date_input = document.getElementById('creation_date')
let tax_input = document.getElementById('tax')
let submit_input = document.getElementById('new-transaction-post')
let instruction = document.getElementById('hint')

const what_day_is_today = () => {
  const date_today = `${new Date().getDay()}/${new Date().getMonth()}/${new Date().getFullYear()}` 
  
  const date = new Date()
  const day  = date.getDay()
  const month  = date.getMonth() + 1
  const year  = date.getFullYear()
  
  if (day < 10 && month < 10) {
      return `0${day}/0${month}/${year}`
  }
  if (day < 10) {
      return `0${day}/${month}/${year}`
  } 
  if (month < 10) {
      return `${day}/0${month}/${year}`
  }
}

const date_validity = (target_date) => {
  const date = new Date()
  const current_year = date.getFullYear()
  const one_century_later = current_year + 100
  const day_calculus = Number(target_date[0] + target_date[1])
  const month_calculus = Number(target_date[3] + target_date[4])
  const year_calculus = Number(target_date[6] + target_date[7] + target_date[8] + target_date[9])
  const has_proper_size = target_date.length === 10
  const has_proper_day = day_calculus > 0 && day_calculus <= 31
  const has_proper_month = month_calculus > 0 && month_calculus <= 12
  const has_proper_year = year_calculus >= current_year && year_calculus <= one_century_later
  const has_first_dash = target_date[2] === '/'
  const has_second_dash = target_date[5] === '/'
  
  let counter = 0
  const requirements = [
    has_proper_size, has_proper_day, has_proper_month, has_proper_year, has_first_dash, has_second_dash
  ]
  requirements.forEach(requirement => {
    if (!requirement) {
      counter++
    }
  })

  // console.log(current_year, one_century_later, day_calculus, month_calculus, year_calculus)
  return counter == 0 ? true : false
}

const range = (min, max) => {
  return Array.from({length: max - min + 1}, (value, key) => key + min)
}

const tax_validity = (target_input) => {
    // console.log(target_input.length)
    // const has_proper_size = target_input.length >= 0 || target_input.length <= 4
    // const has_proper_comma = target_input[1] === ',' || target_input[2] === ','
    // const has_proper_max_value = Number(tax[0] + tax[1]) <= 99

    // let counter = 0
    // let requirements = [has_proper_size, has_proper_comma, has_proper_max_value]
    
    // requirements.forEach(requirement => {
    //   if (!requirement) {
    //     counter++
    //   }
    // })
    
    // console.log(requirements)
    // return counter == 0 ? true : false
}

const loop = setInterval(() => {
    let date_input_status = date_validity(date_input.value)
    // let tax_input_status = tax_validity(tax_input.value)
    
    if (date_input_status) {
      submit_input.style.display = 'inherit'
      instruction.textContent = ''
    } else {
      submit_input.style.display = 'none'
      instruction.textContent = 'Digite uma data em formato "dd/mm/yyyy" para criar uma transação'
    }
}, 1000)
