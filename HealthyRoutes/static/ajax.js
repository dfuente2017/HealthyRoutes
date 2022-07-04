$(document).ready(function(){
    $("#country").change(function(){
        deleteProvinces();
        deleteTowns();

        /*Peticion ajax*/
        $.ajax({
            url:'get/provinces',
            type: 'get',
            data: {
                country_id: $(this).val()
            },
            success: function(response) {
                for(let key in response){
                    $("#province").append('<option value=' + key +'>' + response[key] + '</option>')
                }
                enableSubmit();
            },
            error: function(jqXHR, textStatus, errorThrown){
                alert(textStatus + ':' + errorThrown)
            }
        });
    });

    $("#province").change(function(){
        deleteTowns();

        /*Peticion ajax*/
        $.ajax({
            url: 'get/towns',
            type: 'get',
            data: {
                province_id: $(this).val()
            },
            success: function(response){
                for(let key in response){
                    $("#town").append('<option value=' + key +'>' + response[key] + '</option>')
                }
                enableSubmit();
            },
            error: function(jqXHR, textStatus, errorThrown){
                alert(textStatus + ':' + errorThrown)
            }
        });
    });

    $("#town").change(function(){
        enableSubmit();
    });

    $("#town-stations-excel").change(function(){
        enableSubmit();
    });

    function deleteProvinces(){
        $('#province').find('option').remove().end()
        $("#province").append('<option value=-1>Seleccione una provincia</option>')
    }
    
    function deleteTowns(){
        $('#town').find('option').remove().end()
        $("#town").append('<option value=-1>Seleccione una ciudad</option>')
    }

    function enableSubmit(){
        let country = $('#country').val();
        let province = $('#province').val();
        let town = $('#town').val();
        let file = $('#town-stations-excel').val();

        if(country != -1 && province != -1 && town != -1 && file != ""){
            $('#submit-selected-town').removeAttr('disabled');
            console.log(country + " " + province + " " + town + " " + file);
            console.log("Enabled");
        }else{
            $('#submit-selected-town').attr('disabled', 'disabled');
            console.log(country + " " + province + " " + town + " " + file);
            console.log("Disabled");
        }
    }
});


