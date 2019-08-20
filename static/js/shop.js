$(document).ready(function(){

  // Contact Form Handler
  var contactForm = $('.contact-form')
  var contactFormMethod = contactForm.attr('method')
  var contactFormEndpoint = contactForm.attr('action')

  function displaySubmitting(submitBtn, defaultText, doSubmit){
    if (doSubmit){
      submitBtn.addClass('disabled')
      submitBtn.html('<i class="fa fa-spin fa-spinner"></i> Отправка...')
    } else {
      submitBtn.removeClass('disabled')
      submitBtn.html(defaultText)
    }
  }

  contactForm.submit(function(event){
    event.preventDefault()
    var contactFormSubmitBtn = contactForm.find('[type="submit"]')
    var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
    var contactFormData = contactForm.serialize()
    var thisForm = $(this)
    displaySubmitting(contactFormSubmitBtn, '', true)

    $.ajax({
      method: contactFormMethod,
      url: contactFormEndpoint,
      data: contactFormData,
      success: function(data){
        contactForm[0].reset()
        $.alert({
          title: 'Отправлено!',
          content: data.message,
          theme: 'modern'
        })
        setTimeout(function(){
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 2000)
      },
      error: function(error){
        console.log(error.responseJSON)
        var jsonData = error.responseJSON
        var msg = ''

        $.each(jsonData, function(key, value){
          msg += key + ': ' + value[0].message + '<br/>'
        })

        $.alert({
          title: 'Упс!',
          content: msg,
          theme: 'modern',
        })

        setTimeout(function(){
          displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
        }, 2000)
      }
    })
  })

  // Auto Search
  var searchForm = $('.search-form')
  var searchInput = searchForm.find('[name="q"]')
  var typingTimer
  var typingInterval = 5000
  var searchBtn = searchForm.find('[type="submit"]')

  searchInput.keyup(function(event){
    clearTimeout(typingTimer)
    typingTimer = setTimeout(performSearch, typingInterval)
  })

  searchInput.keydown(function(event){
    clearTimeout(typingTimer)
  })

  function displaySearching(){
    searchBtn.addClass('disabled')
    searchBtn.html('<i class="fa fa-spin fa-spinner"></i> Поиск...')
  }

  function performSearch(){
    displaySearching()
    var query = searchInput.val()
    setTimeout(function(){
      window.location.href = '/search/?q=' + query
    }, 1000)
  }

  // Cart + Add Product Form
  var productForm = $('.form-product-ajax')

  productForm.submit(function(event){
    event.preventDefault();
    // console.log('Form is not sending')
    var thisForm = $(this)
    // var actionEndPoint = thisForm.attr('action')
    var actionEndPoint = thisForm.attr('data-endpoint')
    var httpMethod = thisForm.attr('method')
    var formData = thisForm.serialize()

    $.ajax({
      url: actionEndPoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        var submitSpan = thisForm.find('.submit-span')
        if (data.added){
          submitSpan.html('В корзине <button type="submit" class="btn btn-link">Удалить</button>')
        } else {
          submitSpan.html('<button type="submit" class="btn btn-success">Добавить в корзину</button>')
        }
        var navbarCount = $('.navbar-cart-count')
        navbarCount.text(data.cartItems)
        var currentPath = window.location.href

        if (currentPath.indexOf('cart') != -1) {
          refreshCart()
        }
      },
      error: function(errorData){
        $.alert({
          title: 'Упс!',
          content: 'Произошла ошибка',
          theme: 'modern'
        })
      }
    })
  })

  function refreshCart(){
    console.log('in current cart')
    var cartTable = $('.cart-table')
    var cartBody = cartTable.find('.cart-body')
    var productRows = cartBody.find('.cart-products')
    var currentUrl = window.location.href

    var refreshCartUrl = '/api/cart/'
    var refreshCartMethod = 'GET'
    var data = {}
    $.ajax({
      url: refreshCartUrl,
      method: refreshCartMethod,
      data: data,
      success: function(data){

        var hiddenCartProductRemoveForm = $('.cart-product-remove-form')
        if (data.products.length > 0){
          productRows.html(' ')
          i = data.products.length
          $.each(data.products, function(index, value){
            var newCartProductRemove = hiddenCartProductRemoveForm.clone()
            newCartProductRemove.css('display', 'block')
            newCartProductRemove.find('.cart-product-id').val(value.id)
            cartBody.prepend('<tr><th scope="row">' + i + '</th><td><a href="' + value.url + '">' + value.title + '</a>' + newCartProductRemove.html() + '</td><td>' + value.price + ' BYN' + '</td></tr>')
            i --
          })
          cartBody.find('.cart-subtotal').text(data.subtotal + ' BYN')
          cartBody.find('.cart-total').text(data.total + ' BYN')
        } else {
          window.location.href = currentUrl
        }
      },
      error: function(errorData){
        $.alert({
          title: 'Упс!',
          content: 'Произошла ошибка',
          theme: 'modern'
        })
      }
    })
  }
})
