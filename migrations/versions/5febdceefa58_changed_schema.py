"""Changed schema

Revision ID: 5febdceefa58
Revises: ccbed12a563d
Create Date: 2024-11-04 23:31:40.935359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5febdceefa58'
down_revision = 'ccbed12a563d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stream', schema=None) as batch_op:
        batch_op.alter_column('object_id',
               existing_type=sa.BLOB(),
               type_=sa.String(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stream', schema=None) as batch_op:
        batch_op.alter_column('object_id',
               existing_type=sa.String(),
               type_=sa.BLOB(),
               existing_nullable=False)

    # ### end Alembic commands ###
