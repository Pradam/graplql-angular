from operator import attrgetter
from graphene import relay, ObjectType, Int, String, Field, List
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import (Category, Ingredient)

def get_objects(model, **kwargs):
    return attrgetter("objects.get")(model)(**kwargs)

data = {
        "Ingredient": {
            "1": get_objects,
            "2": get_objects,
            "3": get_objects,
            "4": get_objects,
      }
    }

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node, )

class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        filter_fields = {
           'name': ['exact', 'icontains', 'istartswith'],
           'notes': ['exact', 'icontains'],
           'category': ['exact'],
           'category__name': ['exact'],
        }
        interfaces = (relay.Node, )

    @classmethod
    def get_node(cls, info, id):
        return data["Ingredient"][id](Ingredient, id=id)

class Query(object):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)
    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)
    # category = Field(CategoryType,
    #                          id=Int(),
    #                          name=String())
    # ingredient = Field(IngredientType,
    #                             id=Int(),
    #                             name=String())
    # all_categories = List(CategoryType)
    # all_ingredients = ist(IngredientType)
    #
    # def resolve_all_categories(self, info, **kwargs):
    #     return Category.objects.all()
    #
    # def resolve_all_ingredients(self, info, **kwargs):
    #     return Ingredient.objects.select_related('category').all()
    #
    # def resolve_category(self, info, **kwargs):
    #     id = kwargs.get('id')
    #     name = kwargs.get('name')
    #     if id is not None:
    #         return get_objects(Category, id=id)
    #     if name is not None:
    #         return get_objects(Category, name=name)
    #
    # def resolve_ingredient(self, info, **kwargs):
    #     id = kwargs.get('id')
    #     name = kwargs.get('name')
    #     if id is not None:
    #         return get_objects(Ingredient, id=id)
    #     if name is not None:
    #         return get_objects(Ingredient, name=name)
