<!--#include file="includes/header.asp"-->

<h1>Contact Us</h1>

<%
' Process form submission
If Request.ServerVariables("REQUEST_METHOD") = "POST" Then
    Dim name, email, message, isValid
    
    name = Trim(Request.Form("name"))
    email = Trim(Request.Form("email"))
    message = Trim(Request.Form("message"))
    
    isValid = True
    
    If name = "" Then
        isValid = False
    End If
    
    If email = "" Then
        isValid = False
    End If
    
    If message = "" Then
        isValid = False
    End If
    
    If isValid Then
        ' In a real application, you would save this to a database or send an email
        ' For this demo, we'll just display a success message
        Response.Write("<div class='success-message'>Thank you for your message! We'll get back to you soon.</div>")
    Else
        Response.Write("<div class='error-message'>Please fill out all fields.</div>")
    End If
End If
%>

<div class="contact-form">
    <p>Have questions or comments? Fill out the form below to get in touch with us.</p>
    
    <form method="post" action="contact.asp">
        <div class="form-group">
            <label for="name">Your Name:</label>
            <input type="text" id="name" name="name" value="<%= Request.Form("name") %>" required>
        </div>
        
        <div class="form-group">
            <label for="email">Email Address:</label>
            <input type="email" id="email" name="email" value="<%= Request.Form("email") %>" required>
        </div>
        
        <div class="form-group">
            <label for="message">Message:</label>
            <textarea id="message" name="message" rows="5" required><%= Request.Form("message") %></textarea>
        </div>
        
        <button type="submit" class="button">Send Message</button>
    </form>
</div>

<div class="contact-info">
    <h2>Contact Information</h2>
    <p><strong>Address:</strong> 123 Store St, Web City, WC 12345</p>
    <p><strong>Phone:</strong> (555) 123-4567</p>
    <p><strong>Email:</strong> info@classicaspstore.com</p>
    <p><strong>Hours:</strong> Monday-Friday: 9am-5pm, Saturday: 10am-4pm</p>
</div>

<style>
    .contact-form {
        background: #f9f9f9;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .form-group {
        margin-bottom: 15px;
    }
    
    label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }
    
    input[type="text"],
    input[type="email"],
    textarea {
        width: 100%;
        padding: 8px;
        border: 1px solid #ddd;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 4px;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 4px;
    }
    
    .contact-info {
        background: #f9f9f9;
        padding: 20px;
    }
    
    .contact-info p {
        margin-bottom: 10px;
    }
</style>

<!--#include file="includes/footer.asp"-->
