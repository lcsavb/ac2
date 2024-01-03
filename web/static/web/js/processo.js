'use strict';
(() => {
const isTratado = $('#previous_treatment_selection');
const divTratPrevio = $('#previous_treatments_description');
const campoTrat = $('.cond-trat');
const isIncapaz = $('#id_incapaz');
const divResponsavel = $('#resp-escondido');
const campoIncapaz = $('.cond-incapaz');
const campoDezoito = $('#id_preenchido_por');
const divCampoDezoito = $('.campo-18');
const inputsCampoDezoito = $('.cond-campo-18');

function mostrarCampo(escolha,divAlvo,campoAlvo) {
    if (escolha.val() == 'True' || escolha.val() == 'medico') {
        divAlvo.removeClass('d-none');
        campoAlvo.attr('required', ' ');
    }
    else {
        divAlvo.addClass('d-none');
        campoAlvo.removeAttr('required');
    }
}

$(document).ready (() => {
    mostrarCampo(isTratado,divTratPrevio,campoTrat);
    mostrarCampo(isIncapaz,divResponsavel,campoIncapaz);
    mostrarCampo(campoDezoito,divCampoDezoito, inputsCampoDezoito);
    isTratado.on('change', () => {
        mostrarCampo(isTratado,divTratPrevio,campoTrat);
    });
    isIncapaz.on('change', () => {
        mostrarCampo(isIncapaz,divResponsavel,campoIncapaz);
    });
    campoDezoito.on('change', () => {
        mostrarCampo(campoDezoito,divCampoDezoito, inputsCampoDezoito);
    });
});


})();