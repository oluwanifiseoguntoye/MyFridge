# MyFridge (Recipe Bot)
Recipe Bot is a chatbot that helps users find recipes based on the ingredients they have. Users can send a message containing a list of ingredients to the chatbot, and it will respond with a recipe that includes those ingredients.

# Installation
1. Clone the repository: git clone https://github.com/your-username/recipe-bot.git
2. Navigate to the project directory: cd recipe-bot
3. Install the requirements: pip install -r requirements.txt

# Usage
Start the Django server: python manage.py runserver
Send a POST request to the chatbot endpoint: http://localhost:8000/recipebot/

<b> Example Request <b>
{
    "message": "I have potatoes and chicken"
}

<b> Example Response <b>
{
    "message": "This recipe includes potatoes and chicken: Chicken and Potato Bake. Here's the recipe's URL for preparation: https://www.example.com/chicken-potato-bake"
}

# Technologies Used
<li>Django</li>
<li>Django Rest Framework</li>
<li>ChatterBot</li>
<li>NLTK</li>
