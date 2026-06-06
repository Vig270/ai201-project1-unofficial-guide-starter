# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

This project focuses on building an unofficial student guide for Binghamton University Computer Science courses using real student experiences, course descriptions, and professor reviews. The goal is to help students understand course difficulty, workload, and teaching styles by aggregating fragmented information from Reddit threads, course syllabi, and department pages.

This information is often scattered across Reddit posts, outdated syllabi, and informal reviews, making it difficult for students to get a clear and reliable overview of what CS courses and professors are actually like.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit | cs220       | data/raw/reddit_cs140_difficulty.txt
| 2 | Reddit | cs140       | data/raw/reddit_cs220_workload.txt
| 3 | Reddit | cs prereq   | data/raw/reddit_cs_prereqs.txt
| 4 | Reddit | cs experience | data/raw/reddit_cs_experience.txt
| 5 | Coursicle | gives reviews on professor | data/raw/cs140_overview.txt
| 6 | studocu | gives a good idea on the expectations of class | data/raw/cs140_syllabus.txt
| 7 | Coursicle | gives reviews on professor | data/raw/cs220_description.txt
| 8 | Binghamton | talks about undergradwork | data/raw/cs_undergrad_program.txt
| 9 | Binghamton | lists the facility directories | data/raw/cs_faculty_directory.txt
| 10 | Binghamton | comes with several cs departments | data/raw/cs_department.txt

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

Chunk size: 400 characters
Overlap: 75 characters

Reasoning:
Documents include short Reddit comments and medium-length course descriptions. A moderate chunk size preserves full ideas without splitting opinions or course details. Overlap ensures important context (like prerequisites or professor opinions) is not lost across boundaries.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

Embedding model:all-MiniLM-L6-v2 (sentence-transformers)

Top-k: 3 - 5 chunks

Production tradeoff reflection: Retrieving 3–5 chunks provides enough context for the LLM without overwhelming it with irrelevant information. Embeddings help match meaning even when wording differs (ex, “hard class” vs “very difficult workload”).

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | How difficult is CS140 according to students? | It is considered hard / weed-out / depends on professor
| 2 | Which professor is preferred for CS220? | Aravind Prakash vs Bartenstein opinions
| 3 | Is CS140 good for beginners? | Mixed, depends on C and assembly experience
| 4 | How heavy is workload in CS220? | ~5 homeworks + projects, medium-high workload
| 5 | Should CS220 and CS140 be taken together? | Usually discouraged due to prereqs + workload

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Reddit comments are noisy and opinion-based, which may confuse retrieval and mix conflicting answers.

2. Course syllabus are long and may get split across chunks, losing important context like grading policies.

---

## Architecture

Documents (raw txt files)
        ↓
Chunking (Python script)
        ↓
Embeddings (all-MiniLM-L6-v2)
        ↓
Vector DB (ChromaDB)
        ↓
Retrieval (top-k similarity search)
        ↓
LLM Generation (ChatGPT / API)

---

## AI Tool Plan

I will use ChatGPT to help understand Milestone instructions and clarify concepts like chunking and retrieval.

For chunking, I will provide my Chunking Strategy section and ask it to help implement a Python function for splitting text with 400-character chunks and 75-character overlap.

For debugging, I will use ChatGPT to help fix errors in file paths and chunking logic.

I will verify outputs manually by checking chunk sizes and ensuring all documents are properly processed.

I will use Copilot in VS Code for autocomplete and implementation assistance during embedding and vector store setup.

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
