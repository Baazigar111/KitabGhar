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
            // Save role to identify admin later if needed
            localStorage.setItem("userRole", data.role);
            window.location.href = (data.role === "admin") ? "admin.html" : "index.html";
        } else {
            alert(data.message);
        }
    })
    .catch(err => console.error("Login Error:", err));
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
    })
    .catch(err => console.error("Registration Error:", err));
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
    })
    .catch(err => console.error("Upload Error:", err));
}

function loadEbooks() {
    fetch("/ebooks")
    .then(res => res.json())
    .then(data => {
        let list = document.getElementById("bookList");
        if (!list) return;
        list.innerHTML = "";

        // Check if the current page is admin.html
        const isAdminPage = window.location.pathname.includes("admin.html");

        data.forEach(book => {
            // Only create delete button string if we are on the admin page
            const deleteBtn = isAdminPage ? 
                `<button class="logout-btn" style="margin-top:10px; width:100%; background-color: #ef4444;" onclick="deleteBook(${book.id})">🗑️ Delete Book</button>` 
                : "";

            list.innerHTML += `
                <div class="book">
                    <h3>${book.title}</h3>
                    <p><b>Author:</b> ${book.author}</p>
                    <p><b>Category:</b> ${book.category}</p>
                    <a class="download-link" href="/uploads/${book.file}" target="_blank">📥 Download PDF</a>
                    ${deleteBtn}
                </div>`;
        });
    })
    .catch(err => console.error("Error loading books:", err));
}

// --- NEW DELETE FUNCTION ---
function deleteBook(bookId) {
    if (confirm("Are you sure you want to delete this book permanently?")) {
        fetch(`/delete/${bookId}`, {
            method: "DELETE"
        })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
            loadEbooks(); // Refresh the list after deletion
        })
        .catch(err => console.error("Delete Error:", err));
    }
}

// --- LOGOUT FUNCTION ---
function logout() {
    // Clear both server-side and client-side sessions
    fetch("/logout").then(() => {
        localStorage.clear();
        sessionStorage.clear();
        window.location.href = "login.html";
    });
}

// Automatically load books if the bookList div exists on the page
if (document.getElementById("bookList")) loadEbooks();