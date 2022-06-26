"""initial

Revision ID: 79c7f3a90dd1
Revises: 
Create Date: 2022-06-26 21:52:27.534373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79c7f3a90dd1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('baseitems',
    sa.Column('baseitem_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('baseitem_id')
    )
    op.create_table('meals',
    sa.Column('meal_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('meal_id')
    )
    op.create_table('recipes',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('instructions', sa.String(), nullable=True),
    sa.Column('preparation_time', sa.Integer(), nullable=True),
    sa.Column('cooking_time', sa.Integer(), nullable=True),
    sa.Column('serves', sa.Integer(), nullable=True),
    sa.Column('_added_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('recipe_id')
    )
    op.create_table('shoppinglists',
    sa.Column('shoppinglist_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('shoppinglist_id')
    )
    op.create_table('shops',
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('shop_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('aisles',
    sa.Column('aisle_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('shop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.shop_id'], ),
    sa.PrimaryKeyConstraint('aisle_id')
    )
    op.create_table('ingredients',
    sa.Column('ingredient_id', sa.Integer(), nullable=False),
    sa.Column('baseitem_id', sa.Integer(), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('units', sa.String(), nullable=True),
    sa.Column('preparation', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['baseitem_id'], ['baseitems.baseitem_id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], ),
    sa.PrimaryKeyConstraint('ingredient_id')
    )
    op.create_table('mealplans',
    sa.Column('mealplan_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('meal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['meal_id'], ['meals.meal_id'], ),
    sa.PrimaryKeyConstraint('mealplan_id')
    )
    op.create_table('meals_recipes',
    sa.Column('meal_id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['meal_id'], ['meals.meal_id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], ),
    sa.PrimaryKeyConstraint('meal_id', 'recipe_id')
    )
    op.create_table('shoppinglistitems',
    sa.Column('shoppinglistitem_id', sa.Integer(), nullable=False),
    sa.Column('shoppinglist_id', sa.Integer(), nullable=True),
    sa.Column('baseitem_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('is_purchased', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['baseitem_id'], ['baseitems.baseitem_id'], ),
    sa.ForeignKeyConstraint(['shoppinglist_id'], ['shoppinglists.shoppinglist_id'], ),
    sa.PrimaryKeyConstraint('shoppinglistitem_id')
    )
    op.create_table('aisles_items',
    sa.Column('aisle_id', sa.Integer(), nullable=False),
    sa.Column('baseitem_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['aisle_id'], ['aisles.aisle_id'], ),
    sa.ForeignKeyConstraint(['baseitem_id'], ['baseitems.baseitem_id'], ),
    sa.PrimaryKeyConstraint('aisle_id', 'baseitem_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('aisles_items')
    op.drop_table('shoppinglistitems')
    op.drop_table('meals_recipes')
    op.drop_table('mealplans')
    op.drop_table('ingredients')
    op.drop_table('aisles')
    op.drop_table('users')
    op.drop_table('shops')
    op.drop_table('shoppinglists')
    op.drop_table('recipes')
    op.drop_table('meals')
    op.drop_table('baseitems')
    # ### end Alembic commands ###
