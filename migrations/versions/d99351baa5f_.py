"""empty message

Revision ID: d99351baa5f
Revises: 2d3ff5ecd700
Create Date: 2015-09-14 23:28:20.030855

"""

# revision identifiers, used by Alembic.
revision = 'd99351baa5f'
down_revision = '2d3ff5ecd700'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=40), nullable=True),
    sa.Column('description', sa.Unicode(length=400), nullable=True),
    sa.Column('user_id', sa.Unicode(length=200), nullable=True),
    sa.Column('client_id', sa.Unicode(length=40), nullable=True),
    sa.Column('client_secret', sa.Unicode(length=55), nullable=False),
    sa.Column('is_confidential', sa.Boolean(), nullable=True),
    sa.Column('redirect_uris_text', sa.UnicodeText(), nullable=True),
    sa.Column('default_scopes_text', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('client_id')
    )
    op.create_index(op.f('ix_client_client_secret'), 'client', ['client_secret'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Unicode(length=100), nullable=False),
    sa.Column('name', sa.Unicode(length=200), nullable=True),
    sa.Column('password', sa.Unicode(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('grant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Unicode(length=200), nullable=True),
    sa.Column('client_id', sa.Unicode(length=40), nullable=False),
    sa.Column('code', sa.Unicode(length=255), nullable=False),
    sa.Column('redirect_uri', sa.Unicode(length=255), nullable=True),
    sa.Column('expires', sa.DateTime(), nullable=True),
    sa.Column('_scopes', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.client_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_grant_code'), 'grant', ['code'], unique=False)
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Unicode(length=40), nullable=False),
    sa.Column('user_id', sa.Unicode(length=200), nullable=True),
    sa.Column('token_type', sa.Unicode(length=40), nullable=True),
    sa.Column('access_token', sa.Unicode(length=255), nullable=True),
    sa.Column('refresh_token', sa.Unicode(length=255), nullable=True),
    sa.Column('expires', sa.DateTime(), nullable=True),
    sa.Column('_scopes', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.client_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_token'),
    sa.UniqueConstraint('refresh_token')
    )
    op.drop_table('grants')
    op.drop_table('clients')
    op.drop_table('tokens')
    op.drop_table('users')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=100), nullable=False),
    sa.Column('name', sa.VARCHAR(length=200), nullable=True),
    sa.Column('password', sa.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('tokens',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('client_id', sa.VARCHAR(length=40), nullable=False),
    sa.Column('user_id', sa.VARCHAR(length=200), nullable=True),
    sa.Column('token_type', sa.VARCHAR(length=40), nullable=True),
    sa.Column('access_token', sa.VARCHAR(length=255), nullable=True),
    sa.Column('refresh_token', sa.VARCHAR(length=255), nullable=True),
    sa.Column('expires', sa.DATETIME(), nullable=True),
    sa.Column('_scopes', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], [u'clients.client_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_token'),
    sa.UniqueConstraint('refresh_token')
    )
    op.create_table('clients',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=40), nullable=True),
    sa.Column('description', sa.VARCHAR(length=400), nullable=True),
    sa.Column('user_id', sa.VARCHAR(length=200), nullable=True),
    sa.Column('client_id', sa.VARCHAR(length=40), nullable=True),
    sa.Column('client_secret', sa.VARCHAR(length=55), nullable=False),
    sa.Column('is_confidential', sa.BOOLEAN(), nullable=True),
    sa.Column('redirect_uris_text', sa.TEXT(), nullable=True),
    sa.Column('default_scopes_text', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('client_id')
    )
    op.create_table('grants',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.VARCHAR(length=200), nullable=True),
    sa.Column('client_id', sa.VARCHAR(length=40), nullable=False),
    sa.Column('code', sa.VARCHAR(length=255), nullable=False),
    sa.Column('redirect_uri', sa.VARCHAR(length=255), nullable=True),
    sa.Column('expires', sa.DATETIME(), nullable=True),
    sa.Column('_scopes', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], [u'clients.client_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('token')
    op.drop_index(op.f('ix_grant_code'), table_name='grant')
    op.drop_table('grant')
    op.drop_table('user')
    op.drop_index(op.f('ix_client_client_secret'), table_name='client')
    op.drop_table('client')
    ### end Alembic commands ###
