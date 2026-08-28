# Security Policy

## Scope

LUNEX is primarily a specification and a set of diagrams — not running software with an attack surface in the usual sense. The one part of this repository that *does* execute code is `tools/` (the diagram-generation scripts and the PDF build pipeline). If you find a security issue there — for example, a way a malicious input file could cause unintended behavior in `tools/pdf/build_pdf.py` — report it the same way as below.

If you've found a factual error, gap, or contradiction in the *specification itself* (not a security issue), that belongs in [GitHub Discussions](../../discussions) or [Issues](../../issues), per `CONTRIBUTING.md` — not here.

## Reporting a Vulnerability

Please report security issues privately, not as a public Issue or Discussion post. Email **conduct@lunex.cloud** with:

- A description of the issue and where it is (which script, which file).
- Steps to reproduce, if applicable.
- The potential impact, as you understand it.

You should expect an acknowledgment within a few days. This is a small, single-maintainer project at this stage — response time won't match what you'd get from a large organization's security team, but every report will be read and taken seriously.

## Disclosure

Please allow a reasonable amount of time for a fix before any public disclosure. Given the current scope of `tools/` (local build scripts, not a hosted service), most realistic findings will be low-severity — but report them the same way regardless.

## Supported Versions

LUNEX is pre-1.0 (currently v0.1, draft). There is no long-term-support version — only the current `main` branch is maintained. Fixes land there; there is no backporting policy yet.
