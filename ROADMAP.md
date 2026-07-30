# Natica Roadmap

> **Vision:** Build a native Linux time-tracking application focused on
> organizing work hierarchically and understanding where time is spent.
> The app should stay focused on **time tracking**, not become a general
> productivity suite.

------------------------------------------------------------------------

# Guiding Principles

-   Projects are containers for work.
-   Tasks/Subtasks are persistent and can be resumed at any time.
-   A task may contain subtasks (maximum nesting depth: **3**).
-   Only **one task** may be active within a project at a time.
-   Multiple projects may run independently.
-   Every feature should answer the question: \> **"Does this help the
    user understand where their time went?"**

------------------------------------------------------------------------

# In Progress

-   [x] Multiple independent projects
-   [x] Parent/child timer structure
-   [x] Start / Pause / Resume
-   [x] Live timer updates
-   [x] Multiple projects can run simultaneously
-   [x] Resume switches active sibling automatically
-   [ ] UI redesign

------------------------------------------------------------------------

# Next Release (v0.2)

## User Interface

-   [ ] Modern GTK4 / Libadwaita interface
-   [ ] Better project layout
-   [ ] Better task hierarchy visualization
-   [ ] Expand / Collapse projects
-   [ ] Expand / Collapse subtasks
-   [ ] Inline renaming

## Projects

-   [ ] Create project
-   [ ] Rename project
-   [ ] Delete project

## Tasks

-   [ ] Create subtask
-   [ ] Rename subtask
-   [ ] Delete subtask
-   [ ] Resume any task
-   [ ] Mark complete / incomplete

------------------------------------------------------------------------

# v0.3

## Persistence

-   [ ] JSON save/load
-   [ ] Auto-save
-   [ ] Import project data
-   [ ] Export project data
-   [ ] Backups

------------------------------------------------------------------------

# v0.4

## Organization

-   [ ] Tags
-   [ ] Tag colors
-   [ ] Filter by tags
-   [ ] Search projects
-   [ ] Search tasks
-   [ ] Sort projects

------------------------------------------------------------------------

# v0.5

## Reports

-   [ ] Daily report
-   [ ] Weekly report
-   [ ] Monthly report
-   [ ] Custom date range report
-   [ ] Export CSV
-   [ ] Export PDF
-   [ ] Time by project
-   [ ] Time by task
-   [ ] Time by tag

------------------------------------------------------------------------

# Future

## Statistics

-   [ ] Lifetime tracked time
-   [ ] Time today
-   [ ] Time this week
-   [ ] Time this month
-   [ ] Most worked-on project
-   [ ] Most worked-on task
-   [ ] Average daily tracked time

## Visualizations

-   [ ] Charts
-   [ ] Timeline view
-   [ ] Calendar view

## Advanced

-   [ ] Drag & drop task reordering
-   [ ] Move task to another parent
-   [ ] Archive projects
-   [ ] Pin favorite projects
-   [ ] Keyboard shortcuts
-   [ ] Context menus
-   [ ] Git integration (optional)

## Low Priority

-   [ ] Task notes
-   [ ] Attachments

------------------------------------------------------------------------

# Ideas Parking Lot

Ideas that seem interesting but are intentionally **not** part of the
current roadmap.

-   Better reporting dashboards
-   More visual analytics
-   Additional export formats
-   Plugin system
-   Cloud sync
-   Collaboration
-   AI-powered insights

------------------------------------------------------------------------

# Out of Scope

These do **not** fit the current vision.

-   Pomodoro timer
-   Break reminders
-   Habit tracking
-   Time budgets
-   General task management unrelated to time tracking

------------------------------------------------------------------------

# Philosophy

Natica should feel like a **filesystem for your time**.

Projects contain work.

Work contains more work.

Every node tells you **how much time** you've invested, and reports help
you understand where that time went.
