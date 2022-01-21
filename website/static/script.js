const txt = document.querySelector('#note');
function setNewSize() {
   this.style.height = "1px";
   this.style.height = this.scrollHeight + "px";
}
txt.addEventListener('keyup', setNewSize);

function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/home";
    });
  }