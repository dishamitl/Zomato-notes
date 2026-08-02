// =============================
// Backend Configuration
// =============================

const BASE_URL = "http://127.0.0.1:8000";

const TOKEN = "zomato123";

// =============================
// DOM Elements
// =============================
const algoSelect = document.getElementById("algoSelect");
const lookupTitle = document.getElementById("lookupTitle");
const lookupButton = document.getElementById("lookupButton");
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
const sortSelect = document.getElementById("sortSelect");
const smartSearchInput = document.getElementById("smartSearchInput");
const smartSearchButton = document.getElementById("smartSearchButton");
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
async function fetchNotes(keyword = "", sortBy = "relevance") {

    loadingMessage.style.display = "block";
    apiError.textContent = "";

    try {

let url = `${BASE_URL}/notes`;

if (keyword && sortBy === "relevance") {

    url = `${BASE_URL}/notes/search?keyword=${encodeURIComponent(keyword)}`;

}
else if (sortBy === "date") {

    url = `${BASE_URL}/notes/search?sort_by=date`;

}
else if (keyword) {

    url += `?tag=${encodeURIComponent(keyword)}`;

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
async function updateNoteTag(id, newTag) {

    const response = await fetch(`${BASE_URL}/notes/${id}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            tag: newTag
        })

    });

    if (!response.ok) {

        throw new Error("Failed to update tag.");

    }

    return await response.json();

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
    // ================= AI Suggestion =================

if (note.ai_suggestion) {

    const aiBox = document.createElement("div");

    aiBox.className = "ai-box";

    const heading = document.createElement("h4");

    heading.textContent = "AI Suggests";

    const tags = document.createElement("p");

    tags.textContent =
        "Tags: " + note.ai_suggestion.tags.join(", ");

    const summary = document.createElement("p");

    summary.textContent =
        "Summary: " + note.ai_suggestion.summary;

    const applyBtn = document.createElement("button");

    applyBtn.textContent = "Apply as Tag";

    applyBtn.addEventListener("click", async () => {

        try {

            const updated = await updateNoteTag(

                note.id,

                note.ai_suggestion.tags[0]

            );

            tag.textContent = `Tag: ${updated.tag}`;

        }

        catch (error) {

            apiError.textContent = error.message;

        }

    });

    aiBox.appendChild(heading);

    aiBox.appendChild(tags);
    if (note.similarity !== undefined) {

    const similarity = document.createElement("p");

    similarity.innerHTML =
        `<strong>Similarity:</strong> ${note.similarity.toFixed(3)}`;

    aiBox.appendChild(similarity);

}

    aiBox.appendChild(summary);

    aiBox.appendChild(applyBtn);

    card.appendChild(aiBox);

}

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
let timer;

searchInput.addEventListener("input", () => {

    clearTimeout(timer);

    timer = setTimeout(() => {

        fetchNotes(
            searchInput.value.trim(),
            sortSelect.value
        );

    }, 400);

});
sortSelect.addEventListener("change", () => {

    fetchNotes(
        searchInput.value.trim(),
        sortSelect.value
    );

});
document.addEventListener("DOMContentLoaded", () => {

    await fetchNotes();

    categoryTree.appendChild(
        renderCategoryTree(CATEGORY_TREE)
    );

});
async function lookupNote(title) {

    const response = await fetch(
        `${BASE_URL}/notes/lookup?title=${encodeURIComponent(title)}&algo=${algoSelect.value}`
    );

    if (!response.ok) {

        throw new Error("Note not found.");

    }

    return await response.json();

}
lookupButton.addEventListener("click", async () => {

    apiError.textContent = "";

    const title = lookupTitle.value.trim();

    if (!title) {

        return;

    }

    try {

        const note = await lookupNote(title);

        renderNotes([note]);

    }
    catch (error) {

        apiError.textContent = error.message;

    }

});
async function quickFind(tag){

    const response = await fetch(
        `${BASE_URL}/notes/quick-find?tag=${encodeURIComponent(tag)}`
    );

    if(!response.ok){

        throw new Error("No note found.");

    }

    return await response.json();

}
document.querySelectorAll(".tagButton").forEach(button=>{

    button.addEventListener("click",async()=>{

        try{

            const note=await quickFind(button.dataset.tag);

            renderNotes([note]);

            const card=document.querySelector(".note-card");

            if(card){

                card.classList.add("highlight");

                card.scrollIntoView({

                    behavior:"smooth",

                    block:"center"

                });

            }

        }

        catch(error){

            apiError.textContent=error.message;

        }

    });

});
async function smartSearch(query) {

    const response = await fetch(

        `${BASE_URL}/notes/smart-search?q=${encodeURIComponent(query)}`

    );

    if (!response.ok) {

        throw new Error("Smart search failed.");

    }

    return await response.json();

}
smartSearchButton.addEventListener("click", async () => {

    apiError.textContent = "";

    const query = smartSearchInput.value.trim();

    if (!query) {

        return;

    }

    try {

        const results = await smartSearch(query);

        renderNotes(results);

    }

    catch (error) {

        apiError.textContent = error.message;

    }

});