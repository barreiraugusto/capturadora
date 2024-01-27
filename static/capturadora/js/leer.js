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
          var csrftoken = getCookie('csrftoken');
          $.ajax({
                    url: 'capturaweb',
                    type: 'GET',
                    dataType: 'json',
                    success: function(data) {
                        for (var i = 0; i < data.tiempos.length; i++) {
                            $('#tiempos-container').append('<p>' + data.tiempos[i] + '</p>');
                        }
                    }
                });
        },1000)