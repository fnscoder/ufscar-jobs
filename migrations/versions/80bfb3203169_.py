"""empty message

Revision ID: 80bfb3203169
Revises: 29fd6d1fc6da
Create Date: 2017-11-23 19:08:59.269351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80bfb3203169'
down_revision = '29fd6d1fc6da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('evaluations_company_id_fkey', 'evaluations', type_='foreignkey')
    op.create_foreign_key(None, 'evaluations', 'users', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'evaluations', type_='foreignkey')
    op.create_foreign_key('evaluations_company_id_fkey', 'evaluations', 'companies', ['company_id'], ['id'])
    # ### end Alembic commands ###
