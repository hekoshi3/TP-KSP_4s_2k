// scripts.js

// Скрипт для страницы image_generation.html
document.addEventListener('DOMContentLoaded', function() {
    const imageForm = document.getElementById('imageForm');
    if (imageForm) {
        imageForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            const generateButton = document.getElementById('generateButton');
            const errorMessage = document.getElementById('errorMessage');
            generateButton.disabled = true;
            generateButton.textContent = 'Please wait...';

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            }).then(response => response.json())
            .then(data => {
                if (data.generated_image_path) {
                    document.getElementById('resultImage').src = data.generated_image_path;
                    document.getElementById('resultImage').style.display = 'block';
                    errorMessage.style.display = 'none';
                } else if (data.error) {
                    let errorMessages = '';
                    for (let field in data.error) {
                        errorMessages += data.error[field].join('<br>') + '<br>';
                    }
                    errorMessage.innerHTML = errorMessages;
                    errorMessage.style.display = 'block';
                }
                generateButton.disabled = false;
                generateButton.textContent = 'Generate';
            })
            .catch(error => {
                console.error('Error:', error);
                generateButton.disabled = false;
                generateButton.textContent = 'Generate';
            });
        });
    }
});

// Скрипт для страницы gallery.html
document.addEventListener('DOMContentLoaded', function() {
    const sizeSlider = document.getElementById('sizeSlider');
    if (sizeSlider) {
        sizeSlider.addEventListener('input', function() {
            var newSize = this.value + 'px';
            document.documentElement.style.setProperty('--image-width', newSize);
            msnry.layout();
        });
    }

    var elem = document.querySelector('.gallery');
    if (elem) {
        var msnry = new Masonry(elem, {
            itemSelector: '.gallery-item',
            columnWidth: '.gallery-item',
            percentPosition: true
        });
    }
});

function openModalGallery(imageUrl, username, prompt, negativePrompt, width, height, seed, userId, imageId, modelName, samplerName, samplerSteps, hashValue, cfgScale) {
    document.getElementById("modalImage").src = imageUrl;
    document.getElementById("modalUsername").innerText = username;
    document.getElementById("modalUsername").href = `/profile/${userId}/`;
    document.getElementById("modalPrompt").innerText = prompt;
    document.getElementById("modalNegativePrompt").innerText = negativePrompt;
    document.getElementById("modalWidth").innerText = width;
    document.getElementById("modalHeight").innerText = height;
    document.getElementById("modalSeed").innerText = seed;
    document.getElementById("modalImageId").value = imageId;
    document.getElementById("modalModelName").innerText = modelName;
    document.getElementById("modalSamplerName").innerText = samplerName;
    document.getElementById("modalSamplerSteps").innerText = samplerSteps;
    document.getElementById("modalHashValue").innerText = hashValue;
    document.getElementById("modalCFGScale").innerText = cfgScale;
    document.getElementById("modelDetails").style.display = "none";

    var modalButton = document.getElementById("modalButton");
    modalButton.onclick = function() {
        addToFavouritesGallery(imageId);
    };

    document.getElementById("myModal").style.display = "block";
}

function closeModalGallery() {
    document.getElementById("myModal").style.display = "none";
}

function toggleModelDetailsGallery() {
    const details = document.getElementById("modelDetails");
    if (details.style.display === "none") {
        details.style.display = "block";
    } else {
        details.style.display = "none";
    }
}

window.onclick = function(event) {
    if (event.target == document.getElementById("myModal")) {
        closeModalGallery();
    }
};

