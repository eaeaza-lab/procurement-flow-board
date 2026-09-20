# Procurement Flow Board — Specification

## Problem

Small procurement teams often track purchase requests, supplier quotes, approvals, deliveries, and payments in disconnected spreadsheets. That makes it hard to see which orders are stalled, where money is at risk, and whether expected margin is shrinking.

## Target user

A procurement coordinator at a small operations team who needs a quick, offline view of synthetic procurement work for demos, learning, or internal workflow exploration.

## MVP scope

- An offline React/Vite interface backed by a local FastAPI service and SQLite database.
- Seeded, synthetic purchase requests, quotes, approvals, deliveries, and payments.
- A searchable Kanban board grouped by procurement stage.
- A request-detail view with linked flow records.
- Margin and delivery-delay indicators derived from seed data.
- A sortable/filterable tabular view using TanStack Table.

## Current implementation

The M2 API provides a local FastAPI application, a SQLite schema for all five workflow record types, repeatable synthetic seed records, request list/detail reads, linked workflow records, and deterministic margin and delivery-delay indicators. The board UI remains part of later milestones.

## Explicit non-goals

- Real company, supplier, employee, marketplace, account, or customer data.
- Authentication, multi-user collaboration, or cloud sync.
- Live supplier integrations, email, payments, or network calls at runtime.
- Production accounting, tax, currency conversion, or audit compliance.
- Deployments, billing, and SaaS tenancy in the MVP.

## Acceptance criteria

1. The repository contains the documented project charter and runnable skeleton. Check: `python test/smoke.py`
2. The documented automated check passes offline on Windows. Check: `python test/smoke.py`
3. The starter model exposes all five workflow record types and only synthetic fixture names. Check: `python test/smoke.py`
4. The project has an execution plan with command-checkable milestones. Check: `python test/smoke.py`
