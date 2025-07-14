from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField(help_text="Step-by-step instructions")
    prep_time = models.IntegerField(
        validators=[MinValueValidator(0)], help_text="Preparation time in minutes"
    )
    cook_time = models.IntegerField(
        validators=[MinValueValidator(0)], help_text="Cooking time in minutes"
    )
    servings = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Number of servings",
    )
    difficulty = models.CharField(
        max_length=10, choices=DIFFICULTY_CHOICES, default="medium"
    )
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def total_time(self):
        return self.prep_time + self.cook_time


class RecipeRating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("recipe", "user")

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title} ({self.rating}/5)"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "recipe")

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"


class Ingredient(models.Model):
    UNIT_CHOICES = [
        # Volume
        ("tsp", "Teaspoon"),
        ("tbsp", "Tablespoon"),
        ("cup", "Cup"),
        ("ml", "Milliliter"),
        ("l", "Liter"),
        ("fl_oz", "Fluid Ounce"),
        ("pint", "Pint"),
        ("quart", "Quart"),
        ("gallon", "Gallon"),
        # Weight
        ("g", "Gram"),
        ("kg", "Kilogram"),
        ("oz", "Ounce"),
        ("lb", "Pound"),
        ("mg", "Milligram"),
        # Count
        ("piece", "Piece"),
        ("slice", "Slice"),
        ("clove", "Clove"),
        ("whole", "Whole"),
        ("can", "Can"),
        ("package", "Package"),
        ("bunch", "Bunch"),
        # Other
        ("pinch", "Pinch"),
        ("dash", "Dash"),
        ("to_taste", "To Taste"),
    ]

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients"
    )
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Amount needed",
    )
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    notes = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional notes (e.g., 'finely chopped', 'room temperature')",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.quantity} {self.get_unit_display()} {self.name}"
