from django.contrib import admin
from .models import Recipe, RecipeRating, Favorite


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "difficulty",
        "prep_time",
        "cook_time",
        "servings",
        "created_at",
    ]
    list_filter = ["difficulty", "created_at", "author"]
    search_fields = ["title", "description", "ingredients"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Basic Information", {"fields": ("title", "description", "author", "image")}),
        ("Recipe Details", {"fields": ("ingredients", "instructions", "difficulty")}),
        ("Time & Servings", {"fields": ("prep_time", "cook_time", "servings")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(RecipeRating)
class RecipeRatingAdmin(admin.ModelAdmin):
    list_display = ["recipe", "user", "rating", "created_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["recipe__title", "user__username"]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "recipe", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__username", "recipe__title"]
