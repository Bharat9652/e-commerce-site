document.addEventListener('DOMContentLoaded', function () {
  // Add an event listener to the search form
  const searchForm = document.getElementById('searchForm');
  searchForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from submitting

    // Get the search input value and selected category filter
    const keyword = document.getElementById('ingredientsInput').value;
    const categoryFilter = document.getElementById('categoryFilter').value;

    // Get the min and max prices & ratings
    const minPrice = document.getElementById('minPrice').value;
    const maxPrice = document.getElementById('maxPrice').value;
    const minRating = document.getElementById('minRating').value;
    const maxRating = document.getElementById('maxRating').value;

    // Make a request to your Flask API with keyword, category filter, min, and max prices
    fetch(`/search/products?keyword=${keyword}&category_filter=${categoryFilter}&minPrice=${minPrice}&maxPrice=${maxPrice}&minRating=${minRating}&maxRating=${maxRating}`)
      .then(response => response.json())
      .then(data => {
        // Hide the explore menu container
        const exploreMenuContainer = document.getElementById('exploreMenuSection');
        exploreMenuContainer.style.display = 'none';

        // Populate the product list with the search results
        populateProductList(data);
      })
      .catch(error => {
        console.error('Error fetching search results:', error);
      });
  });

  // Add an event listener to update the category filter when the user selects a category
  const categoryDropdown = document.getElementById('categoryFilter');
  categoryDropdown.addEventListener('change', function () {
    // Trigger the search form submission when the category is changed
    searchForm.dispatchEvent(new Event('submit'));
  });

  // Function to populate the product list based on search results
  function populateProductList(results) {
    const productListContainer = document.getElementById('searchResultsContainer');

    // Clear previous content
    productListContainer.innerHTML = '';

    // Check if there are any search results
    if (results.length === 0) {
      const noResultsMessage = document.createElement('p');
      noResultsMessage.textContent = 'No results found.';
      productListContainer.appendChild(noResultsMessage);
      return;
    }

    // Loop through the search results and create product cards
    results.forEach(result => {
      const productCard = document.createElement('div');
      productCard.className = 'menu-item-card shadow p-3 mb-3';

      const productImage = document.createElement('img');
      productImage.src = result.ImageURL;
      productImage.className = 'menu-item-image w-100';

      const productTitle = document.createElement('h4');
      productTitle.textContent = result.ProductName;

      // Create "View Item Details" button
      const viewDetailsButton = document.createElement('button');
      viewDetailsButton.textContent = 'View Item Details';
      viewDetailsButton.className = 'btn btn-info mr-2';
      viewDetailsButton.addEventListener('click', function () {
        // Show details modal
        showDetailsModal(result);
      });

      // Create "Add to Cart" button
      const addToCartButton = document.createElement('button');
      addToCartButton.textContent = 'Add to Cart';
      addToCartButton.className = 'btn btn-success';
      addToCartButton.addEventListener('click', function () {
        // Add logic to add item to cart
        alert(`Added ${result.ProductName} to cart`);
      });

      // Append elements to the product card
      productCard.appendChild(productImage);
      productCard.appendChild(productTitle);
      productCard.appendChild(viewDetailsButton);
      productCard.appendChild(addToCartButton);

      // Append the product card to the product list container
      productListContainer.appendChild(productCard);
    });
  }

  // Function to show details modal
  function showDetailsModal(product) {
    const modalOverlay = document.getElementById('modalOverlay');
    const modalContent = document.getElementById('modalContent');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    const closeButton = document.getElementById('closeButton');

    // Update modal content with product details
    modalTitle.textContent = product.ProductName;
    modalBody.innerHTML = `
      <img src="${product.ImageURL}" class="modal-image" />
      <p>Brand: ${product.BrandName}</p>
      <p>Specifications: ${product.Specifications}</p>
      <p>Price: $${product.Price}</p>
      <p>Rating: ${product.Rating}</p>
      <p>Manufactured Date: ${product.ManufacturedDate}</p>
    `;

    // Display the modal
    modalOverlay.style.display = 'flex';

    // Close the modal when the close button is clicked
    closeButton.addEventListener('click', () => {
      modalOverlay.style.display = 'none';
    });
  }
});


// Close the modal when the close button is clicked
closeButton.addEventListener('click', () => {
  modalOverlay.style.display = 'none';
});