// console.log("javaScript active");

let show_pass = document.getElementById("show-pass");

if (show_pass && logBtn) {
  show_pass.addEventListener("click", () => {
    let x = document.getElementById("password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  });
}

const Searchid = () => {
  let filter = document.getElementById("IdInput").value.toUpperCase();
  let table = document.getElementById("table");

  let tr = table.getElementsByTagName("tr");

  for (var i = 0; i < tr.length; i++) {
    let td = tr[i].getElementsByTagName("td")[0];

    if (td) {
      let textvalue = td.textContent || td.innerHTML;

      if (textvalue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
};

const Searchname = () => {
  let filter = document.getElementById("NameInput").value.toUpperCase();
  let table = document.getElementById("table");

  let tr = table.getElementsByTagName("tr");

  for (var i = 0; i < tr.length; i++) {
    let td = tr[i].getElementsByTagName("td")[1];

    if (td) {
      let textvalue = td.textContent || td.innerHTML;

      if (textvalue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
};

let IdInput = document.getElementById("IdInput");
let NameInput = document.getElementById("NameInput");

if (IdInput && NameInput) {
  IdInput.addEventListener("keyup", () => {
    Searchid();
  });

  NameInput.addEventListener("keyup", () => {
    Searchname();
  });
}

const dateInput = document.getElementById("date");
const prevBtn = document.getElementById("prevDate");
const nextBtn = document.getElementById("nextDate");
const ClareBtn = document.getElementById("ClareBtn");

if (dateInput && ClareBtn) {
  // Today's date by default
  dateInput.value = new Date().toISOString().split("T")[0];

  prevBtn.addEventListener("click", () => {
    event.preventDefault();
    let date = new Date(dateInput.value);
    date.setDate(date.getDate() - 1);

    dateInput.value = date.toISOString().split("T")[0];
  });

  nextBtn.addEventListener("click", () => {
    event.preventDefault();
    let date = new Date(dateInput.value);
    date.setDate(date.getDate() + 1);

    dateInput.value = date.toISOString().split("T")[0];
  });

  ClareBtn.addEventListener("click", () => {
    event.preventDefault();
    let accounts = (document.getElementById("accounts").value = "");
    let description = (document.getElementById("description").value = "");
    let jama = (document.getElementById("jama").value = 0);
    let kharch = (document.getElementById("kharch").value = 0);
  });
}

setTimeout(() => {
  const alerts = document.querySelectorAll(".alert");

  alerts.forEach((alert) => {
    alert.classList.remove("show");
    alert.classList.add("fade");

    setTimeout(() => {
      alert.remove();
    }, 300);
  });
}, 5000);
