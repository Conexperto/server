"""empty message

Revision ID: 44b0f3ef6d99
Revises: 
Create Date: 2021-09-14 11:46:45.167368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44b0f3ef6d99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.String(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('photo_url', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('privileges', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('method',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('speciality',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.String(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('photo_url', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('rating_average', sa.Integer(), nullable=True),
    sa.Column('rating_stars', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('rating_votes', sa.Integer(), nullable=True),
    sa.Column('headline', sa.String(length=60), nullable=True),
    sa.Column('about_me', sa.String(length=150), nullable=True),
    sa.Column('session_taken', sa.Integer(), nullable=True),
    sa.Column('complete_register', sa.Boolean(), nullable=True),
    sa.Column('timezone', sa.String(), nullable=True),
    sa.Column('link_video', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('association_expert_to_method',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('left_id', sa.Integer(), nullable=False),
    sa.Column('right_id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['left_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['method.id'], ),
    sa.PrimaryKeyConstraint('left_id', 'right_id'),
    sa.UniqueConstraint('right_id')
    )
    op.create_table('association_user_to_speciality',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('left_id', sa.Integer(), nullable=False),
    sa.Column('right_id', sa.Integer(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['left_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['speciality.id'], ),
    sa.PrimaryKeyConstraint('left_id', 'right_id'),
    sa.UniqueConstraint('right_id')
    )
    op.create_table('plan',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('coin', sa.String(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('session',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_start', sa.DateTime(), nullable=False),
    sa.Column('date_end', sa.DateTime(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.Column('expert_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['expert_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association_session_to_user',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('left_id', sa.Integer(), nullable=False),
    sa.Column('right_id', sa.Integer(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['left_id'], ['session.id'], ),
    sa.ForeignKeyConstraint(['right_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('left_id', 'right_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association_session_to_user')
    op.drop_table('session')
    op.drop_table('plan')
    op.drop_table('association_user_to_speciality')
    op.drop_table('association_expert_to_method')
    op.drop_table('user')
    op.drop_table('speciality')
    op.drop_table('method')
    op.drop_table('admin')
    # ### end Alembic commands ###
