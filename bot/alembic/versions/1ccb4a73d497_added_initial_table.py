"""Added initial table

Revision ID: 1ccb4a73d497
Revises: 
Create Date: 2023-03-21 19:59:46.483652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ccb4a73d497'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_chat', sa.BigInteger(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('Active', 'Ended', 'Established', 'ChoiceOfResponder', 'RypleProcess', 'Interrupted', 'Discussion', name='stateenum'), nullable=True),
    sa.Column('result', sa.Enum('Users', 'Bot', 'Not', name='resultenum'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tg_id')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=200), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rounds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_session', sa.Integer(), nullable=True),
    sa.Column('points_team', sa.Integer(), nullable=True),
    sa.Column('points_bot', sa.Integer(), nullable=True),
    sa.Column('round_number', sa.Integer(), nullable=True),
    sa.Column('responsible', sa.Boolean(), nullable=True),
    sa.Column('is_awaited', sa.VARCHAR(length=200), nullable=True),
    sa.ForeignKeyConstraint(['id_session'], ['sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('session_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_session', sa.Integer(), nullable=True),
    sa.Column('id_qusetion', sa.Integer(), nullable=True),
    sa.Column('is_answerd', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_qusetion'], ['question.id'], ),
    sa.ForeignKeyConstraint(['id_session'], ['sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('session_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sessions_id', sa.BigInteger(), nullable=False),
    sa.Column('users_id', sa.BigInteger(), nullable=False),
    sa.Column('ready_to_play', sa.Boolean(), nullable=True),
    sa.Column('is_creator', sa.Boolean(), nullable=True),
    sa.Column('is_captain', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['sessions_id'], ['sessions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session_users')
    op.drop_table('session_question')
    op.drop_table('rounds')
    op.drop_table('answer')
    op.drop_table('users')
    op.drop_table('sessions')
    op.drop_table('question')
    # ### end Alembic commands ###
