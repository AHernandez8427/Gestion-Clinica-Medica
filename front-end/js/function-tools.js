// formData is a JSON Object with all values
// from de REST API
function fillForm(formData) {
  $.each(formData, function (key, valor) {
    var elemento = $('[name="' + key + '"]');
    if (elemento.length > 0) {
      if (elemento.is(":checkbox") || elemento.is(":radio")) {
        elemento.prop("checked", elemento.val() === valor);
      } else if (elemento.is("select")) {
        elemento.val(valor);
      } else {
        elemento.val(valor);
      }
    }
  });
}

function setDataElementsReadOnly(formData, isReadOnly) {
  $.each(formData, function (key) {
    var elemento = $('[name="' + key + '"]');
    elemento.prop("readonly", isReadOnly ? "readonly" : "");
  });
}
