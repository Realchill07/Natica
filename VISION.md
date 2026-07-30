# Natica Vision

> **A native Linux application for understanding where your time goes.**

Natica is a hierarchical time-tracking application built for people who
work on projects that naturally break down into smaller pieces. Rather
than tracking isolated timers, Natica lets users organize work into
projects and subtasks while preserving the relationship between them.

The goal is simple:

> **Know where your time went, not just how much time passed.**

------------------------------------------------------------------------

# The Problem

Most time trackers are centered around a flat list of timers or
historical sessions. As projects become more complex, it becomes
difficult to understand how effort was distributed across different
parts of the work.

Examples:

-   A programming project with frontend, backend, and bug fixing.
-   A university course with assignments and topics.
-   A game where time is split across different activities.

Natica aims to make these relationships visible.

------------------------------------------------------------------------

# Core Concepts

## Projects

Projects represent the highest level of organization.

Examples:

-   Natica
-   Data Structures
-   Gaming
-   Personal Website

------------------------------------------------------------------------

## Tasks

Projects contain tasks.

Tasks represent meaningful pieces of work that can be resumed at any
time.

Examples:

-   GUI Redesign
-   JSON Persistence
-   Assignment 3
-   Ranked Matches

Tasks are persistent---not disposable sessions.

------------------------------------------------------------------------

## Hierarchy

Tasks may contain subtasks to organize larger pieces of work.

To keep the interface manageable, the user interface may limit nesting
depth (currently planned: three levels), even if the underlying model
can support more.

------------------------------------------------------------------------

## Time

Every task tracks its own accumulated time.

Only one task may be active within a project at any given time.

Projects reflect the total time invested in the work beneath them.

------------------------------------------------------------------------

# Design Principles

-   Native Linux experience first.
-   Simple before powerful.
-   Fast to use.
-   Minimal visual clutter.
-   Hierarchy should always be obvious.
-   Data should remain under the user's control.

------------------------------------------------------------------------

# What Natica Is

-   A hierarchical time tracker.
-   A project-focused work logger.
-   A tool for understanding where time is invested.
-   A desktop application built for Linux.

------------------------------------------------------------------------

# What Natica Is Not

Natica is intentionally **not**:

-   A Pomodoro timer.
-   A habit tracker.
-   A break reminder.
-   A generic to-do list.
-   A project management suite.
-   A collaboration platform.

Those are different problems and are outside the primary vision.

------------------------------------------------------------------------

# Long-Term Goals

-   Beautiful native GTK interface.
-   Reliable local storage.
-   Rich reporting.
-   Statistics and visualizations.
-   Powerful search and filtering.
-   Tags for organizing work.
-   Exportable reports.

------------------------------------------------------------------------

# Development Philosophy

Every new feature should answer one question:

> **Does this help users understand where their time went?**

If the answer is no, it probably doesn't belong in Natica.
