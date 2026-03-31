from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..monitoring_core.database import Base


class DashboardRecord(Base):
	__tablename__ = "dashboard_records"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	dashboard_type: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
	payload: Mapped[dict] = mapped_column(JSON, nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
	)


class ReportRecord(Base):
	__tablename__ = "report_records"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	report_type: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
	payload: Mapped[dict] = mapped_column(JSON, nullable=False)


class ReportJob(Base):
	__tablename__ = "report_jobs"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	job_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
	report_type: Mapped[str] = mapped_column(String(80), nullable=False)
	filters: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
	format: Mapped[str] = mapped_column(String(10), nullable=False)
	status: Mapped[str] = mapped_column(String(20), nullable=False)
	download_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
	)


class RiskRule(Base):
	__tablename__ = "risk_rules"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	rule_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
	name: Mapped[str] = mapped_column(String(150), nullable=False)
	condition: Mapped[str] = mapped_column(String(200), nullable=False)
	risk_level: Mapped[str] = mapped_column(String(20), nullable=False)
	active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class AuditLog(Base):
	__tablename__ = "audit_logs"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	audit_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
	user_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
	action: Mapped[str] = mapped_column(String(100), nullable=False)
	resource: Mapped[str] = mapped_column(String(255), nullable=False)
	timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
	ip_address: Mapped[str] = mapped_column(String(50), nullable=False)


class KpiSnapshot(Base):
	__tablename__ = "kpi_snapshots"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	kpi_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
	name: Mapped[str] = mapped_column(String(150), nullable=False)
	value: Mapped[float] = mapped_column(Float, nullable=False)
	unit: Mapped[str] = mapped_column(String(50), nullable=False)
	trend: Mapped[str] = mapped_column(String(20), nullable=False)
	compared_to_previous_term: Mapped[float] = mapped_column(Float, nullable=False)


class Intervention(Base):
	__tablename__ = "interventions"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	intervention_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
	student_id: Mapped[str] = mapped_column(String(50), nullable=False)
	class_id: Mapped[str] = mapped_column(String(50), nullable=False)
	reason: Mapped[str] = mapped_column(Text, nullable=False)
	assigned_to: Mapped[str] = mapped_column(String(50), nullable=False)
	status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
	notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class DashboardSnapshot(Base):
	__tablename__ = "dashboard_snapshots"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	snapshot_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
	role: Mapped[str] = mapped_column(String(50), nullable=False)
	generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
	summary: Mapped[dict] = mapped_column(JSON, nullable=False)
