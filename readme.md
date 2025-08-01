# 📊 AI Chart Generation Challenge

This project is a full-stack application with a FastAPI backend and a React + TypeScript + Vite frontend. It demonstrates a data-driven dashboard using SQLModel and Postgres, with AI-powered chart generation.

## Setup Instructions

### Prerequisites

- Docker & Docker Compose
- Node.js (for frontend development)
- Python 3.9+ (for backend development)

### Backend Setup

1. Copy `.env.example` to `.env` in `backend/` and adjust credentials if needed.
2. Build and start the backend services:

   ```sh
   docker-compose up --build
   ```

   This will start the Postgres database, FastAPI backend and the frontend.

3. To run tests:

   ```sh
   docker compose exec backend pytest
   ```

4. Access the frontend at [http://localhost:5173](http://localhost:5173).

### Frontend Development Setup

To prevent ESLint import warnings, install dependencies locally:

```sh
cd frontend
npm install
```

## Design Decisions

To meet the goals of this challenge within a tight 2–3 day timeframe, I prioritized a stack that allowed for rapid development without compromising future scalability.

### Backend

The backend uses a layered architecture that is straightforward yet flexible. If the application grows, this structure can evolve into a hybrid between Clean and Screaming Architecture. With the addition of dependency injection, the system could become even more modular, enabling easy testing and infrastructure swaps (e.g., changing databases, adding queues, etc.).

FastAPI was selected for its balance of performance, clarity, and speed of development. It’s a mature and well-supported framework that fits both quick MVPs and production-grade systems.

SQLModel was chosen for its ease of use and type safety. While it limits fine-grained control over complex joins, it helps deliver fast and clean code. Raw SQL is used when more control is needed—particularly for dynamic AI-generated queries.

Testing was implemented exclusively on the backend to ensure core reliability and prevent regressions. Due to time constraints, no frontend tests were included. The backend includes both unit and integration tests, focused on validating the logic and behavior of the single existing endpoint.

This setup makes it easier to scale in the future (e.g., with PostgreSQL features like indexing, partitioning, and connection pooling), even if some lower-level control is initially sacrificed.

### Frontend

The frontend follows a pragmatic file-type structure (components/, services/, types/, etc.), aligning with the KISS principle. This is ideal for MVPs and short-cycle development.

For a larger codebase, I would migrate to a domain/feature-based structure (Screaming Architecture) — organizing by folders like auth/, dashboard/, reports/, etc. This improves scalability, separation of concerns, and onboarding.

The tech stack — React + Vite + TypeScript — was chosen for its fast setup, great DX, and strong type safety. In a more complex app, I would consider adding:

- TanStack Router for type-safe, flexible routing
- Zustand for lightweight, scalable global state management
- React Hook Form + Zod for ergonomic forms and schema-based validation

These were intentionally left out for the challenge to reduce boilerplate and stay focused on core functionality.

## Trade-offs

### Backend

- **FastAPI:** Chosen for its speed of development, great typing support, and production readiness — striking a solid balance between rapid prototyping and scalability.
- **SQLModel:** Offers developer-friendly syntax and full typing, but it’s less flexible for advanced or complex queries — raw SQL is used when needed (e.g., for AI-generated queries).
- **LLM Querying:** Allows natural-language-driven analytics, which is powerful for end users. However, generated queries must be sandboxed and validated for security and correctness. A fine-tuned model using actual production data would improve reliability and relevance.
- **Chart Types:** Limited to bar, line, area, and pie to keep the challenge scoped and focused.

### Frontend

- **Simple File Structure:** Adopted a by-type structure (`components/`, `services/`, etc.) to move quickly — perfect for smaller projects or MVPs.
- **No Router / State Manager / Form Library:** Libraries like TanStack Router, Zustand, and React Hook Form + Zod were consciously excluded to avoid boilerplate and unnecessary complexity for the challenge scope.
- **Vite + React + TypeScript:** This combo gives blazing-fast dev/build times with full type safety, ideal for SPAs that don’t require SEO or SSR. A heavier stack like Next.js wasn’t justified here.
- **Scalability Path:** If this were to grow, shifting to a feature-based (Screaming Architecture) folder structure and gradually introducing the above libraries would support long-term maintainability and scale.

## Scaling Considerations

### Multi-user Usage

- **Authentication:** Add OAuth or JWT-based authentication to secure endpoints.
- **Rate Limiting:** Implement rate limiting on AI endpoints to prevent abuse.
- **Session Management:** Use Redis or similar for scalable session storage if needed.

### Large Datasets

- **Database Optimization:**

  - Migrate to normalized tables with proper indexes to fast queries.
  - Use connection pooling for efficient query handling.
  - Partition large tables if necessary.

- **Query Performance:**

  - Consider using metadata (like min/max dates from data) to reduce unnecessary LLM calls.
  - Validate and optimize AI-generated SQL queries.
  - Use caching for frequent queries (e.g., Redis).

- **AI Service:**
  - Add query complexity checks to avoid expensive joins.
  - Predefine allowed tables and columns for safe query generation.
