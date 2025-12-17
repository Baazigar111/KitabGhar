function login() {
    fetch("https://tp-6s3i.onrender.com/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message === "Login Successful") {
            if (data.role === "admin") {
                window.location.href = "admin.html";
            } else {
                window.location.href = "index.html";
            }
        } else {
            alert(data.message);
        }
    });
}

function register() {
    fetch("https://tp-6s3i.onrender.com/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: document.getElementById("rusername").value,
            password: document.getElementById("rpassword").value,
            role: document.getElementById("role").value
        })
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}


function searchBooks() {
    const bookList = document.getElementById("bookList");
    bookList.innerHTML = "";

    const books = [
        { title: "Python Basics", author: "Guido" },
        { title: "Machine Learning", author: "Andrew Ng" },
        { title: "Data Science", author: "Jake" }
    ];

    books.forEach(book => {
        const div = document.createElement("div");
        div.className = "book";
        div.innerHTML = `
            <h3>${book.title}</h3>
            <p>Author: ${book.author}</p>
            <button>Read</button>
            <button>Download</button>
        `;
        bookList.appendChild(div);
    });
}

function uploadBook() {
    alert("Upload functionality will be connected to backend later");
}

function uploadEbook() {
    let formData = new FormData();
    formData.append("title", document.getElementById("title").value);
    formData.append("author", document.getElementById("author").value);
    formData.append("category", document.getElementById("category").value);
    formData.append("file", document.getElementById("ebook").files[0]);

    fetch("https://tp-6s3i.onrender.com/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}

function loadEbooks() {
    fetch("https://tp-6s3i.onrender.com/ebooks")
        .then(res => res.json())
        .then(data => {
            let list = document.getElementById("bookList");
            list.innerHTML = "";

            data.forEach(book => {
                list.innerHTML += `
                    <div class="book">
                        <h3>${book.title}</h3>
                        <p><b>Author:</b> ${book.author}</p>
                        <p><b>Category:</b> ${book.category}</p>
                        <a href="https://tp-6s3i.onrender.com/uploads/${book.file}" target="_blank">📥 Download</a>
                    </div>
                `;
            });
        });
}

loadEbooks();
