/**
     * Permite obtener el token de django
     *
     */
    function getCookie(name) {

        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        //RETORNANDO EL TOKEN
        return cookieValue;

      }//end function getCookie

  /*EJEMPLO AJAX HACIA DJANGO*/
          //token
        setInterval(function chequeo_carton(){
          var contenidoHTML = '';
//          var csrftoken = getCookie('csrftoken');
          $.ajax({
                    url: 'get_tiempo',
                    type: 'GET',
                    dataType: 'json',
                    for (var i = 0; i < data.tiempos.length; i++) {
                        contenidoHTML += data.tiempos[i];
                    }
                    $('#tiempos-container').html('<p>' + contenidoHTML + '</p>');
                });
        },1000)