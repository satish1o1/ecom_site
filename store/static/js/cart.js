cartBtn = document.getElementsByClassName('update-cart')
for (var i = 0; i < cartBtn.length; i++){
      cartBtn[i].addEventListener('click', function () {
            productId = this.dataset.product
            action = this.dataset.action
            if (user == 'Anonymous') {
                  console.log("unauthorized user")
            }
            else {
                  add_item(productId, action)
            }    
               
      })
}

function add_item(productId, action) {
      var url = '/update_item/'
      fetch(url, {
            method: 'POST',
            headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'productId':productId,'action':action}),

      })
            .then((response) => {
            return response.json()
            })
            .then((data) => {
                  console.log("data:", data)
                  location.reload()
      })
}