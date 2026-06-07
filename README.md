# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This project focuses on building an unofficial student guide for Binghamton University Computer Science courses using real student experiences, course descriptions, and professor reviews. The goal is to help students understand course difficulty, workload, and teaching styles by aggregating fragmented information from Reddit threads, course syllabi, and department pages.

This information is often scattered across Reddit posts, outdated syllabi, and informal reviews, making it difficult for students to get a clear and reliable overview of what CS courses and professors are actually like.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
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

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used: all-MiniLM-L6-v2 from sentence-transformers**

**Production tradeoff reflection: This model was chosen because it is lightweight, runs locally, and performs well on semantic similarity tasks. In a production system, a larger model like OpenAI text-embedding-3-large would improve accuracy and context understanding but would increase cost and latency. A local model was preferred for simplicity and no API dependency.**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction: Use ONLY the provided context. If the answer is not in the context, say 'I don't have enough information.' Do not use external knowledge**

**How source attribution is surfaced in the response: Retrieved chunks include metadata which are from source file and chunk ID, which are returned alongside the LLM response in the UI. The frontend displays a list of sources under each answer and gives the accurate txt sources**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which professor is preferred for CS220? | students prefer Prakash over Bartenstein | I don’t have enough information. | Partially relevant. | Grounded (no hallucination), because the system did not invent a preference not supported by the documents.

| 2 | Is CS 140 good for beginners? | No, it is hard for beginners and must self learn | No, it is hard for beginners and must self learn | Relevant | Accurate

| 3 | How heavy is workload in CS220? | It is manageable | It is manageable | Relevant | Accurate 

| 4 | Should CS220 and CS140 be taken together? | No, it has prereqs | No, it has prereqs so they should not be taken together | Relevant | Accurate

| 5 | How difficult is CS140 according to students? | It is very difficult for students for sure | CS140 is considered challenging for many students, especially for beginners | Relevant | Accurate

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed: Who is preferred for CS 220?**

**What the system returned: I dont have enough information.**

**Root cause (tied to a specific pipeline stage): The retrieval system did not return any chunk that explicitly compares CS220 professors. The dataset contains course descriptions and workload discussions, but no direct preference ranking between professors, so the model correctly refused to hallucinate.**

**What you would change to fix it: Add more data and bring ratemyprofessor or add more professor-specific review data from reviews or improve document coverage for instructor comparisons.**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation: The planning.md helped define chunk size and overlap before implementation, which reduced trial-and-error during embedding and retrieval setup.**

**One way your implementation diverged from the spec, and why: The expected retrieval distance threshold (<0.5) was not strictly met, but retrieval still worked well, so the threshold was not enforced.**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI: chunking strategy + raw documents*
- *What it produced: chunking function with sliding window*
- *What I changed or overrode: adjusted chunk size to 400 and overlap to 75 after testing*

**Instance 2**

- *What I gave the AI: debugging error logs from embedding.py*
- *What it produced: fix for ChromaDB + file path issues*
- *What I changed or overrode: manually verified retrieval outputs*
