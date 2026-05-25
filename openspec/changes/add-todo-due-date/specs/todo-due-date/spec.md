## ADDED Requirements

### Requirement: Optional due date on create

The system SHALL accept an optional due date when a user adds a todo. If provided, the due date MUST be stored as `YYYY-MM-DD`. If omitted or invalid, the todo MUST be stored with no due date (`NULL`).

#### Scenario: Add todo with due date

- **WHEN** user submits the add form with non-empty task text and a valid due date
- **THEN** a new todo is created with that due date persisted

#### Scenario: Add todo without due date

- **WHEN** user submits the add form with task text and leaves the due date empty
- **THEN** a new todo is created with no due date

#### Scenario: Invalid due date ignored

- **WHEN** user submits the add form with a due date that is not valid `YYYY-MM-DD`
- **THEN** a new todo is created with no due date

### Requirement: Due date visible in list

The system SHALL display each todo's due date in the todo list when a due date is set. Todos without a due date MUST NOT show a due date label.

#### Scenario: Todo with due date shows label

- **WHEN** a todo has a stored due date
- **THEN** the list item shows a human-readable due date

#### Scenario: Todo without due date has no label

- **WHEN** a todo has no due date
- **THEN** the list item does not show a due date label

### Requirement: Overdue active todos highlighted

The system SHALL visually distinguish active (not done) todos whose due date is before today as overdue.

#### Scenario: Active todo past due date

- **WHEN** a todo is not done and its due date is before today
- **THEN** the list item is styled as overdue

#### Scenario: Active todo due today or later

- **WHEN** a todo is not done and its due date is today or in the future
- **THEN** the list item is not styled as overdue

#### Scenario: Completed todo never overdue

- **WHEN** a todo is marked done
- **THEN** the list item is not styled as overdue regardless of due date

### Requirement: Active todos sorted by due date

The system SHALL order incomplete todos with due dates before those without, and among dated todos sort by earliest due date first. Incomplete todos without a due date MUST appear after all dated incomplete todos, ordered by creation time (newest first). Completed todos MUST remain grouped after active todos, ordered by creation time (newest first).

#### Scenario: Multiple active todos with due dates

- **WHEN** the list contains incomplete todos with different due dates
- **THEN** they appear ordered soonest due date first

#### Scenario: Active todos with and without due dates

- **WHEN** the list contains incomplete todos with and without due dates
- **THEN** dated todos appear before undated todos

### Requirement: Database supports due date column

The system SHALL persist `due_date` on the `todos` table as a nullable text column. Existing databases MUST be migrated without data loss.

#### Scenario: Existing database upgraded on startup

- **WHEN** the application starts against a database created before this feature
- **THEN** the `due_date` column exists and existing rows have no due date
