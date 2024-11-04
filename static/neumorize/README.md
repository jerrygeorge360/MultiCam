
# Neumorize

**Neumorize** is a sleek UI library that embodies the elegance of neumorphism, designed for modern dark-themed applications. With its minimalist approach, it provides soft shadows and intuitive interfaces to elevate your user experience.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [License](#license)

## Installation

To install **Neumorize**, use npm:

```bash
npm install neumorize
```

Or you can include it directly from a CDN in your HTML file:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/neumorize/dist/css/index.css">
<script src="https://cdn.jsdelivr.net/npm/neumorize/dist/js/all.min.js"></script>
```

### Cloning the Repository

If you prefer to clone the repository, follow these steps:

1. **Clone the Repository**

   Open your terminal and run the following command:
   ```git clone https://github.com/jerrygeorge360/neumorize.git```
2. **Navigate to the Cloned Directory**

    Change to the directory of the cloned repository:

    ``` cd neumorize ```

3. **Install Dependencies:**

    Install the necessary packages specified in the package.json:

    ``` npm install ```
4. **Run Gulp Tasks**

    You can run the default Gulp task to process your Sass files:

    ``` gulp ```

5. **Check Compiled Output**

    After running the Gulp tasks, you can find the compiled CSS in the output directory specified in the Gulp configuration.


6. **Link the Compiled CSS in Your Project**

    Finally, include the compiled CSS and JS file in your HTML:

    ```
    <link rel="stylesheet" href="dist/css/scss/index.css" />
    
    <script src="dist/js/all.min.js">
    ```
   
    
    




## Quick Start

1. Include **Neumorize** in your HTML file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/neumorize/dist/css/index.css">
    <title>My Neumorize Project</title>
</head>
<body>
 
    <script src="https://cdn.jsdelivr.net/npm/neumorize/dist/js/all.min.js"></script>
</body>
</html>
```



## API Documentation

This documentation provides an overview of the UI Component Library, detailing the available components, their HTML structure, and associated CSS utility classes. Each component is designed to be reusable and customizable, ensuring consistent design and functionality across your web application.

## Table of Contents
1. [Alerts](#alerts)
2. [Badges](#badges)
3. [Breadcrumbs](#breadcrumbs)
4. [Buttons](#buttons)
5. [Cards](#cards)
   - [Blog Card](#blog-card)
   - [Review Card](#review-card)
   - [Product Card](#product-card)
6. [Carousel](#carousel)
7. [Dropdown Menu](#dropdown-menu)
8. [Footer](#footer)
9. [Forms](#forms)
10. [Indicators](#indicators)
11. [Modals](#modals)
12. [Navbar](#navbar)
13. [Pagination](#pagination)
14. [Progress](#progress)
15. [Sidebar](#sidebar)
16. [Containers](#containers)
17. [Utilities](#utilities)
   - [Margin Utilities](#margin-utilities)
   - [Padding Utilities](#padding-utilities)
   - [Text Utilities](#text-utilities)
   - [Background Utilities](#background-utilities)
   - [Display Utilities](#display-utilities)
   - [Flexbox Utilities](#flexbox-utilities)
   - [Positioning Utilities](#positioning-utilities)
   - [Hover Utilities](#hover-utilities)
   - [Shadow Utilities](#shadow-utilities)
   - [Border Utilities](#border-utilities)
   - [Spacing Utilities](#spacing-utilities)

---

## Alerts
Alerts provide feedback messages to users regarding the status of their actions.

### HTML Structure
```html
<div class="alert-container">
    <div class="button-alert-success">
        <div class="alert-icon">✔</div>
        <div class="alert-message">
            <p>Success! Your action was successful.</p>
        </div>
    </div>
    <div class="button-alert-error">
        <div class="alert-icon">✖</div>
        <div class="alert-message">
            <p>Error! Something went wrong.</p>
        </div>
    </div>
    <div class="button-alert-info">
        <div class="alert-icon">ℹ</div>
        <div class="alert-message">
            <p>Info! Here's some information for you.</p>
        </div>
    </div>
</div>
```

---

## Badges
Badges are used to display labels or indicators.

### HTML Structure
```html
<div class="badge-container">
    <div class="badge-success">Success</div>
    <div class="badge-error">Error</div>
    <div class="badge-info">Info</div>
</div>
```

---

## Breadcrumbs
Breadcrumbs indicate the current page’s location within a navigational hierarchy.

### HTML Structure
```html
<ul class="breadcrumbs" id="breadcrumbs"></ul>
```

---

## Buttons
Buttons trigger actions and are essential for user interaction.

### HTML Structure
```html
<div class="button-container">
    <div class="ghost-button-container">
        <div class="button-text-icon-container">
            <div class="button-text">Help</div>
        </div>
    </div>
    <div class="toggle-button-container" id="toggle-button-container">
        <div class="toggle-button-metal" id="toggle-button-metal"></div>
    </div>
    <div class="filled-button-container">
        <div class="button-text-icon-container">
            <div class="button-text">Help</div>
        </div>
    </div>
    <div class="fab-action-button-container">
        <div class="button-text-icon-container">
            <div class="button-text">Help</div>
        </div>
    </div>
    <div class="hamburger-button-container">
        <div class="ham-strip"></div>
        <div class="ham-strip"></div>
        <div class="ham-strip"></div>
    </div>
</div>
```

---

## Cards

### Blog Card
Displays a brief overview of a blog post.

#### HTML Structure
```html
<div class="blog-card-container">
    <div class="blog-card-image-container" style="background-image: url('path-to-your-image.jpg');"></div>
    <div class="blog-card-text-container">
        <div class="blog-card-title">Blog Title</div>
        <div class="blog-card-overview-container">
            <div class="blog-card-overview">Blog overview text...</div>
        </div>
        <div class="blog-card-text-button-container">
            <a class="blog-card-text-button" href="#">Read More</a>
        </div>
    </div>
</div>
```

### Review Card
Displays user reviews for products or services.

#### HTML Structure
```html
<div class="review-card-container">
    <div class="review-card-text-container">
        <div class="product-card-title">Product Name</div>
        <div class="review-rating">
            <span class="star">★</span>
            <span class="star">★</span>
            <span class="star">★</span>
            <span class="star">★</span>
            <span class="star">☆</span>
        </div>
        <div class="review-card-overview-container">
            <div class="review-card-overview">
                This product is amazing! I have used it for a few months now, and it’s still working great. The build quality is excellent.
            </div>
        </div>
        <div class="review-card-cta-container">
            <button class="review-card-cta">Read More</button>
        </div>
    </div>
</div>
```

### Product Card
Displays product information and actions.

#### HTML Structure
```html
<div class="product-card-container">
    <div class="product-card-image-container" style="background-image: url('path_to_image.jpg');"></div>
    <div class="product-card-text-container">
        <div class="product-card-title">Product Name</div>
        <div class="product-card-overview-container">
            <div class="product-card-overview">This is a short description of the product. It highlights the key features and benefits to the customer.</div>
        </div>
        <div class="product-card-amount-container">
            <div class="product-card-amount">$99.99</div>
            <div class="product-card-count">In Stock: 12</div>
        </div>
        <div class="product-card-cta-container">
            <button class="product-card-cta1">Buy Now</button>
            <button class="product-card-cta2">Add to Cart</button>
        </div>
    </div>
</div>
```

---

## Carousel
Displays a rotating selection of items or images.

### HTML Structure
```html
<div class="carousel-container">
    <div class="carousel" id="carousel">
        <!-- Images will be inserted dynamically via JavaScript -->
    </div>
    <button class="carousel-button prev" id="prevButton">&lt;</button>
    <button class="carousel-button next" id="nextButton">&gt;</button>
</div>
```

---

## Dropdown Menu
A list of options that are displayed when the user interacts with a button.

### HTML Structure
```html
<div class="dropdown-container">
    <button class="dropdown-button">Menu</button>
    <div class="dropdown-content">
        Dropdown items will be added dynamically here
    </div>
</div>
```

---

## Footer
Displays footer information for the website.

### HTML Structure
```html
<footer class="footer-container">
    <div class="footer-content"></div>
</footer>
```

---

## Forms
Collects user input through various input fields.

### HTML Structure
```html
<form class="form-container">
    <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" placeholder="Enter your name">
    </div>
    <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" placeholder="Enter your email">
    </div>
    <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" placeholder="Enter your password">
    </div>
    <div class="form-group">
        <label for="message">Message:</label>
        <textarea id="message" placeholder="Type your message here"></textarea>
    </div>
    <div class="form-group">
        <label>Gender:</label>
        <div>
            <input type="radio" id="male" name="gender" value="male">
            <label for="male">Male</label>
            <input type="radio" id="female" name="gender" value="female">
            <label for="female">Female</label>
        </div>
    </div>
    <div class="form-group">
        <label>
            <input type="checkbox" id="terms"> I agree to the terms and conditions
        </label>
    </div>
    <button type="submit" class="form-button">Submit</button>
</form>
```

---

## Indicators
Displays status indicators and allows users to toggle their state.

### HTML Structure
```html
<div class="indicator-container">
    <div class="indicator" id="indicator

1"></div>
    <div class="indicator" id="indicator2"></div>
    <div class="indicator" id="indicator3"></div>
</div>
```

---

## Modals
Displays overlays for user interaction or information.

### HTML Structure
```html
<div class="modal-container" id="modal">
    <div class="modal-content">
        <span class="close-button" id="closeButton">&times;</span>
        <h2>Modal Title</h2>
        <p>This is a modal message.</p>
        <button class="modal-cta">OK</button>
    </div>
</div>
```

---

## Navbar
A navigation bar for accessing different sections of the site.

### HTML Structure
```html
<nav class="navbar-container">
    <ul class="navbar">
        <li class="navbar-item">Home</li>
        <li class="navbar-item">About</li>
        <li class="navbar-item">Services</li>
        <li class="navbar-item">Contact</li>
    </ul>
</nav>
```

---

## Pagination
Allows users to navigate through multiple pages of content.

### HTML Structure
```html
<div class="pagination-container">
    <button class="pagination-button prev" id="prevPage">&lt;</button>
    <span class="pagination-numbers">
        <button class="pagination-number">1</button>
        <button class="pagination-number">2</button>
        <button class="pagination-number">3</button>
    </span>
    <button class="pagination-button next" id="nextPage">&gt;</button>
</div>
```

---

## Progress
Displays progress status.

### HTML Structure
```html
<div class="progress-container">
    <div class="progress-bar" style="width: 50%;"></div>
</div>
```

---

## Sidebar
A side navigation menu.

### HTML Structure
```html
<div class="sidebar-container">
    <ul class="sidebar">
        <li class="sidebar-item">Item 1</li>
        <li class="sidebar-item">Item 2</li>
        <li class="sidebar-item">Item 3</li>
    </ul>
</div>
```

---

## Containers
Divs used for wrapping and organizing content.

### HTML Structure
```html
<div class="container"></div>
```

---

## Utilities

### Margin Utilities
Utilize classes for consistent margin spacing.
- `.m-1`, `.m-2`, etc. for margins

### Padding Utilities
Utilize classes for consistent padding spacing.
- `.p-1`, `.p-2`, etc. for padding

### Text Utilities
Classes for controlling text styling.
- `.text-center`, `.text-bold`, etc.

### Background Utilities
Classes for background color control.
- `.bg-primary`, `.bg-secondary`, etc.

### Display Utilities
Control display properties.
- `.d-block`, `.d-none`, etc.

### Flexbox Utilities
Classes for utilizing flexbox properties.
- `.d-flex`, `.flex-row`, `.align-items-center`, etc.

### Positioning Utilities
Control positioning styles.
- `.position-relative`, `.position-absolute`, etc.

### Hover Utilities
Styles applied on hover.
- `.hover-effect`, etc.

### Shadow Utilities
Control shadow properties for elements.
- `.shadow-small`, `.shadow-large`, etc.

### Border Utilities
Classes for border styling.
- `.border`, `.border-radius`, etc.

### Spacing Utilities
Classes for consistent spacing.
- `.spacing-1`, `.spacing-2`, etc.

---

#### Customization

You can customize styles by overriding default CSS variables in your own stylesheet.

```css
:root {
    --button-bg: #your-custom-color;
    --button-shadow: #your-custom-shadow;
}
```