// Pase de lista: habilitar el motivo solo cuando se marca "justificada"
document.querySelectorAll("table tbody tr").forEach(function (fila) {
  var motivo = fila.querySelector(".motivo");
  if (!motivo) return;
  fila.querySelectorAll("input[type=radio]").forEach(function (r) {
    r.addEventListener("change", function () {
      var just = r.classList.contains("just") && r.checked;
      motivo.disabled = !just;
      motivo.required = just;
      motivo.minLength = just ? 10 : 0;
      if (!just) motivo.value = "";
    });
  });
});

// Convocatoria: máximo 12 seleccionados
var checks = document.querySelectorAll(".conv");
var contador = document.getElementById("contador");
function actualizar() {
  var n = document.querySelectorAll(".conv:checked").length;
  if (contador) contador.textContent = n;
  checks.forEach(function (c) { if (!c.checked) c.disabled = n >= 12; });
}
checks.forEach(function (c) { c.addEventListener("change", actualizar); });
if (checks.length) actualizar();
