// =============================
// Backend Configuration
// =============================

const BASE_URL = "http://127.0.0.1:8000";

const TOKEN = "zomato123";

// =============================
// DOM Elements
// =============================

const notesContainer = document.getElementById("notesContainer");
const loadingMessage = document.getElementById("loadingMessage");
const apiError = document.getElementById("apiError");

const noteForm = document.getElementById("noteForm");

const titleInput = document.getElementById("title");
const contentInput = document.getElementById("contentInput");
const tagInput = document.getElementById("tag");
const ownerIdInput = document.getElementById("ownerId");

const errorMessage = document.getElementById("errorMessage");

const searchInput = document.getElementById("searchInput");
const categoryTree = document.getElementById("categoryTree");
let debounceTimer;
const CATEGORY_TREE = {
    name: "All Tags",
    children: [
        {
            name: "Work",
            children: [
                { name: "Standups", children: [] },
                { name: "Retros", children: [] }
            ]
        },
        {
            name: "Personal",
            children: [
                {
                    name: "Health",
                    children: [
                        {
                            name: "Fitness",
                            children: []
                        }
                    ]
                },
                {
                    name: "Recipes",
                    children: []
                }
            ]
        },
        {
            name: "Travel",
            children: []
        }
    ]
};
async function fetchNotes(tag = "") {

    loadingMessage.style.display = "block";
    apiError.textContent = "";

    try {

        let url = `${BASE_URL}/notes`;

        if (tag) {
            url += `?tag=${encodeURIComponent(tag)}`;
        }

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Unable to fetch notes.");
        }

        const notes = await response.json();

        renderNotes(notes);

    }
    catch (error) {

        apiError.textContent = error.message;

    }
    finally {

        loadingMessage.style.display = "none";

    }

}
async function createNote(noteData) {

    const response = await fetch(`${BASE_URL}/notes`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(noteData)

    });

   if (!response.ok) {

    const errorData = await response.json();

    throw new Error(
        errorData.detail || "Failed to create note."
    );

}

    return await response.json();

}
async function deleteNote(id) {

    const response = await fetch(`${BASE_URL}/notes/${id}`, {

        method: "DELETE",

        headers: {
            "x-token": TOKEN
        }

    });
if (!response.ok) {

    const errorData = await response.json();

    throw new Error(
        errorData.detail || "Delete failed."
    );

}

}
function renderSingleNote(note) {

    const card = document.createElement("div");
    card.className = "note-card";

    const title = document.createElement("h3");
    title.textContent = note.title;

    const content = document.createElement("p");
    content.textContent = note.content;

    const tag = document.createElement("p");
    tag.textContent = `Tag: ${note.tag}`;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";

    deleteBtn.addEventListener("click", async () => {

        try {

            await deleteNote(note.id);

            card.remove();

        }
        catch (error) {

            apiError.textContent = error.message;

        }

    });

    card.appendChild(title);
    card.appendChild(content);
    card.appendChild(tag);
    card.appendChild(deleteBtn);

    notesContainer.appendChild(card);

}
function renderNotes(notes) {

    // Clear old notes
    notesContainer.innerHTML = "";

    // No notes found
    if (notes.length === 0) {

        const emptyMessage = document.createElement("p");
        emptyMessage.textContent = "No notes found.";

        notesContainer.appendChild(emptyMessage);

        return;
    }
notes.forEach(note => {
    renderSingleNote(note);
});
}
function renderCategoryTree(node) {

    const ul = document.createElement("ul");

    const li = document.createElement("li");

    li.textContent = node.name;

    ul.appendChild(li);

    if (node.children.length > 0) {

        const childTree = document.createElement("div");

        node.children.forEach(child => {

            childTree.appendChild(
                renderCategoryTree(child)
            );

        });

        li.appendChild(childTree);

        li.addEventListener("click", (event) => {

            event.stopPropagation();

            childTree.classList.toggle("hidden");

        });

    }

    return ul;

}
noteForm.addEventListener("submit", async (event) => {

    event.preventDefault();

    errorMessage.textContent = "";

    const title = titleInput.value.trim();
    const content = contentInput.value.trim();
    const tag = tagInput.value.trim();
    const owner_id = Number(ownerIdInput.value);

    // Validation
    if (title === "") {

        errorMessage.textContent = "Title is required.";
        errorMessage.className = "error";
        return;
    }

    if (content === "") {

        errorMessage.textContent = "Content is required.";
        errorMessage.className = "error";
        return;
    }

    try {

        const newNote = await createNote({

            title,
            content,
            tag,
            owner_id

        });

        // Add new note without refreshing
        renderSingleNote(newNote);

        // Clear form
        noteForm.reset();

    }
    catch (error) {

        apiError.textContent = error.message;

    }

});
searchInput.addEventListener("input", () => {

    clearTimeout(debounceTimer);

    debounceTimer = setTimeout(() => {

        const searchText = searchInput.value.trim();

        fetchNotes(searchText);

    }, 400);

});
document.addEventListener("DOMContentLoaded", () => {

    fetchNotes();

    categoryTree.appendChild(
        renderCategoryTree(CATEGORY_TREE)
    );

});