function addToFavouritesGallery(imageId) {
    fetch(`/profile/toggle_favourite/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({request_id: imageId, is_favourite: false})
    }).then(response => response.json()).then(data => {
        if (data.success) {
            closeModalGallery();
        }
    });
}

// Скрипт для страницы profile.html
document.addEventListener('DOMContentLoaded', function() {
    var galleryElems = document.querySelectorAll('.gallery');
    galleryElems.forEach(function(galleryElem) {
        var msnry = new Masonry(galleryElem, {
            itemSelector: '.gallery-item',
            columnWidth: '.gallery-item',
            percentPosition: true
        });
        galleryElem.msnryInstance = msnry;
    });
});

function openModalProfile(imageUrl, username, prompt, negativePrompt, width, height, seed, userId, imageId, modelName, samplerName, samplerSteps, hashValue, cfgScale, isFavourite) {
    document.getElementById("modalImage").src = imageUrl;
    document.getElementById("modalUsername").innerText = username;
    document.getElementById("modalUsername").href = `/profile/${userId}/`;
    document.getElementById("modalPrompt").innerText = prompt;
    document.getElementById("modalNegativePrompt").innerText = negativePrompt;
    document.getElementById("modalWidth").innerText = width;
    document.getElementById("modalHeight").innerText = height;
    document.getElementById("modalSeed").innerText = seed;
    document.getElementById("modalImageId").value = imageId;
    document.getElementById("modalModelName").innerText = modelName;
    document.getElementById("modalSamplerName").innerText = samplerName;
    document.getElementById("modalSamplerSteps").innerText = samplerSteps;
    document.getElementById("modalHashValue").innerText = hashValue;
    document.getElementById("modalCFGScale").innerText = cfgScale;
    document.getElementById("modelDetails").style.display = "none";

    var modalButton = document.getElementById("modalButton");
    var currentUserId = document.querySelector('meta[name="current-user-id"]').content;
    var profileUserId = document.querySelector('meta[name="profile-user-id"]').content;

    modalButton.style.display = 'inline-block';
    if (isFavourite && currentUserId === profileUserId) {
        modalButton.innerText = "Remove from Favourites";
        modalButton.onclick = function() {
            toggleFavouriteProfile(imageId, true);
        };
    } else {
        modalButton.innerText = "Add to Favourites";
        modalButton.onclick = function() {
            toggleFavouriteProfile(imageId, false);
        };
    }

    document.getElementById("myModal").style.display = "block";
}

function closeModalProfile() {
    document.getElementById("myModal").style.display = "none";
}

function toggleModelDetailsProfile() {
    const details = document.getElementById("modelDetails");
    if (details.style.display === "none") {
        details.style.display = "block";
    } else {
        details.style.display = "none";
    }
}

window.onclick = function(event) {
    if (event.target == document.getElementById("myModal")) {
        closeModalProfile();
    }
};

function showHistory() {
    document.getElementById('history').style.display = 'flex';
    document.getElementById('favourites').style.display = 'none';
    var msnry = new Masonry(document.querySelector('#history'), {
        itemSelector: '.gallery-item',
        columnWidth: '.gallery-item',
        percentPosition: true
    });
    msnry.layout();
}

function showFavourites() {
    document.getElementById('history').style.display = 'none';
    document.getElementById('favourites').style.display = 'flex';
    var msnry = new Masonry(document.querySelector('#favourites'), {
        itemSelector: '.gallery-item',
        columnWidth: '.gallery-item',
        percentPosition: true
    });
    msnry.layout();
}

function toggleFavouriteProfile(imageId, isFavourite) {
    fetch(`/profile/toggle_favourite/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({request_id: imageId, is_favourite: isFavourite})
    }).then(response => response.json()).then(data => {
        if (data.success) {
            closeModalProfile();
            if (isFavourite) {
                var galleryItem = document.querySelector(`.gallery-item[data-id='${imageId}']`);
                var galleryElem = galleryItem.parentElement;
                galleryElem.msnryInstance.remove(galleryItem);
                galleryElem.msnryInstance.layout();
            } else {
                addImageToFavourites(imageId);
            }
        }
    });
}

function addImageToFavourites(imageId) {
    const imageUrl = document.getElementById("modalImage").src;
    const username = document.getElementById("modalUsername").innerText;
    const prompt = document.getElementById("modalPrompt").innerText;
    const negativePrompt = document.getElementById("modalNegativePrompt").innerText;
    const width = document.getElementById("modalWidth").innerText;
    const height = document.getElementById("modalHeight").innerText;
    const seed = document.getElementById("modalSeed").innerText;
    const modelName = document.getElementById("modalModelName").innerText;
    const samplerName = document.getElementById("modalSamplerName").innerText;
    const samplerSteps = document.getElementById("modalSamplerSteps").innerText;
    const hashValue = document.getElementById("modalHashValue").innerText;
    const cfgScale = document.getElementById("modalCFGScale").innerText;

    const newGalleryItem = document.createElement('div');
    newGalleryItem.className = 'gallery-item';
    newGalleryItem.setAttribute('data-id', imageId);
    newGalleryItem.onclick = function() {
        openModalProfile(imageUrl, username, prompt, negativePrompt, width, height, seed, document.querySelector('meta[name="profile-user-id"]').content, imageId, modelName, samplerName, samplerSteps, hashValue, cfgScale, true);
    };

    const img = document.createElement('img');
    img.src = imageUrl;
    img.alt = 'Generated Image';

    newGalleryItem.appendChild(img);

    const currentUserId = document.querySelector('meta[name="current-user-id"]').content;
    const profileUserId = document.querySelector('meta[name="profile-user-id"]').content;
    if (currentUserId === profileUserId) {
        const favouritesGallery = document.getElementById('favourites');
        favouritesGallery.insertBefore(newGalleryItem, favouritesGallery.firstChild);

        var msnry = new Masonry(favouritesGallery, {
            itemSelector: '.gallery-item',
            columnWidth: '.gallery-item',
            percentPosition: true
        });
        msnry.layout();
    }
}

