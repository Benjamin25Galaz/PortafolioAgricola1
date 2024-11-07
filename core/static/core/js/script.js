// Variables para el flujo
const plantaArbolOption = document.getElementById('plantaArbolRadio');
const plantarDetails = document.getElementById('plantarDetails');
const continuarButton = document.getElementById('continuarButton');
let selectedComuna = '';
let cantidadArboles = 1;

// Selección de "Planta un Árbol"
plantaArbolOption.addEventListener('click', function() {
    plantarDetails.style.display = 'block';
});

// Botón continuar
continuarButton.addEventListener('click', function(event) {
    event.preventDefault(); // Evita el comportamiento predeterminado del botón
    selectedComuna = document.getElementById('comuna').value;
    cantidadArboles = document.getElementById('cantidadArboles').value;
    const tipoArbol = document.getElementById('tipoArbol').value;

    if (selectedComuna === '' || tipoArbol === '') {
        alert('Por favor, selecciona una comuna y un tipo de árbol.');
    } else {
        const queryString = `comuna=${encodeURIComponent(selectedComuna)}&tipoArbol=${encodeURIComponent(tipoArbol)}&cantidad=${encodeURIComponent(cantidadArboles)}&total=${encodeURIComponent(cantidadArboles * 5000)}`;
        window.location.href = `resumen.html?${queryString}`;
    }
});





