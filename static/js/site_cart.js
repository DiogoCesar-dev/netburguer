// site_cart.js
// Intercepta formulários de adicionar ao carrinho e faz POST via fetch

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function(){
    // tornar botões de adicionar (forms) em AJAX
    const addForms = document.querySelectorAll('form[action*="adicionar"]');
    addForms.forEach(form => {
        form.addEventListener('submit', function(e){
            e.preventDefault();
            const action = form.getAttribute('action');
            const formData = new FormData(form);
            const csrftoken = getCookie('csrftoken');

            fetch(action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData,
            })
            .then(resp => resp.json())
            .then(data => {
                if(data && data.success){
                    // mostrar toast
                    Toastify({
                        text: "Adicionado ao carrinho!",
                        duration: 3000,
                        gravity: "top",
                        position: "right",
                        style: { background: "#16a34a" }
                    }).showToast();

                    // atualizar contador
                    const counter = document.getElementById('cart-count');
                    if(counter){
                        counter.textContent = data.count || 0;
                    }
                }
            })
            .catch(err => {
                console.error('Erro ao adicionar ao carrinho', err);
            })
        })
    })

    // buscar contador inicial
    fetch('/cart/count/')
    .then(r => r.json())
    .then(d => {
        const counter = document.getElementById('cart-count');
        if(counter) counter.textContent = d.count || 0;
    })
    .catch(()=>{})
});
