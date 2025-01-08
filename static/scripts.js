document.getElementById('cadastroForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const nome = document.getElementById('nome').value;
    const cpf = document.getElementById('cpf').value;
    const rg = document.getElementById('rg').value;
    const telefone = document.getElementById('telefone').value;
    const cep = document.getElementById('cep').value;
    const endereco = document.getElementById('endereco').value;
    const anotacoes = document.getElementById('anotacoes').value;

    fetch('/api/cadastrar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nome, cpf, rg, telefone, cep, endereco, anotacoes })
    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(obj => {
        if (obj.status === 200) {
            alert(obj.body.message);
            window.location.href = '/';
        } else {
            alert('Erro: ' + obj.body.message);
        }
    })
    .catch(error => {
        console.error('Erro ao cadastrar paciente:', error);
    });
});
