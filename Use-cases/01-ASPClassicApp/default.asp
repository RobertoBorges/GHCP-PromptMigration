<!--#include file="includes/header.asp"-->

<div class="hero">
    <h1>Welcome to Classic ASP Store</h1>
    <p>Your one-stop shop for quality office products</p>
    <a href="products.asp" class="button">Browse Products</a>
</div>

<div class="features">
    <div class="feature">
        <h2>Quality Products</h2>
        <p>We offer only the highest quality office equipment and accessories.</p>
    </div>
    
    <div class="feature">
        <h2>Fast Shipping</h2>
        <p>Get your items delivered to your doorstep within 2-3 business days.</p>
    </div>
    
    <div class="feature">
        <h2>Customer Support</h2>
        <p>Our support team is available 24/7 to assist you with any questions.</p>
    </div>
</div>

<style>
    .hero {
        text-align: center;
        padding: 50px 20px;
        background: #f9f9f9;
        margin-bottom: 30px;
    }
    
    .hero h1 {
        font-size: 2.5em;
        margin-bottom: 15px;
    }
    
    .hero p {
        font-size: 1.2em;
        margin-bottom: 25px;
        color: #666;
    }
    
    .features {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        grid-gap: 20px;
        margin-top: 30px;
    }
    
    .feature {
        background: #f9f9f9;
        padding: 20px;
        border-radius: 5px;
    }
    
    .feature h2 {
        margin-bottom: 10px;
        color: #333;
    }
    
    @media(max-width: 768px) {
        .hero h1 {
            font-size: 2em;
        }
    }
</style>

<!--#include file="includes/footer.asp"-->
