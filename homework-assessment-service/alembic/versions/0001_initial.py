"""initial
down_revision = None
branch_labels = None
depends_on = None
"""

def upgrade() -> None:
    op.create_table(
        'assignments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('type', sa.String(length=30), nullable=False),
        sa.Column('class_id', sa.String(length=100), nullable=False, index=True),
        sa.Column('subject_id', sa.String(length=100), nullable=False, index=True),
        sa.Column('teacher_id', sa.String(length=100), nullable=False, index=True),
        sa.Column('publish_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('due_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('total_marks', sa.Float(), nullable=False),
        sa.Column('allow_late_submission', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('max_attempts', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('language_medium', sa.String(length=20), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='DRAFT'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'submissions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('assignment_id', sa.Integer(), sa.ForeignKey('assignments.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('student_id', sa.String(length=100), nullable=False, index=True),
        sa.Column('submission_text', sa.Text(), nullable=True),
        sa.Column('file_url', sa.String(length=255), nullable=True),
        sa.Column('original_file_name', sa.String(length=255), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('is_late', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('attempt_no', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='SUBMITTED'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'grade_entries',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('submission_id', sa.Integer(), sa.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False, unique=True, index=True),
        sa.Column('marks_obtained', sa.Float(), nullable=False),
        sa.Column('grade', sa.String(length=10), nullable=True),
        sa.Column('feedback_summary', sa.Text(), nullable=True),
        sa.Column('graded_by', sa.String(length=100), nullable=False),
        sa.Column('graded_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('is_published', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('grade_entries')
    op.drop_table('submissions')
    op.drop_table('assignments')