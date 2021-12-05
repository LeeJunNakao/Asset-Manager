"""Create currency table

Revision ID: 946b164575b1
Revises: 2ebac442454b
Create Date: 2021-12-05 13:23:57.878230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '946b164575b1'
down_revision = '2ebac442454b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('code', sa.String(), nullable=True),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('decimal', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('code', 'user_id',
                                        name='currency_unique__code__user_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('currency')
    # ### end Alembic commands ###
