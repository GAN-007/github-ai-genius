# GitHub AI Genius Agent

## Overview
This repository contains the complete production blueprint and tooling for the GitHub AI Genius Agent—an autonomous system capable of secure, comprehensive repository analysis, modification, and rebuilding.

## Components

### 1. Production Blueprint (Web)
A React-based interactive documentation site detailing the architectural specification, security model, and RAG pipeline.
- **Location**: `/web`
- **Stack**: React 19, Tailwind CSS 4, Shadcn UI
- **Design**: Cyber-Brutalist / Terminal Chic

### 2. Gitmal CLI (Tooling)
A static page generator for Git repositories, serving as a core utility for the agent's visualization capabilities.
- **Location**: `/gitmal`
- **Stack**: Go 1.24
- **Features**: Syntax highlighting, commit history, markdown rendering

## Getting Started

### Web Blueprint
```bash
cd web
pnpm install
pnpm dev
```

### Gitmal CLI
```bash
cd gitmal
go build
./gitmal
```

## Architecture
The system relies on a hybrid RAG pipeline (Vector + Graph) and a secure GitHub App authentication model to perform large-scale repository refactoring safely.

## License
MIT
