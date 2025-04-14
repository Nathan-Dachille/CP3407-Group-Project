function hide_after_delay() {
  const confirmation = document.querySelector(".confirmation-div");
  window.onload = function() {
    setTimeout(function() {
      confirmation.dataset.hidden = "True";
          }, 5000);
  }
}

hide_after_delay();
