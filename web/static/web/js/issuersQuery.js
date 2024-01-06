(() => {

    var issuerSelect = $('#issuerSelect');
    var patientSelect = $('#patientSelect');
    var issuerUrl = issuerSelect.data('url');
    // the slice method removes the last two characters from the URL, because we don't need the issuer ID
    // and that is a workaround to avoid hardcoding the URL in the JS file, but retrieving from the Django
    // templating system
    var patientUrl = $('#patientSelect').data('url').slice(0, -2);  

    $.ajax({
        url: issuerUrl, 
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            issuerSelect.empty();
            issuerSelect.append($('<option></option>').attr('value', '').text('Selecione o emissor').prop('disabled', true).prop('selected', true));
            $.each(data.issuers, function(index, issuer) {
                issuerSelect.append($('<option></option>').attr('value', issuer.id).text(issuer.name));
            });
        }
    });

    issuerSelect.change(function() {
        var selectedIssuerId = $(this).val();
        $.ajax({
            url: patientUrl + selectedIssuerId,  // replace with the actual URL
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                patientSelect.removeClass('d-none');  // remove the d-none class
                patientSelect.empty();
                $.each(data.patients, function(index, patient) {
                    patientSelect.append($('<option></option>').attr('value', patient.id).text(patient.name));
                });
            }
        });
    });

})();
