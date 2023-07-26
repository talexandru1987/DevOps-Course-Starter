// target the document elements
const taskUpdate = document.querySelectorAll(
  ".taskUpdate"
);

const taskDelete = document.querySelectorAll(
  ".deleteTask"
);

//define the functions
const updateList = (event) => {
  const id = event.target.parentNode.id;
  fetch("/check", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
    }),
  })
    .then((response) => response.json())
    .then((data) => console.log(data))
    .catch((error) => console.log(error));
};

const deleteItem = (event) => {
  const id = event.target.parentNode.id;

  fetch("/delete", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
    }),
  })
    .then((response) => response.json())
    .then((data) => console.log(data))
    .catch((error) => console.log(error));
};

//add the event listners
if (taskUpdate.length > 0) {
  taskUpdate.forEach((input) =>
    input.addEventListener("change", updateList)
  );
}

if (taskDelete.length > 0) {
  taskDelete.forEach((input) =>
    input.addEventListener("click", deleteItem)
  );
}

$(document).ready(function () {
  $(".checkbox-group").click(function () {
    $(".checkbox-group")
      .not(this)
      .prop("checked", false);
  });
});
