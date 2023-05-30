"""created models

Revision ID: 7da802970a1a
Revises: 
Create Date: 2023-05-29 21:07:40.950591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7da802970a1a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applications',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('api_key', sa.CHAR(length=32), nullable=False),
    sa.Column('_layout', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_applications_api_key'), 'applications', ['api_key'], unique=False)
    op.create_index(op.f('ix_applications_name'), 'applications', ['name'], unique=False)
    op.create_index(op.f('ix_applications_uuid'), 'applications', ['uuid'], unique=False)
    op.create_table('credentials',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('application_uuid', sa.Uuid(), nullable=False),
    sa.Column('type', sa.SmallInteger(), nullable=False),
    sa.Column('values', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['application_uuid'], ['applications.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_credentials_application_uuid'), 'credentials', ['application_uuid'], unique=False)
    op.create_index(op.f('ix_credentials_uuid'), 'credentials', ['uuid'], unique=False)
    op.create_table('emails',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('application_uuid', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('subject', sa.String(length=100), nullable=False),
    sa.Column('_template', sa.String(), nullable=False),
    sa.Column('variables', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['application_uuid'], ['applications.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_emails_application_uuid'), 'emails', ['application_uuid'], unique=False)
    op.create_index(op.f('ix_emails_name'), 'emails', ['name'], unique=False)
    op.create_index(op.f('ix_emails_uuid'), 'emails', ['uuid'], unique=False)
    op.create_table('dispatches',
    sa.Column('uuid', sa.Uuid(), nullable=False),
    sa.Column('application_uuid', sa.Uuid(), nullable=False),
    sa.Column('email_uuid', sa.Uuid(), nullable=True),
    sa.Column('template', sa.String(), nullable=False),
    sa.Column('variables', sa.JSON(), nullable=True),
    sa.Column('logs', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['application_uuid'], ['applications.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['email_uuid'], ['emails.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_dispatches_application_uuid'), 'dispatches', ['application_uuid'], unique=False)
    op.create_index(op.f('ix_dispatches_uuid'), 'dispatches', ['uuid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dispatches_uuid'), table_name='dispatches')
    op.drop_index(op.f('ix_dispatches_application_uuid'), table_name='dispatches')
    op.drop_table('dispatches')
    op.drop_index(op.f('ix_emails_uuid'), table_name='emails')
    op.drop_index(op.f('ix_emails_name'), table_name='emails')
    op.drop_index(op.f('ix_emails_application_uuid'), table_name='emails')
    op.drop_table('emails')
    op.drop_index(op.f('ix_credentials_uuid'), table_name='credentials')
    op.drop_index(op.f('ix_credentials_application_uuid'), table_name='credentials')
    op.drop_table('credentials')
    op.drop_index(op.f('ix_applications_uuid'), table_name='applications')
    op.drop_index(op.f('ix_applications_name'), table_name='applications')
    op.drop_index(op.f('ix_applications_api_key'), table_name='applications')
    op.drop_table('applications')
    # ### end Alembic commands ###
