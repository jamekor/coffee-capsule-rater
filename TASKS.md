# Task Breakdown

- [x] Draft PRD and task breakdown

## 1. Project Setup
- [x] Repository & Dev Environment
  - [x] Initialize project repo, install framework (e.g., Django + React or Flask + plain JS).
  - [x] Configure linting, formatting, and testing tools.
- [x] CI/CD Setup
  - [x] Add automated testing & build pipeline (GitHub Actions, etc.).

## 2. Backend Development
- [x] Data Models
    - [x] `User` model with authentication fields.
    - [x] `Capsule` model: name, brand, roast level, flavor notes.
    - [x] `Rating` model: rating value, review text, timestamp, relation to User & Capsule.
- [ ] User APIs
  - [ ] Register, login, edit profile endpoints.
- [ ] Capsule APIs
  - [ ] Create, list, retrieve capsules.
- [ ] Rating APIs
  - [ ] Submit rating, list ratings per capsule, calculate average.
- [ ] Validation & Security
  - [ ] Password hashing, input validation, authentication middleware.
- [ ] Tests
  - [ ] Unit tests for models and endpoints, integration tests for main flows.

## 3. Frontend Development
- [x] Layout & Navigation
  - [x] Header, footer, navigation links to capsules, add capsule, profile.
- [x] Authentication Views
  - [x] Sign-up, login, profile editing forms.
- [x] Capsule Views
  - [x] List view with search/filter.
  - [x] Detail view with rating history and add-rating form.
  - [x] Add capsule form.
- [x] Rating Component
  - [x] Form for rating submission (score + review text).
  - [x] Display average rating & user rating history.
- [x] Client-Side Validation & UX Enhancements
  - [x] Form error handling, loading indicators, mobile responsiveness.
- [x] Tests
  - [x] Component/unit tests, basic end-to-end tests for critical paths.

## 4. Deployment & Monitoring
- [ ] Deployment Environment
  - [ ] Set up staging and production environments (e.g., Heroku, Vercel).
- [ ] Logging & Monitoring
  - [ ] Basic logging for error tracking (e.g., Sentry, CloudWatch).
- [ ] Documentation
  - [ ] README, API docs, user instructions.

## 5. Project Management & Iteration
- [ ] Beta Testing
  - [ ] Collect user feedback, track bugs/feature requests.
- [ ] Iteration & Improvements
  - [ ] Prioritize backlog, implement improvements for public release.
