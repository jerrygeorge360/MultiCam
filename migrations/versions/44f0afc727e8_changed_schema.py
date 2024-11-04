"""Changed schema

Revision ID: 44f0afc727e8
Revises: dedcf868924c
Create Date: 2024-11-03 11:19:21.495107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44f0afc727e8'
down_revision = 'dedcf868924c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_image_url', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('profile_image_url')

    # ### end Alembic commands ###