"""Set delete cascade for asset entry

Revision ID: 1296b24e39d6
Revises: a28b1c5c28d3
Create Date: 2021-12-05 21:40:02.675220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1296b24e39d6'
down_revision = 'a28b1c5c28d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('asset_entry_asset_id_fkey', 'asset_entry', type_='foreignkey')
    op.drop_constraint('asset_entry_currency_id_fkey', 'asset_entry', type_='foreignkey')
    op.create_foreign_key(None, 'asset_entry', 'currency', ['currency_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'asset_entry', 'asset', ['asset_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'asset_entry', type_='foreignkey')
    op.drop_constraint(None, 'asset_entry', type_='foreignkey')
    op.create_foreign_key('asset_entry_currency_id_fkey', 'asset_entry', 'currency', ['currency_id'], ['id'])
    op.create_foreign_key('asset_entry_asset_id_fkey', 'asset_entry', 'asset', ['asset_id'], ['id'])
    # ### end Alembic commands ###
