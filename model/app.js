let page = 1;
const modelList = document.querySelector(".model-list");
const searchButton = document.querySelector("#search-button");
const searchInput = document.querySelector("#search-id");
const prevButton = document.querySelector("#prev-button");
const nextButton = document.querySelector("#next-button");


function displayModels() {
    const limit = 100;
    window.apiURL = "https://civitai.com/api/v1/models?page=" + page + "&limit=100";
    fetch(apiURL)
        .then((response) => response.json())
        .then((data) => {
            modelList.innerHTML = "";
            data.items.forEach((item) => {
                if (!item.nsfw) {
                    const modelItem = document.createElement("div");
                    modelItem.classList.add("model-item");

                    const modelImage = document.createElement("img");
                    modelImage.src = item.modelVersions[0].images[0].url;
                    modelItem.appendChild(modelImage);


                    const modelName = document.createElement("h2");
                    modelName.innerText = item.name;
                    modelItem.appendChild(modelName);

                    const modelID = document.createElement("p");
                    modelID.innerText = "ID: " + item.id;
                    modelItem.appendChild(modelID);

                    const downloadLink = document.createElement("a");
                    downloadLink.classList.add("download-button");
                    downloadLink.setAttribute("href", item.modelVersions[0].downloadUrl);
                    downloadLink.setAttribute("download", item.modelVersions[0].filename);
                    downloadLink.innerText = "Download";
                    modelItem.appendChild(downloadLink);

                    modelList.appendChild(modelItem);
                }
            });
        });

}

// Function to filter models by ID
function searchModels() {
    const searchID = searchInput.value;
    fetch(apiURL)
        .then((response) => response.json())
        .then((data) => {
            modelList.innerHTML = "";
            data.items.forEach((item) => {
                if (item.id == searchID && !item.nsfw) {
                    const modelItem = document.createElement("div");
                    modelItem.classList.add("model-item");

                    const modelImage = document.createElement("img");
                    modelImage.src = item.modelVersions[0].images[0].url;
                    modelItem.appendChild(modelImage);

                    const modelName = document.createElement("h2");
                    modelName.innerText = item.name;
                    modelItem.appendChild(modelName);

                    const modelID = document.createElement("p");
                    modelID.innerText = "ID: " + item.id;
                    modelItem.appendChild(modelID);

                    const downloadLink = document.createElement("a");
                    downloadLink.classList.add("download-button");
                    downloadLink.setAttribute("href", item.modelVersions[0].downloadUrl);
                    downloadLink.setAttribute("download", item.modelVersions[0].filename);
                    downloadLink.innerText = "Download";
                    modelItem.appendChild(downloadLink);

                    modelList.appendChild(modelItem);
                }
            });
        });
}


function prevPage() {
    if (page > 1) {
        page--;
        displayModels();
    }
}

function nextPage() {
    page++;
    displayModels();
}

// 初始显示模型数据
displayModels();

searchButton.addEventListener("click", searchModels);
prevButton.addEventListener("click", prevPage);
nextButton.addEventListener("click", nextPage);


searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        searchModels();
    }
});