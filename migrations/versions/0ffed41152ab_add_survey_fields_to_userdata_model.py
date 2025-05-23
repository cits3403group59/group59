"""Add survey fields to UserData model

Revision ID: 0ffed41152ab
Revises: 
Create Date: 2025-05-07 18:19:51.683956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ffed41152ab'
down_revision = 'c5029594f206'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('friend_request',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('sender_id', sa.Integer(), nullable=False),
    # sa.Column('receiver_id', sa.Integer(), nullable=False),
    # sa.Column('status', sa.String(length=20), nullable=True),
    # sa.Column('timestamp', sa.DateTime(), nullable=True),
    # sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
    # sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    # sa.PrimaryKeyConstraint('id')
    # )
    # op.create_table('friendships',
    # sa.Column('user_id', sa.Integer(), nullable=False),
    # sa.Column('friend_id', sa.Integer(), nullable=False),
    # sa.ForeignKeyConstraint(['friend_id'], ['user.id'], ),
    # sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    # sa.PrimaryKeyConstraint('user_id', 'friend_id')
    # )
    with op.batch_alter_table('user_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sleep_hours', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('coffee_intake', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('social_media', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('daily_steps', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('exercise_minutes', sa.Integer(), nullable=True))
        batch_op.drop_column('carbon_footprint')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('carbon_footprint', sa.FLOAT(), nullable=False))
        batch_op.drop_column('exercise_minutes')
        batch_op.drop_column('daily_steps')
        batch_op.drop_column('social_media')
        batch_op.drop_column('coffee_intake')
        batch_op.drop_column('sleep_hours')

    op.drop_table('friendships')
    op.drop_table('friend_request')
    # ### end Alembic commands ###
