document.addEventListener('DOMContentLoaded', function() {
  const usuarioLink = document.querySelector('.usuario');
  usuarioLink.addEventListener('click', function(event) {
    event.preventDefault(); // Prevenir el comportamiento predeterminado del enlace
    const cerrarSesionAlert = confirm('¿Deseas cerrar sesión?'); // Alerta para preguntar si se desea cerrar sesión
    if (cerrarSesionAlert) {
      const confirmacion = confirm('¿Estás seguro que deseas cerrar sesión?');
      if (confirmacion) {
        window.location.href = usuarioLink.href; // Redirigir a la página de cierre de sesión si se confirma
      }
    }
  });
});
