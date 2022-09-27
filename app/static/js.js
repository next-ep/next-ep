var btn_add = document.getElementById('add-seasons')
var input = document.getElementById('season-number')
var season_number = input.ariaValueText;
var box = document.getElementById('box')

var i = 0;

btn_add.addEventListener('click', function(){
    for (i; i < season_number; i++)
    createLabel();
    createInput();
});

function createLabel()
{
    var elemento = document.createElement('label');
    elemento.setAttribute('for', 'episode_' + i);
    elemento.textContent = 'Episodios Temporada ' + i + ':';

    box.appendChild(elemento);
}

function createInput()
{
    var elemento = document.createElement('input');
    elemento.setAttribute('type', 'text');
    elemento.setAttribute('name', 'episode_' + i);
    elemento.setAttribute('id', 'episode_' + i);
    elemento.setAttribute('autocomplete', 'off');

    box.appendChild(elemento);
}