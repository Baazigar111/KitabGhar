function login() {
    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message === "Login Successful") {
            // Store role in case we need it for UI checks
            localStorage.setItem("userRole", data.role);
            window.location.href = (data.role === "admin") ? "admin.html" : "index.html";
        } else {
            alert(data.message);
        }
    });
}

function register() {
    fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: document.getElementById("rusername").value,
            password: document.getElementById("rpassword").value,
            role: document.getElementById("role").value
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if(data.message === "User Registered Successfully") window.location.href = "login.html";
    });
}

function uploadEbook() {
    let formData = new FormData();
    formData.append("title", document.getElementById("title").value);
    formData.append("author", document.getElementById("author").value);
    formData.append("category", document.getElementById("category").value);
    formData.append("file", document.getElementById("ebook").files[0]);

    fetch("/upload", { method: "POST", body: formData })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        loadEbooks();
    });
}

function loadEbooks() {
    fetch("/ebooks")
    .then(res => res.json())
    .then(data => {
        let list = document.getElementById("bookList");
        if (!list) return;
        list.innerHTML = "";
        data.forEach(book => {
            list.innerHTML += `
                <div class="book">
                    <h3>${book.title}</h3>
                    <p><b>Author:</b> ${book.author}</p>
                    <p><b>Category:</b> ${book.category}</p>
                    <a href="/uploads/${book.file}" target="_blank">📥 Download</a>
                </div>`;
        });
    });
}

// --- NEW LOGOUT FUNCTION ---
function logout() {
    localStorage.clear();
    sessionStorage.clear();
    window.location.href = "login.html";
}

if (document.getElementById("bookList")) loadEbooks();